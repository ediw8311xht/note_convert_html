#!/bin/python3
import re
from collections           import OrderedDict
from maceurtlib.MacHelpers import read_file, write_file

import handlers as hl


class Convert(object):
    handle_funcs = [ hl.title_handle  , hl.latex_handle  , 
                     hl.bold_handle   , hl.italic_handle , 
                     hl.header_handle ,
                   ]
    default_args = {
        "in_file"   : "input.md", 
        "out_file"  : "output.html", 
        "cdn_latex" : "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js",
        "title"     : "Notes",
        "in_text"   : lambda s: read_file(s.in_file)
    }

    def __init__(self, **args):
        self.handle_args(args)
    def handle_args(self, d):
        for k, i in self.default_args.items():
            set = d[k] if k in d else i
            if callable(set):
                set = set(self)
            setattr(self, k, set)
    def handle_line(self, line):
        self.state = 0
        for i in self.handle_funcs:
            line, c = i(self, line)
            if c == "break": break
        return [line]
    def make_head(self):
        latex = f'<script id="MathJax-script" async src="{self.cdn_latex}"></script>'
        title = f'<title>{self.title}</title>'
        return [ "<head>", '<meta charset="utf-8"/>', title, latex, '</head>' ]
    def setup_html(self):
        il = self.in_text.split("\n")
        ol = ['<body>']
        #o = ["<DOCTYPE html>", ["<html>", ["<head>", "</head>"], "</html>"]]
        for i in il:
            ol += self.handle_line(i)
        return ol + ['</body>']
    def convert_html(self):
        l =  [ '<!DOCTYPE html>', '<html>' ]
        l += self.make_head()
        l += self.setup_html()
        l += [ '</html>' ]
        return "\n".join(l)
    def convert_html_file(self):
        text_out = self.convert_html()
        return write_file(self.out_file, text_out)



def main():
    pass

if __name__ == "__main__":
    a = Convert()
    print(a.convert_html())
    print(a.convert_html_file())
    #print(a.title)
