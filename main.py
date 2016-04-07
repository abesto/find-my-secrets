#!/usr/bin/env python
import argparse
import glob
import importlib
import os
import re
import sys
import subprocess


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


class Find(Rule):
    def __init__(self, path, filename_patterns, description):
        self.path = path
        self.filename_patterns = filename_patterns
        self.description = description

    def _inames_or(self):
        it = iter(self.filename_patterns)
        yield '-iname'
        yield next(it)
        for item in it:
            yield '-or'
            yield '-iname'
            yield item

    def check(self):
        argv = ['find', os.path.expanduser(self.path)] + list(self._inames_or())
        print ' '.join(argv)
        find = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = find.communicate()

        if find.returncode == 0:
            for line in [line.strip() for line in stdout.split('\n') if line]:
                yield Hit(line, self.description)
        else:
            raise Exception('exec failed: ' + str(argv))


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


class Grep(Rule):
    def __init__(self, path, regex, description):
        self.path = path
        self.regex = regex
        self.description = description

    def _binary(self):
        for candidate in ['ag', 'ack', 'grep']:
            if os.path.isfile(candidate):
                return candidate

    def check(self):
        argv = [self._binary(), self.regex, '-l', '-r', os.path.expanduser(self.path)]
        print ' '.join(argv)
        find = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = find.communicate()

        for line in [line.strip() for line in stdout.split('\n') if line]:
            yield Hit(line, self.description)



class FastReporter(object):
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

    def report(self):
        for hit in self.check():
            print hit.path


class FancyReporter(FastReporter):
    def __init__(self):
        self.items = []
        self.quiet = False

    def add_rules(self, items):
        for item in items:
            assert isinstance(item, Rule)
            self.items.append(item)
        return self

    def check(self):
        for item in self.items:
            for hit in item.check():
                yield hit

    def report(self):
        if self.quiet:
            super(FancyReporter, self).report()
        else:
            hits = list(self.check())
            max_path_len = max(len(hit.path) for hit in hits)
            max_description_len = max(len(hit.description) for hit in hits)
            for hit in hits:
                print "%s%s in %s" % (" " * (max_description_len - len(hit.description)), hit.description, hit.path)


class Builder(object):
    FilesContain = FilesContain
    FilesExist = FilesExist
    Find = Find
    Grep = Grep

    FancyReporter = FancyReporter
    FastReporter = FastReporter

    def __init__(self):
        self.reporter = FancyReporter


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find files on your machine containing authentication credentials. A good start for any .gitignore file.")
    parser.add_argument("--quiet", "-q", help="Print only filenames, not the kind of credentials they contain.",
                        action="store_true")
    parser.add_argument("--rules-module", "-r", help="A python module containing the rules to check.",
                        action="store", default="default_rules")
    args = parser.parse_args()

    builder = Builder()

    rules_module = importlib.import_module(args.rules_module, package=None)
    rules = rules_module.rules(builder)

    reporter = builder.reporter()
    reporter.quiet = args.quiet
    reporter.add_rules(rules).report()
