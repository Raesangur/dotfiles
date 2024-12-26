# #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles the installation and setup of various shell utilities
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
from backend.reader import jsonReader


class Shells:
    def __init__(self):
        self.data = jsonReader("shells.json")["shells"]
        self.shells = [Shell(sh) for sh in self.data]
        
    def get_available(self):
        return [shell.name for shell in self.shells]

    def get_selected(self, selected: str):
        for shell in self.shells:
            if shell.name == selected:
                return shell
        return None
        
class Shell:
    def __init__(self, data):
        self.data = data
        
        self.name     = self.data.get("name",     "")
        self.path     = self.data.get("path",     self.name)
        self.packages = self.data.get("packages", None)
        self.links    = self.data.get("links",    None)
