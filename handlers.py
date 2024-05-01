#!/bin/python3
import re
#from collections import OrderedDict
class Table(object):
    table_reg = re.compile(r'[ ]*[|][ ]+(?P<table_element>[^|]+)[ ]+([|][ ]*$)?')

    @classmethod
    def table_find(cls, s):
        match = re.finditer(cls.table_reg, s)
        return [x.group("table_element") for x in match]

    def __init__(self):
        self.head = []
        self.body = []
    def as_list(self):
        pass
    def next_line(self):
        pass
        #out =  ["<th>" + x + "</th>" for x in self.head]
        #out += ["<th>" + x + "</th>" for x in self.head]

def title_handle(self, s):
    match = re.search(r'title:[ ]*(?P<title>.*)', s, re.IGNORECASE)
    if match != None:
        self.title = match.group("title")
        return ( "", "break" )
    else:
        return ( s, "continue" )
def latex_handle(_self, s):
    callback = lambda x: '<span class="math inline">\(' + x.group("latex") + '\)</span>'
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
def table_handle(_self, s):
    match = Table.table_find(s)
    if _self.current_table != None:
        return Table.next(s)
        return (s, "continue")
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

