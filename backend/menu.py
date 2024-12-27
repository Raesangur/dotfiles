# #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints the user interface and handles selection of options during the installation script
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

class BoolMenu():
    def __init__(self, title: str):
        self.realMenu = SelectionMenu(title, ["true", "false"], skippable = False)

    def answer(self):
        ans = self.realMenu.answer()
        if ans == "true":
            return True
        else:
            return False
        

class SelectionMenu():
    def __init__(self, title: str, options: list, skippable = True):
        self.options = options
        self.skip = skippable
        
        self.display_options(title, options)

    def display_options(self, title: str, options: list):
        print("\n--------------------------------------------------")
        print(title.upper())
        if self.skip:
            print("0) Skip")
        
        for i in range(len(options)):
            print("{0}) {1}".format(i + 1, options[i]))

            
    def answer(self):
        ans = True
        while ans:
            ans = int(input("Please select an option "))

            if self.skip and ans == 0:
                return "skip"
            
            if ans > len(self.options) or ans == 0:
                print("Invalid answer, please try again")
                ans = True
                continue

            print("")
            return self.options[ans - 1]
            
