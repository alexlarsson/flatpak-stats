#!/usr/bin/env python3

import stats
import sys
import pickle

if len(sys.argv) > 2:
    filename = sys.argv[2]
else:
    filename = "refs.db"

refs_db = open(filename, "rb")
refs = pickle.load(refs_db)

all=[]
for ref in refs:
    parts = ref.split("/")
    if parts[1] == sys.argv[1]:
        all = all + refs[ref]

for i in all:
    req = i[3]
    print("{}\t{}\t{}".format(req[0], req[1], req[6]))
