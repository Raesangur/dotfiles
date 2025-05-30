# #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Installer script to setup a new Linux install
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

from backend.installer import Installer
from backend.menu import SelectionMenu, BoolMenu

from backend.distribution import Distribution
from backend.packages import Packages

from backend.shell import Shells
from backend.desktopenvironment import DesktopEnvironments

import argparse
import os
args = None

sshPath = os.path.abspath(os.path.expanduser(os.path.expandvars("~/.ssh/ed25519")))

def main():
    distro = handle_distribution()
    installer = Installer(distro)

    handle_packages(installer)
    ssh_installed = handle_ssh(installer)
    handle_git(installer, True)
    
    handle_shell(installer)
    handle_desktop_environment(installer)
    

def handle_distribution():
    distro = Distribution()
    if args.verbose:
        print("{} Linux detected".format(distro.get_name().title()))
    return distro


def handle_packages(installer: Installer):
    packages = Packages()

    for pkg in packages.packages:
        shouldInstall = False
        if pkg.required:
            shouldInstall = True
        else:
            confirmMenu = BoolMenu("Install package {}?".format(pkg.name))
            if confirmMenu.answer() == True:
                shouldInstall = True

        if shouldInstall:
            installer.install(pkg, quiet=True, noconfirm=True)
            installer.create_links(pkg, verbose=args.verbose)      
            

def handle_shell(installer: Installer):
    shells = Shells()

    # Ask for a shell selection
    shellMenu = SelectionMenu("Shell Selection", shells.get_available(), skippable=True)
    shell = shellMenu.answer()
    if shell == "skip":
        return
    shell = shells.get_selected(shell)

    # Install specified shell
    installer.install(shell, quiet=args.quiet)

    # Create symbolic links to configuraition
    installer.create_links(shell, verbose=args.verbose)

    # Run additionnal commands if needed
    installer.run_additionnal_commands(shell, verbose=args.verbose)

def handle_desktop_environment(installer: Installer):
    desktopEnvironments = DesktopEnvironments()

    # Ask for a shell selection
    desktopEnvironmentMenu = SelectionMenu("Desktop Environment / Window Manager Selection", desktopEnvironents.get_available(), skippable=True)
    desktopEnvironment = desktopEnvironmentMenu.answer()
    if desktopEnvironment == "skip":
        return
    desktopEnvironment = desktopEnvironments.get_selected(desktopEnvironment)

    # Install specified shell
    installer.install(desktopEnvironment, quiet=args.quiet)

    # Create symbolic links to configuraition
    installer.create_links(desktopEnvironment, verbose=args.verbose)

    # Run additionnal commands if needed
    installer.run_additionnal_commands(desktopEnvironment, verbose=args.verbose)


def handle_ssh(installer: Installer):
    confirmMenu = BoolMenu("Configure SSH key?")
    if confirmMenu.answer() == False:
        return False

    # Create SSH key
    installer.run_command("ssh-keygen -o -a 128 -t ed25519 -f {}".format(sshPath))
    return True

def handle_git(installer: Installer, creds):
    # Check if SSH was configured
    if not creds:
        if not args.quiet:
            print("SSH needs to be configured to run the git configuration")
        return
    
    confirmMenu = BoolMenu("Configure git?")
    if confirmMenu.answer() == False:
        return

    # Open browser with SSH configuration
    print("Copy the following line and press ENTER to open Github Settings in a browser")
    with open(sshPath, 'r') as file:
            print(file.read())
    input("Press ENTER to continue to https://www.github.com/settings/ssh/new")
    
    # xdg-open opens the default browser
    installer.run_command("xdg-open 'https://www.github.com/settings/ssh/new'", verbose=args.verbose, quiet=args.quiet)


    signMenu = BoolMenu("Add GPG signing?")
    if signMenu.answer() == False:
        return

    print("Don't forget to add the signing key to github!")
    installer.run_command("git config --global gpg.format ssh", verbose=args.verbose, quiet=args.quiet)
    installer.run_command("git config --global user.signingkey {}".format(sshPath), verbose=args.verbose, quiet=args.quiet)



# -----------------------------------------------    
def parse_arguments():
    global args

    parser = argparse.ArgumentParser(prog="Raesangur's Installer Script",
                                         description="Install packages and configure applications for a fresh Linux install")
    parser.add_argument("-v", "--verbose", default=False, action='store_true', help="Print additionnal debug information")
    parser.add_argument("-q", "--quiet",   default=False, action='store_true', help="Suppress most applications' outputs")

    args = parser.parse_args()

# -----------------------------------------------
if __name__ == "__main__":
    parse_arguments();
    main()

