#!/bin/python3
import re
#from collections           import OrderedDict
from   qmake_helpers   import read_file, write_file
import qmake_handlers  as hl
import qmake_styles    as sl

class Convert(object):
    handle_funcs = [
        hl.ignore_handle,
        #---------------------------------Special-------------------------------#
        hl.title_handle,        hl.latex_handle,      hl.bold_handle,   hl.italic_handle,
        #---------------------------------Table---------------------------------#
        hl.table_handle,
        #---------------------------------Rest----------------------------------#
        hl.header_handle,       hl.paragraph_handle,
    ]
    default_args = {
        "in_file"       : "input.md",
        "out_file"      : "output.html",
        "charset"       : "utf-8",
        "cdn_latex"     : "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js",
        "title"         : "Notes",
        "in_text"       : lambda s: read_file(s.in_file),
        "list_out"      : [],
        "styles"        : ["test.css"],
        "states"        : {"italic": False, "bold": False, "table": False}
    }

    def __repr_(self): return "\n".join(self.list_out)
    def __str__(self): return "\n".join(self.list_out)
    def __init__(self, **args):
        self.handle_args(args)
    def handle_args(self, d):
        for k, i in self.default_args.items():
            set = d[k] if k in d else i
            if callable(set):
                set = set(self)
            setattr(self, k, set)
    def prep(self, l):      self.list_out = l + self.list_out
    def appe(self, l):      self.list_out = self.list_out + l
    def inse(self, l, p):   self.list_out = self.list_out[:p] + l + self.list_out[p + 1:]
    def make_head(self):
        style_link = lambda x: f'<link rel="stylesheet" type="text/css" href="{x}"/>'
        head_l = [
            "<head>",
            f'<meta charset="{self.charset}"/>',
            f'<title>{self.title}</title>',
            f'<script id="MathJax-script" async src="{self.cdn_latex}"></script>'
        ]
        head_l += [style_link(x) for x in self.styles]
        head_l += ["</head>"]
        self.prep(head_l)
    def make_doc(self):
        self.prep([ '<!DOCTYPE html>', '<html>' ])
        self.appe([ '</html>' ])
    def handle_line(self, line):
        for i in self.handle_funcs:
            line, c = i(self, line)
            if c == "break": break
        if line != None and line != "":
            self.appe([line])
    def reset_states(self):
        self.states = {x: False for x in self.states}
    def setup_html(self):
        self.reset_states()
        il = self.in_text.split("\n")   # Input Text handling happens line by line
        self.prep(['<body>'])
        for i in il:
            self.handle_line(i)
        self.appe(['</body>'])
    def convert_structures(self):
        for i in range(0, len(self.list_out)):
            if type(self.list_out[i]) == hl.Table:
                self.list_out[i] = "\n".join(self.list_out[i].convert())


    def convert_html(self, l=[]):
        self.list_out = l
        self.setup_html()           # Parse through markdown, creating body and setting options
        self.make_head()            # Make head of list
        self.make_doc()             # Make document
        self.convert_structures()   # Convert structures [Table] in list to strings
    def convert_html_file(self):
        self.convert_html()
        print(str(self))
        return write_file(self.out_file, str(self))

def main():
    pass

if __name__ == "__main__":
    a = Convert()
    #print(a.convert_html())
    print(a.convert_html_file())
    #print(a.title)
