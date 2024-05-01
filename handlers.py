#!/bin/python3
import re
#from collections import OrderedDict
class Table(object):
    table_reg   = re.compile(r'[ ]*[|](?P<table_element>[^|]+)([|][ ]*$)?')
    head_reg    = re.compile(r'^[ ]*([|][ ][-]+[ ][|]?)+$')
    detect_reg  = re.compile(r'^[ ]*[|].*[|].*[|][ ]*$')

    @classmethod
    def table_find(cls, s):
        match = re.finditer(cls.table_reg, s)
        l = [x.group("table_element").strip(" ") for x in match]
        return l if len(l) > 0 else None

    @classmethod
    def is_table(cls, s):
        return re.fullmatch(cls.detect_reg, s) != None

    def __init__(self, s="", l=[]):
        self.last = None
        self.table_contents = l
        self.handle_lines(s)
    def to_html(self, l):
        beg, end = ("<th>", "</th>") if l["type"] == "head" else ("<td>", "</td>")
        out = ["<tr>"]
        out += [ f'{beg}{x}{end}' for x in l["fields"] ]
        out += ["</tr>"]
        return out

    def convert(self):
        l = ["<table>"]
        for i in self.table_contents:
            print("-----------", i)
            l += self.to_html(i)
        l += ["</table>"]
        return l
    def handle_lines(self, s):
        for i in s.split("\n"):
            if self.next_line(i) == None:
                return None
        return True
    def check_head(self, s):
        if re.fullmatch(self.head_reg, s) != None and len(self.table_contents) >= 1:
            self.table_contents[-1]["type"] = "head"
            return True
        return None
    def next_line(self, s):
        if self.check_head(s) != None:
            return True
        elif (match := self.table_find(s)):
            self.table_contents.append({"type": "body", "fields": match})
            return True
        return None
        #out =  ["<th>" + x + "</th>" for x in self.head]
        #out += ["<th>" + x + "</th>" for x in self.head]
def ignore_handle(self, s):
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
def bold_handle(_self, s):
    callback = lambda x: f'<b>{ x.group("bold") }</b>'
    match = re.sub( r'[*][*](?P<bold>.*?)[*][*]', callback, s)
    return ( match, "continue" )
def italic_handle(_self, s):
    callback = lambda x: f'<i>{ x.group("italic") }</i>'
    match = re.sub( r'[*](?P<italic>[^*]*)[*]', callback, s)
    return ( match, "continue" )
#def table_begin_handle(_self, s):

def table_handle(self, s):
    if not (gg := Table.is_table(s)):
        self.table = None
        return (s, "continue")
    elif self.table == None:
        self.table = Table(s)
        return (self.table, "break")
    else:
        print("HERE", s)
        self.table.next_line(s)
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

