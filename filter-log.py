#!/usr/bin/env python2

import gzip, base64, binascii
import re, sys, gi
from gi.repository import GLib
import urllib2

log_pat = (r''
           '(\d+.\d+.\d+.\d+)\s-\s-\s' #source
           '\[(.+)\]\s' #datetime
           '"GET\s(.+)\s(\w+/.+)"\s' #path
           '(\d+)\s' #status
           '(\d+)\s' #size
           '"([^"]+)"\s' #referrer
           '"([^"]+)"' #user agent
)
log_re = re.compile(log_pat)

def deltaid_to_commit(deltaid):
    if deltaid:
        return binascii.hexlify(base64.b64decode(deltaid.replace("_", "/") + "=")).decode("utf-8")
    return None

refs_cache = {}

def parse_log(logname):
    if logname.endswith(".gz"):
        log_file = gzip.open(logname, 'rb')
    else:
        log_file = open(logname, 'r')

    while True:
        line = log_file.readline()
        if line == "":
            break
        l = log_re.match(line.decode("utf-8"))
        if not l:
            continue
        result = l.group(5)
        path = l.group(3)
        referer = l.group(8)
        if result == "200" and path.startswith("/repo/deltas/") and path.endswith("/superblock") and referer.startswith("ostree"):
            delta = path[len("/repo/deltas/"):-len("/superblock")].replace("/", "")
            if delta.find("-") != -1:
                source = delta[:delta.find("-")]
                target = delta[delta.find("-")+1:]
            else:
                source = None
                target = delta

            ref = None
            if target in refs_cache:
                ref = refs_cache[target]
            else:
                commit = deltaid_to_commit(target)
                url = "https://flathub.org/repo/objects/%s/%s.commit" % (commit[0:2], commit[2:])
                try:
                    response = urllib2.urlopen(url)
                    commitv = response.read()
                    if commitv:
                        v = GLib.Variant.new_from_bytes(GLib.VariantType.new("(a{sv}aya(say)sstayay)"), GLib.Bytes.new(commitv), False)
                        if "xa.ref" in v[0]:
                            ref = v[0]["xa.ref"]
                except:
                    pass
                refs_cache[target] = ref
            if ref:
                print('%s\t%s\t%s\t%s' % (l.group(1), l.group(2), ref, l.group(8)))

for logname in sys.argv[1:]:
    parse_log(logname)
