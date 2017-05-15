#!/usr/bin/env python3

import stats
import sys

s = stats.FlatpakStats()

for logname in sys.argv[1:]:
    s.parse_log(logname)

all = []
for ref in s.refs:
    if ref.find(".Locale/") != -1 or ref.startswith("appstream/"):
        continue
    all.append( (len(s.refs[ref]), ref) )

for count, ref in sorted(all, reverse=True):
    print("{}\t{}".format (count, ref))
