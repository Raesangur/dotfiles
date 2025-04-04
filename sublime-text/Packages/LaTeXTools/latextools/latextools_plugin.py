"""
Plugin auto-discovery system intended for use in LaTeXTools package.

Overview
========

A plugin is a Python class that extends LaTeXToolsPlugin and provides some
functionality, usually via a function, that LaTeXTools code interacts with.
This module provide mechanisms for loading such plugins from arbitrary files
and configuring the environment in which they are used. It tries to make as
few assumptions as possible about how the consuming code and the plugin
interact. At it's heart it is just a plugin registry.

A quick example plugin:

    from latextools_plugin import LaTeXToolsPlugin

    class PluginSample(LaTeXToolsPlugin):
        def do_something():
            pass

And example consuming code:

    from latextools_plugin import get_plugin

    plugin = get_plugin('plugin_sample')
    # instantiate and use the plugin
    plugin().do_something()

Note that we make no assumption about how plugins are used, just how they are
loaded. It is up to the consuming code to provide a protocol for interaction,
i.e., methods that will be called, etc.

As shown above, plugin others should import and sub-class the
`LaTeXToolsPlugin` class from this module, as this will ensure the plugin is
properly registered and so available to consuming code. Plugins are registered
by using a version of the class name, so it is important that all plugins used
have a unique class name. The conversion is similar to how Sublime handles
*Command objects, so the name is converted from CamelCase to snake_case. In
addition, the word "Plugin", if it occurs at the end of the class name, is
removed.

Consuming code loads a plugin from the registry by passing the converted plugin
name to the `get_plugin()` function defined in this class. What is returned is
the class itself, i.e., it is the responsibility of the consuming code to
initialize the plugin and then interact with it.

Finding Plugins
===============

The following loading mechanisms for plugins are provided, either using
configuration options or the `add_plugin_path()` function defined in this
module.

Configuration options:
    `plugin_paths`: in the standard user configuration.
         A list of either directories to search for plugins or paths to
         plugins.
         Defaults to an empty list, in which case nothing will be done.

        Paths can either be specified as absolute paths, paths relative to the
        LaTeXTools package or paths relative to the User package. Paths in the
        User package will mask paths in the LaTeXTools package. This is
        intended to emulate the behaviour of ST.

        If the default glob of *.py is unacceptable, the path can instead be
        specified as a tuple consisting of the path and the glob to use. The
        glob *must* be compatible with the Python glob module. E.g.,
        ```json
            "plugin_paths": [['latextools_plugins', '*.py3']]
        ```
        will load all .py3 files in the `latextools_plugins` subdirectory of
        the User package.

API:
    `add_plugin_path()`: can be used in a manner similar to the `plugin_paths`
    configuration option. Its required argument is the path to be search, which
    can be specified either relative to the LaTeXTools package, the User
    package or as an absolute path. In addition it takes an optional argument
    of the glob to use to identify plugin files. The main purpose is to allow
    LaTeXTools code to register a default location to load plugins from.

The Plugin Environment
======================
The plugin environment will be setup so that the directory containing the
plugin is the first entry on sys.path, enabling import of any modules located
in the same folder, according to standard Python import rules. In addition, the
standard modules available to SublimeText are available. In addition, a small
number of modules from LaTeXTools itself can be made available.
"""
import glob as _glob
import os
import re
import sys
import threading
import traceback

from contextlib import contextmanager
from collections.abc import MutableMapping
from importlib.machinery import PathFinder, SourceFileLoader

import sublime

from .utils.logging import logger
from .utils.settings import get_setting

_MODULE_PREFIX = 'LaTeXTools.plugins.'
"""this is used to load plugins and not interfere with other modules"""

_REGISTRY = None

_REGISTERED_PATHS_TO_LOAD = []
"""
list of tuples consisting of a path and a glob to load in the plugin_loaded()
method to handle the case where `add_plugin_path` is called before this
module has been fully loaded.
"""

_REGISTERED_CLASSES_TO_LOAD = []
"""
list of tuples consisting of names and class objects to load in the
plugin_loaded() method to handle the case where a plugin is defined before
the registry has been created
"""

# -- Public API -- #

# exceptions
class LaTeXToolsPluginException(Exception):
    """
    Base class for plugin-related exceptions
    """

    pass


class NoSuchPluginException(LaTeXToolsPluginException):
    """
    Exception raised if an attempt is made to access a plugin that does not
    exist

    Intended to allow the consumer to provide the user with some more useful
    information e.g., how to properly configure a module for an extension point
    """

    pass


class InvalidPluginException(LaTeXToolsPluginException):
    """
    Exception raised if an attempt is made to register a plugin that is not a
    subclass of LaTeXToolsPlugin.
    """

    pass


class LaTeXToolsPluginMeta(type):
    '''
    Metaclass for plugins which will automatically register them with the
    plugin registry
    '''
    def __init__(cls, name, bases, attrs):
        try:
            super(LaTeXToolsPluginMeta, cls).__init__(name, bases, attrs)
        except TypeError:
            # occurs on reload
            return

        if cls == LaTeXToolsPluginMeta or cls is None:
            return

        try:
            if not any(
                (True for base in bases if issubclass(base, LaTeXToolsPlugin))
            ):
                return
        except NameError:
            return

        registered_name = _classname_to_internal_name(name)

        _REGISTERED_CLASSES_TO_LOAD.append((registered_name, cls))

        if _REGISTRY is not None:
            _REGISTRY[registered_name] = cls


LaTeXToolsPlugin = LaTeXToolsPluginMeta('LaTeXToolsPlugin', (object,), {})
'''
Base class for LaTeXTools plugins. Implementation details will depend on where
this plugin is supposed to be loaded. See the documentation for details.
'''


# methods for consumers
def add_plugin_path(path, glob="*.py"):
    """
    This function adds plugins from a specified path.

    It is primarily intended to be used by consumers to load plugins from a
    custom path without needing to access the internals. For example, consuming
    code could use this to load any default plugins

    `glob`, if specified should be a valid Python glob. See the `glob` module.
    """
    if (path, glob) not in _REGISTERED_PATHS_TO_LOAD:
        _REGISTERED_PATHS_TO_LOAD.append((path, glob))

    # if we are called before `plugin_loaded`
    if _REGISTRY is None:
        return

    previous_plugins = set(_REGISTRY.keys())

    if not os.path.exists(path):
        return

    if os.path.isfile(path):
        plugin_dir = os.path.dirname(path)
        sys.path.insert(0, plugin_dir)

        _load_plugin(os.path.basename(path), plugin_dir)

        sys.path.pop(0)
    else:
        for file in _glob.iglob(os.path.join(path, glob)):
            plugin_dir = os.path.dirname(file)
            sys.path.insert(0, plugin_dir)

            _load_plugin(os.path.basename(file), plugin_dir)

            sys.path.pop(0)

    logger.info(
        "Loaded plugins %s from path '%s'",
        list(set(_REGISTRY.keys()) - previous_plugins),
        path,
    )

def get_plugin(name):
    """
    This is intended to be the main entry-point used by consumers (not
    implementors) of plugins, to find any plugins that have registered
    themselves by name.

    If a plugin cannot be found, a NoSuchPluginException will be thrown. Please
    try to provide the user with any helpful information.

    Use case:
        Provide the user with the ability to load a plugin by a memorable name,
        e.g., in a settings file.

        For example, 'biblatex' will get the plugin named 'BibLaTeX', etc.
    """
    if _REGISTRY is None:
        raise NoSuchPluginException(
            "Could not load plugin {0} because the registry either hasn't "
            + "been loaded or has just been unloaded.".format(name)
        )
    return _REGISTRY[name]


def get_plugins_by_type(cls):
    if _REGISTRY is None:
        raise NoSuchPluginException(
            "No plugins could be loaded because the registry either hasn't "
            "been loaded or has been unloaded"
        )

    plugins = [plugin for _, plugin in _REGISTRY.items() if issubclass(plugin, cls)]

    return plugins


# -- Private API --#

# WARNING:
# imp module is deprecated in 3.x, unfortunately, importlib does not seem
# to have a stable API, as in 3.4, `find_module` is deprecated in favour of
# `find_spec` and discussions of how best to provide access to the import
# internals seem to be on-going
def _load_module(module_name, filename, *paths):
    name, ext = os.path.splitext(filename)

    if ext in (".py", ""):
        loader = PathFinder.find_module(name, path=paths)
        if loader is None:
            loader = PathFinder.find_module(name)
        if loader is None:
            raise ImportError("Could not find module {} on path {} or sys.path".format(name, paths))
    else:
        loader = None
        for path in paths:
            p = os.path.normpath(os.path.join(path, filename))
            if os.path.exists(p):
                loader = SourceFileLoader(module_name, p)

        if loader is None:
            raise ImportError("Could not find module {} on path {}".format(name, paths))

    loader.name = module_name
    return loader.load_module()


def _get_sublime_module_name(directory, module):
    return "{0}.{1}".format(os.path.basename(directory), module)


class LaTeXToolsPluginRegistry(MutableMapping):
    """
    Registry used internally to store references to plugins to be retrieved
    by plugin consumers.
    """

    def __init__(self):
        self._registry = {}

    def __getitem__(self, key):
        try:
            return self._registry[key]
        except KeyError:
            raise NoSuchPluginException(
                "Plugin {0} does not exist. Please ensure that the plugin is "
                "configured as documented".format(key)
            )

    def __setitem__(self, key, value):
        if not isinstance(value, LaTeXToolsPluginMeta):
            raise InvalidPluginException(value)

        self._registry[key] = value

    def __delitem__(self, key):
        del self._registry[key]

    def __iter__(self):
        return iter(self._registry)

    def __len__(self):
        return len(self._registry)

    def __str__(self):
        return str(self._registry)


def _classname_to_internal_name(s):
    '''
    Converts a Python class name in to an internal name

    The intention here is to mirror how ST treats *Command objects, i.e., by
    converting them from CamelCase to under_scored. Similarly, we will chop
    "Plugin" off the end of the plugin, though it isn't necessary for the class
    to be treated as a plugin.

    E.g.,
        SomeClass will become some_class
        ReferencesPlugin will become references
        BibLaTeXPlugin will become biblatex
    '''
    if not s:
        return s

    def _repl(match):
        match = match.group(0)
        return match[0] + match[1:].lower()

    s = re.sub(r'(?:Bib)?(?:La)?TeX', _repl, s)

    # pilfered from https://code.activestate.com/recipes/66009/
    s = re.sub(r'(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])', r"_\g<0>", s).lower()

    if s.endswith('_plugin'):
        s = s[:-7]

    return s


def _get_plugin_paths():
    plugin_paths = get_setting("plugin_paths", [])
    return plugin_paths


def _load_plugin(filename, *paths):
    name, ext = os.path.splitext(filename)

    # hopefully a unique-enough module name!
    if not ext or ext == ".py":
        module_name = "{0}{1}".format(_MODULE_PREFIX, name)
    else:
        module_name = "{0}{1}_{2}".format(_MODULE_PREFIX, name, ext[1:])

    if module_name in sys.modules:
        try:
            return sys.modules[module_name]
        except FileNotFoundError:
            # A previous plugin has been moved or removed, so just reload it
            pass

    try:
        return _load_module(module_name, filename, *paths)
    except Exception:
        logger.error("Could not load module %s using path %s.", name, paths)
        traceback.print_exc()

    return None


def _load_plugins():
    def _resolve_plugin_path(path):
        if not os.path.isabs(path):
            p = os.path.normpath(os.path.join(sublime.packages_path(), "User", path))
            if not os.path.exists(p):
                p = os.path.normpath(os.path.join(sublime.packages_path(), "LaTeXTools", path))
            return p
        return path

    for path in _get_plugin_paths():
        if isinstance(path, str):
            add_plugin_path(_resolve_plugin_path(path))
        else:
            try:
                # assume path is a tuple of [<path>, <glob>]
                add_plugin_path(_resolve_plugin_path(path[0]), path[1])
            except Exception:
                logger.error("An error occurred while trying to add the plugin path %s", path)
                traceback.print_exc()


# load plugins when the Sublime API is available, just in case...
def latextools_plugin_loaded():
    global _REGISTRY
    _REGISTRY = LaTeXToolsPluginRegistry()

    logger.info("Loading LaTeXTools plugins...")

    for name, cls in _REGISTERED_CLASSES_TO_LOAD:
        _REGISTRY[name] = cls

    _load_plugins()

    for path, glob in _REGISTERED_PATHS_TO_LOAD:
        add_plugin_path(path, glob)
