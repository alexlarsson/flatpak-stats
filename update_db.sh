#!/usr/bin/env python3

import stats
import sys
import pickle

s = stats.FlatpakStats()

for logname in sys.argv[1:]:
    s.parse_log(logname)

refs_db = open("refs.db", 'wb')
pickle.dump(s.refs, refs_db)
refs_db.close()
