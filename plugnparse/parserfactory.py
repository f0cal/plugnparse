import argparse

class ParserTree(object):
    _dest_prefix = 'cmd'

    def __init__(self, base=None):
        if base is None:
            base = argparse.ArgumentParser()
        self._base_parser = base
        self.subparsers = {}
        self.parsers = {}

    def _make_tuple(self, item):
        if isinstance(item, str):
            return (item, )
        return tuple(item)

    def __getitem__(self, item):
        item = self._make_tuple(item)
        if len(item) == 0:
            return self._base_parser
        if item in self.parsers:
            return self.parsers[item]
        parent_item = item[:-1]
        parent_parser = self[parent_item]
        if parent_item not in self.subparsers:
            _dest = "{}{}".format(self._dest_prefix, len(parent_item))
            self.subparsers[parent_item] = parent_parser.add_subparsers(dest=_dest)
            self.subparsers[parent_item].required = True
        if item not in self.parsers:
            self.parsers[item] = self.subparsers[parent_item].add_parser(item[-1])
        return self.parsers[item]

    def parse_args(self, *args, **dargs):
        return self._base_parser.parse_args(*args, **dargs)

class ParserFactory(object):
    def __init__(self, base=None):
        if base is None:
            base = argparse.ArgumentParser()
        self._tree = ParserTree(base)
        self._captured_parse_args = base.parse_args
        self._captured_parse_known_args = base.parse_known_args
        base.parse_args = self._parse_args
        base.parse_known_args = self._parse_known_args

    def read_annotated_class(self, cls):
        for attr in dir(cls):
            if not attr.startswith('cli_'):
                continue
            cmds = attr.replace('cli_', '').split('_')
            self._tree[cmds].set_defaults(func=attr)

    def read_package(self, package, target=None):
        scanner = venusian.Scanner(entrypoints=[], setopts=[])
        scanner.scan(package)
        for cmds, arg_factory, fn in scanner.entrypoints:
            self._tree[cmds].set_defaults(func=fn)
            arg_factory(self._tree[cmds])

    def _parse_args(self, *args, **dargs):
        return self._captured_parse_args(*args, **dargs)

    def _parse_known_args(self, *args, **dargs):
        ns, _ = self._captured_parse_known_args(*args, **dargs)
        def _run():
            if isinstance(ns.func, str):
                return getattr(ns.api, ns.func)(ns, self._tree._base_parser)
            return ns.func(ns.api, ns, self._tree._base_parser)
        setattr(ns, 'run', _run)
        return ns, _
