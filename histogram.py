#!/usr/bin/env python3

import stats
import sys
import pickle

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "refs.db"
refs_db = open(filename, "rb")
refs = pickle.load(refs_db)

all = []
for ref in refs:
    if ref.find(".Locale/") != -1 or ref.startswith("appstream/"):
        continue
    accesses = refs[ref];
    unique = {}
    for a in accesses:
        ip = a[3][0]
        unique[ip] = True
    all.append( (len(accesses), len(unique), ref) )

for count, unique, ref in sorted(all, reverse=True):
    print("{}\t{}\t{}".format (count, unique, ref))
