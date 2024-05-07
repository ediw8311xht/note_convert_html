#!/bin/python3
import re

class HtmlTable(object):
    table_reg   = re.compile(r'[ ]*[|](?P<table_element>[^|]+)([|][ ]*$)?')
    head_reg    = re.compile(r'[ ]*[|]([ ]*[-]+[ ]*[|])*$')
    detect_reg  = re.compile(r'^[ ]*[|].*[|].*[|][ ]*$')

    @classmethod
    def table_find(cls, s):
        match = re.finditer(cls.table_reg, s)
        l = [x.group("table_element").strip(" ") for x in match]
        return l if len(l) > 0 else None

    @classmethod
    def is_table(cls, s):
        return re.fullmatch(cls.detect_reg, s) != None

    def __init__(self, s=""):
        self.last = None
        self.table_contents = []
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
