"""
Installer utilities to install packages on various distros
---------------------------------------------------------------------------------------------------
:author  Pascal-Emmanuel Lachance | Raesangur <https://www.github.com/Raesangur>
         https://www.raesangur.com
:date    2024-12-25

:copyright Copyright (c) 2023 Pascal-Emmanuel Lachance | Raesangur

:license 'MIT <https://opensource.org/license/mit/>'
    This project is release under the MIT License
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software
    and associated documentation files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or
    substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
    BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
---------------------------------------------------------------------------------------------------
"""
import os
import subprocess

from backend.distribution import Distribution

class Installer:
    def __init__(self, distro: Distribution):
        self.distro = distro

    def install(self, package, quiet=False, noconfirm=False):
        packageName = package.name
        if package.packages is not None:
            for pack in package.packages:
                if self.distro.get_package_manager() in pack:
                    packageName = pack[self.distro.get_package_manager()]

        subprocess.run(["sudo",
                        self.distro.get_package_manager(),
                        self.distro.get_install_flag(),
                        packageName,
                        *([self.distro.get_quiet_flag()] if quiet else []),
                        *([self.distro.get_confirm_flag()] if noconfirm else []),
                        *(self.distro.get_extra_flags())
                        ])

    def create_links(self, package, verbose=False):
        if package.links is not None:
            for link in package.links:
                sourcePath = os.path.dirname(os.path.dirname(__file__)) + '/' + package.path + '/' +  link["source"]
                destinationPath = os.path.abspath(os.path.expanduser(os.path.expandvars(link["destination"])))
                print(sourcePath)
                print(destinationPath)
                if verbose:
                    print("Creating symbolic link from {} to {}".format(destinationPath, sourcePath))

                subprocess.run(["ln", "-s", sourcePath, destinationPath])

    def run_additionnal_commands(self, package, verbose=False):
        if package.commands is not None:
            for command in package.commands:
                cmd = command["command"]
                if verbose:
                    print(cmd)
                subprocess.run(cmd, shell=True)

    
