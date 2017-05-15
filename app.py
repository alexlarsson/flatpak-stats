#!/usr/bin/env python3

import stats
import sys

s = stats.FlatpakStats()

for logname in sys.argv[2:]:
    s.parse_log(logname)

all=[]
for ref in s.refs:
    parts = ref.split("/")
    print (parts[1])
    print (sys.argv[1])
    if parts[1] == sys.argv[1]:
        all = all + s.refs[ref]

for i in all:
    req = i[3]
    print("{}\t{}\t{}".format(req[0], req[1], req[6]))
