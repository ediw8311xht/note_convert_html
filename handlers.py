#!/bin/python3
import re
from collections import OrderedDict

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

def header_handle(_self, s):
    def callback(x):
        n = len(x.group("header"))
        return f'<h{ n }>{ x.group("contents") }</h{ n }>'

    match = re.sub( r'^(?P<header>[#]{1,5})[ ](?P<contents>.*)$', callback, s)
    return ( match, "continue" )
    
#def table_handle(_self, s):



if __name__ == "__main__":
    print(latex_handle("", "help: $3+3$ out"))
    print(italic_handle("", "**asdf**asdfadf**asdfadf**"))

