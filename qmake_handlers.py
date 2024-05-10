#!/bin/python3
import re
import qmake_structures as st

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

def link_handle(_self, s):
    callback = lambda x: f'<a href="{x.group("link")}">{x.group("text")}</a>'
    subbed = re.sub(r'\[(?P<text>[^\]]*)\]\((?P<link>[^)]*)\)', callback, s)
    return (subbed, "continue")

def bold_handle(self, s):
    subbed = tag_replace(self, s, *self.state_tags["bold"], "bold")
    return (subbed, "continue")

def italic_handle(self, s):
    subbed = tag_replace(self, s, *self.state_tags["italic"], "italic")
    return (subbed, "continue")

def table_handle(self, s):
    if not (gg := st.HtmlTable.is_table(s)):
        self.states["table"] = False
        return (s, "continue")
    elif self.states["table"] == False:
        self.states["table"] = st.HtmlTable(s)
        #print(self.states["table"])
        return (self.states["table"], "break")
    else:
        #print("HERE", s)
        self.states["table"].next_line(s)
        return (None, "break")

def list_handle(self, s, state, reg, start, end):
    callback = lambda x: "<li>" + x.group("list_element") + "</li>"
    match = re.sub(reg, callback, s)
    if match != s:
        match = start + match if not self.states[state] else match
        self.states[state] = True
        return (match, "continue")
    else:
        s = (end, s) if self.states[state] else s
        self.states[state] = False
        return (s, "continue")

def unordered_list_handle(self, s):
    reg = r'^-[ ](?P<list_element>.+)$'
    return list_handle(self, s, "unordered_list", reg, "<ul>", "</ul>")

def ordered_list_handle(self, s):
    reg = r'^[0-9]+[.][ ](?P<list_element>.+)$'
    return list_handle(self, s, "ordered_list", reg, "<ol>", "</ol>")

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

