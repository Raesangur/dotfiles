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
from backend.menu import Menu

from backend.distribution import Distribution
from backend.shell import Shells

import argparse
args = None




def main():
    distro = handle_distribution()
    installer = Installer(distro)
    
    handle_shell(installer)

def handle_distribution():
    distro = Distribution()
    if args.verbose:
        print("{} Linux detected".format(distro.get_name().title()))
    return distro

def handle_shell(installer: Installer):
    shells = Shells()

    # Ask for a shell selection
    shellMenu = Menu("Shell Selection", shells.get_available(), skippable=True)
    shell = shellMenu.answer()
    if shell == "skip":
        return
    shell = shells.get_selected(shell)

    # Install specified shell
    installer.install(shell, quiet=args.quiet)

    # Create symbolic links to configuraition
    installer.create_links(shell, verbose=args.verbose)
    

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

