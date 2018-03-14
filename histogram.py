#!/usr/bin/env python3

import argparse
import time
import stats
import sys
import pickle
import datetime
import gzip

parser = argparse.ArgumentParser(description='Print a histograme.')
parser.add_argument('--from-date', metavar='DATE')
parser.add_argument('--to-date', metavar='DATE')
parser.add_argument('file', nargs='*')
args = parser.parse_args()

from_date = None
if args.from_date:
    from_date = time.mktime(time.strptime(args.from_date, '%d/%m/%Y'))
to_date = None
if args.to_date:
    to_date = time.mktime(time.strptime(args.to_date, '%d/%m/%Y')) + 24 * 60 * 60

refs = {}

def parse_log(logname):
    if logname.endswith(".gz"):
        log_file = gzip.open(logname, 'rb')
    else:
        log_file = open(logname, 'r')

    while True:
        line = log_file.readline().decode("utf8")
        if line == "":
            break

        l = line.split("\t")
        ref = l[2]

        if ref.find(".Locale/") != -1:
            continue

        if from_date or to_date:
            date = time.mktime(time.strptime(l[1], '%d/%b/%Y:%H:%M:%S %z'))
            if from_date and date < from_date:
                continue
            if to_date and date > to_date:
                continue

        if ref in refs:
            refs[ref] = refs[ref] + 1
        else:
            refs[ref] = 0

for logname in args.file:
    parse_log(logname)

for ref, count in sorted(refs.items(), reverse=True, key=lambda tuple: tuple[1]):
    print("{}\t{}".format (count, ref))
