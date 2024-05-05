#!/bin/python3
import re
from qmake_table import Table

def tag_replace(self, s, find, replace, state):
    s_find =    find[0] if not self.states[state] else    find[1]
    s_repl = replace[0] if not self.states[state] else replace[1]
    if (match := re.search(s_find, s)) != None:
        span = match.span()
        self.states[state] = not self.states[state]
        return s[:span[0]] + s_repl + tag_replace(self, s[span[1]:], find, replace, state)
    else:
        return s

def title_handle(self, s):
    match = re.search(r'title:[ ]*(?P<title>.*)', s, re.IGNORECASE)
    if match != None:
        self.title = match.group("title")
        return ( None, "break" )
    else:
        return ( s, "continue" )

def latex_handle(self, s):
    subbed = tag_replace(self, s, *self.state_tags["latex"], "latex")
    return (subbed, "continue") if not self.states["latex"] else (subbed, "break")

def bold_handle(self, s):
    subbed = tag_replace(self, s, *self.state_tags["bold"], "bold")
    return (subbed, "continue")

def italic_handle(self, s):
    subbed = tag_replace(self, s, *self.state_tags["italic"], "italic")
    return (subbed, "continue")

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

def paragraph_handle(self, s):
    subbed = tag_replace(self, s, *self.state_tags["paragraph"], "paragraph")
    return (subbed, "continue")


if __name__ == "__main__":
    from quick_make import Convert
    a = Convert()
    g = 'Hello *italic* and this is **bold**. This **bold** and this is ***bold italic***.'
    g = 'Hello italic and this is bold. This bold and this is bold italic.'
    print(bold_handle(a, g))

    #g = "| asdfa | kdjfkj | kasdfadf |"
    #print(Table.table_find(g))
    #print(latex_handle("", "help: $3+3$ out"))
    #print(italic_handle("", "**asdf**asdfadf**asdfadf**"))

