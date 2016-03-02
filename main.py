#!/usr/bin/env python
import argparse
import glob
import importlib
import os
import re
import sys


class Hit(object):
    def __init__(self, path, description):
        self.path = path
        self.description = description


class Rule(object):
    def check(self):
        raise NotImplementedError()


class FilesExist(Rule):
    def __init__(self, glob, description):
        self.glob = glob
        self.description = description

    def check(self):
        for filename in glob.glob(os.path.expanduser(self.glob)):
            if os.path.exists(os.path.expanduser(filename)):
                yield Hit(filename, self.description)


class FilesContain(Rule):
    def __init__(self, glob, regex, description):
        self.glob = glob
        self.regex = regex
        self.description = description

    def check(self):
        for filename in glob.glob(os.path.expanduser(self.glob)):
            if not os.path.isfile(filename):
                continue
            with open(filename, 'r') as f:
                if re.search(self.regex, f.read()):
                    yield Hit(filename, self.description)


class Reporter(object):
    def __init__(self):
        self.items = []

    def add_rules(self, items):
        for item in items:
            assert isinstance(item, Rule)
            self.items.append(item)
        return self

    def check(self):
        for item in self.items:
            for hit in item.check():
                yield hit

    def report(self, quiet):
        if quiet:
            for hit in self.check():
                print hit.path
        else:
            hits = list(self.check())
            max_path_len = max(len(hit.path) for hit in hits)
            max_description_len = max(len(hit.description) for hit in hits)
            for hit in hits:
                print "%s%s in %s" % (" " * (max_description_len - len(hit.description)), hit.description, hit.path)


class Builder(object):
    FilesContain = FilesContain
    FilesExist = FilesExist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find files on your machine containing authentication credentials. A good start for any .gitignore file.")
    parser.add_argument("--quiet", "-q", help="Print only filenames, not the kind of credentials they contain.",
                        action="store_true")
    parser.add_argument("--rules-module", "-r", help="A python module containing the rules to check.",
                        action="store", default="default_rules")
    args = parser.parse_args()

    rules_module = importlib.import_module(args.rules_module, package=None)
    rules = rules_module.rules(Builder)
    Reporter().add_rules(rules).report(args.quiet)
