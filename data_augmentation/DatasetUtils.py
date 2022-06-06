import pandas as pd
import os, sys
from shutil import copyfile
from copy import deepcopy

import io, tokenize, re, os

from random import randint

# https://stackoverflow.com/a/62074206/9432116
def py_cleaner(source):
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        if token_type == tokenize.COMMENT:
            pass
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    out = '\n'.join(l for l in out.splitlines() if l.strip())
    return out
def c_cleaner(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    final_string = re.sub(pattern, replacer, text)
    final_string = '\n'.join(l for l in final_string.splitlines() if l.strip())

    return final_string

def add_to_list(lst, df, idx):
    qsort = df["Quicksort"].iloc[idx]
    msort = df["Mergesort"].iloc[idx]
    ssort = df["Selectionsort"].iloc[idx]
    isort = df["Insertionsort"].iloc[idx]
    bsort = df["Bubblesort"].iloc[idx]
    lsearch = df["Linear search"].iloc[idx]
    bsearch = df["Binary Search"].iloc[idx]
    llist = df["Linked List"].iloc[idx]
    hmap = df["Hashmap"].iloc[idx]
    fname = df["Filename"].iloc[idx]
    tup = (fname, qsort, msort, ssort, isort, bsort, lsearch, bsearch, llist, hmap)
    lst.append(tup)