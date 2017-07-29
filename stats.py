#!/usr/bin/env python3

import re, sys, gi
gi.require_version('OSTree', '1.0')
from gi.repository import GLib, Gio, OSTree

verbose = False

class FlatpakStats:
    def __init__(self):
        self.commits = {}
        self.roots = {}
        self.refs = {}
        self.lines = []
        self.repo = OSTree.Repo.new(Gio.File.new_for_path("mirror"))
        self.repo.open(None)

        _,all_refs = self.repo.list_refs()
        for ref in sorted(all_refs):
            self.parse_ref (ref, all_refs[ref])

    def parse_ref (self, ref, commit):
        if commit in self.commits:
            print ("Warning, multiple refs for commit " + commit)
        self.commits[commit] = ref
        try:
            _,v,_ = self.repo.load_commit(commit)
            root = OSTree.checksum_from_bytes_v(v.get_child_value(6))
            if root in self.roots and self.roots[root] != ref and verbose:
                print ("Warning, multiple refs has root " + root + " (" + ref + ")")
            self.roots[root] = (ref, commit)
            parent = OSTree.commit_get_parent(v)
            if parent:
                self.parse_ref (ref, parent)
        except:
            pass

    def lookupCommit(self,commit):
        if commit in self.commits:
            return self.commits[commit]
        try:
            res = self.repo.load_commit(commit)
        except:
            return None
        metadata = res[1][0]
        if not "xa.ref" in metadata:
            return None
        ref = metadata["xa.ref"]
        self.commits[commit] = ref;
        return ref;

    def get_log_requests(self, f):
        log_line = f.read()
        pat = (r''
               '(\d+.\d+.\d+.\d+)\s-\s-\s' #source
               '\[(.+)\]\s' #datetime
               '"GET\s(.+)\s\w+/.+"\s' #path
               '(\d+)\s' #status
               '(\d+)\s' #size
               '"([^"]+)"\s' #referrer
               '"([^"]+)"' #user agent
        )
        return re.findall(pat, log_line)

    def parse_log_line(self, line):
        file = line[2]
        if line[3] != "200":
            return None

        if not file.startswith("/repo/") or file.startswith("/repo/summary") or file.startswith("/repo/config"):
            return None

        if file.startswith("/repo/deltas/") and file.endswith("/superblock"):
            delta = file[len("/repo/deltas/"):-len("/superblock")].replace("/", "")
            if delta.find("-") != -1:
                source = delta[:delta.find("-")]
                target = delta[delta.find("-")+1:]
            else:
                source = None
                target = delta
            commit = OSTree.checksum_from_bytes(OSTree.checksum_b64_to_bytes(target))
            ref = self.lookupCommit(commit)
            if ref == None:
                return None
        elif file.startswith("/repo/objects/") and file.endswith(".dirtree"):
            dirtree = file[len("/repo/objects/"):-len(".dirtree")].replace("/", "")
            source = None
            if dirtree in self.roots:
                ref, commit = self.roots[dirtree]
            else:
                return None
        else:
            return None

        return (ref, commit, source, line)

    def parse_log(self, logname):
        log_file = open(logname, 'r')
        requests = self.get_log_requests(log_file)
        for req in requests:
            t = self.parse_log_line (req)
            if t:
                self.lines.append(t)
                ref = t[0]
                if not ref in self.refs:
                    self.refs[ref] = []
                self.refs[ref].append(t)
