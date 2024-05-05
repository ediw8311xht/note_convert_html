#!/bin/python3
import re
from qmake_table import Table

def ignore_handle(_self, s):
    return ( s, "continue")
def title_handle(self, s):
    match = re.search(r'title:[ ]*(?P<title>.*)', s, re.IGNORECASE)
    if match != None:
        self.title = match.group("title")
        return ( None, "break" )
    else:
        return ( s, "continue" )
def latex_handle(_self, s):
    callback = lambda x: f'<span class="math inline">\({ x.group("latex") }\)</span>'
    match = re.sub( r'[$](?P<latex>[^$]*)[$]', callback, s)
    return ( match, "continue" )
def bold_handle(self, s):
    tag = "<b>" if not self.states["bold"] else "</b>"
    match = s.replace( '**', tag, 1)
    if match != s:
        self.states["bold"] = not self.states["bold"]
        return bold_handle(self, match)
    else:
        return ( match, "continue" )
def italic_handle(self, s):
    tag = "<i>" if not self.states["italic"] else "</i>"
    match = s.replace( '*', tag, 1)
    if match != s:
        self.states["italic"] = not self.states["italic"]
        return italic_handle(self, match)
    else:
        return ( match, "continue" )
#def table_begin_handle(_self, s):

def table_handle(self, s):
    if not (gg := Table.is_table(s)):
        self.states["table"] = False
        return (s, "continue")
    elif self.states["table"] == False:
        self.states["table"] = Table(s)
        #print(self.states["table"])
        return (self.states["table"], "break")
    else:
        #print("HERE", s)
        self.states["table"].next_line(s)
        return (None, "break")

def header_handle(_self, s):
    def callback(x):
        n = len(x.group("header"))
        return f'<h{ n }>{ x.group("contents") }</h{ n }>'
    match = re.subn( r'^(?P<header>[#]{1,5})[ ](?P<contents>.*)$', callback, s)
    return (match[0], "break") if match[1] > 0 else (match[0], "continue")

def paragraph_handle(_self, s):
    return ("<p>" + s + "</p>", "break")


if __name__ == "__main__":
    g = "| asdfa | kdjfkj | kasdfadf |"
    print(Table.table_find(g))
    #print(latex_handle("", "help: $3+3$ out"))
    #print(italic_handle("", "**asdf**asdfadf**asdfadf**"))

