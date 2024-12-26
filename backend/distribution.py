# #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Distribution-related utilities
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
import distro

from backend.reader import jsonReader
from backend.menu import Menu

class Distribution:
    def __init__(self):
        supportedDistros = jsonReader("distributions.json")["distributions"]

        distroId = distro.like() if distro.like() != "" else distro.id()
        self.distribution = self.get_distribution(supportedDistros, distroId)
         

    def get_distribution(self, supportedDistros: list, distroId: str):
        distribution = None
        for dist in supportedDistros:
            if dist.get("name", "") == distroId:
                distribution = dist
                break

        if distribution == None:
            print("Current distribution is not supported")
            print("Please select one from the list:")
            distroMenu = Menu("Distribution Selection", [dist.get("name", "") for dist in supportedDistros])
            distroSelected = distroMenu.answer()
            return self.get_distribution(supportedDistros, distroSelected)
        else:
            return distribution

    
    def get_name(self):
        return self.distribution["name"]

    def get_package_manager(self):
        return self.distribution["package manager"]

    def get_install_flag(self):
        return self.distribution.get("install flag", "")

    def get_quiet_flag(self):
        return self.distribution.get("quiet flag", "")

    def get_extra_flags(self):
        return self.distribution.get("extra flags", [])
