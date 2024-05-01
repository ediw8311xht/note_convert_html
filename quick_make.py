#!/bin/python3
import re
#from collections           import OrderedDict
from maceurtlib.MacHelpers import read_file, write_file
import handlers as hl

class Convert(object):
    handle_funcs = [
        #---------------------------------Special-------------------------------#
        hl.title_handle,        hl.latex_handle,      hl.bold_handle,   hl.italic_handle,
        #---------------------------------Table---------------------------------#
        #hl.table_begin_handle,  hl.table_end_handle,  hl.table_handle,
        hl.table_handle,
        #---------------------------------Rest----------------------------------#
        hl.header_handle,       hl.paragraph_handle,
    ]
    default_args = {
        "in_file"       : "input.md",
        "out_file"      : "output.html",
        "cdn_latex"     : "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js",
        "title"         : "Notes",
        "in_text"       : lambda s: read_file(s.in_file),
        "current_table" : None,
        "structures"    : [],
        "list_out"      : [],
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
        latex = f'<script id="MathJax-script" async src="{self.cdn_latex}"></script>'
        title = f'<title>{self.title}</title>'
        head_l = [ "<head>", '<meta charset="utf-8"/>', title, latex, '</head>' ]
        self.prep(head_l)
    def make_doc(self):
        self.prep([ '<!DOCTYPE html>', '<html>' ])
        self.appe([ '</html>' ])
    def handle_line(self, line):
        self.state = 0
        for i in self.handle_funcs:
            line, c = i(self, line)
            if c == "break": break
        self.appe([line])
    def setup_html(self):
        il = self.in_text.split("\n")
        self.prep(['<body>'])
        for i in il:
            self.handle_line(i)
        self.appe(['</body>'])
    def convert_structures(self):
        pass
    def convert_html(self, l=[]):
        self.list_out = l
        # Parse through markdown, creating body and setting options
        self.setup_html()
        # Make head of list
        self.make_head()
        # Make document
        self.make_doc()
        # Convert structures [Table] in list to strings
        self.convert_structures()
    def convert_html_file(self):
        self.convert_html()
        print(str(self))
        return write_file(self.out_file, str(self))

def main():
    pass

if __name__ == "__main__":
    a = Convert()
    print(a.convert_html())
    print(a.convert_html_file())
    #print(a.title)
