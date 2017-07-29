#!/usr/bin/env python3

import stats
import sys

s = stats.FlatpakStats()

for logname in sys.argv[1:]:
    s.parse_log(logname)

for l in s.lines:
    orig=l[3]
    if l[0].startswith("appstream"):
        continue
    if ".Locale/" in l[0]:
        continue
    print('%s - - [%s] "GET /%s HTTP/1.1" 200 1 "%s" "%s"' % (orig[0], orig[1], l[0], orig[5], orig[6]))

#  ('appstream/x86_64', 'b8a5953e0236793fd8db5b1308d914da3f8e041eb49359128e632febaf5cafbd', 'CgX7s4q1AK7MsyECcKPri1HIBMlkhX9XPubeL36T5Ks', ('83.248.85.174', '29/Jul/2017:09:43:20 +0000', '/repo/deltas/Cg/X7s4q1AK7MsyECcKPri1HIBMlkhX9XPubeL36T5Ks-uKWVPgI2eT_Y21sTCNkU2j+OBB60k1kSjmMv669cr70/superblock', '200', '4660', '-', 'ostree'))
#  83.248.85.174 - - [29/Jul/2017:09:43:20 +0000] "GET /repo/deltas/Cg/X7s4q1AK7MsyECcKPri1HIBMlkhX9XPubeL36T5Ks-uKWVPgI2eT_Y21sTCNkU2j+OBB60k1kSjmMv669cr70/superblock HTTP/1.1" 200 4660 "-" "ostree" "-"

