#!/bin/python3
import os

def read_file(file):
    if not os.path.isfile(file): return False
    with open(file, 'r') as f:
        file_contents = f.read()
    if not f.closed: raise Exception('file still open')
    return file_contents

def write_file(file, string, t="w"):
    if t not in {'a', 'w', 'x'}: raise ValueError("Passed incorrect type for t")
    if not os.path.isfile(file): return False
    with open(file, t) as f:
        f.write(string)
    if not f.closed: raise Exception('file still open')
    return file
