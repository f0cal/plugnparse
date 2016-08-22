import argparse
import venusian

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
        _parsers = self.parsers
        _subparsers = self.subparsers
        item = self._make_tuple(item)
        if len(item) == 0:
            return self._base_parser
        if item in _parsers:
            return _parsers[item]
        parent_item = item[:-1]
        parent_parser = self[parent_item]
        if parent_item not in _subparsers:
            _d = "{}{}".format(self._dest_prefix, len(parent_item))
            _subparsers[parent_item] = parent_parser.add_subparsers(dest=_d)
            _subparsers[parent_item].required = True
        if item not in _parsers:
            _parsers[item] = _subparsers[parent_item].add_parser(item[-1])
        return _parsers[item]

class ParserFactory(object):
    def __init__(self, base=None):
        if base is None:
            base = argparse.ArgumentParser()
        self._tree = ParserTree(base)
        self._captured_parse_args = base.parse_args
        self._captured_parse_known_args = base.parse_known_args
        base.parse_args = self._parse_args
        base.parse_known_args = self._parse_known_args
        self._base = base

    def read_annotated_class(self, cls):
        for attr in dir(cls):
            if not attr.startswith('cli_'):
                continue
            cmds = attr.replace('cli_', '').split('_')
            self._tree[cmds].set_defaults(func=attr)

    def read_package(self, package, require=None):
        # TODO (br) Make 'entrypoints' global
        scanner = venusian.Scanner(entrypoints=[])
        scanner.scan(package)
        for cmds, arg_factory, fn in scanner.entrypoints:
            # TODO (br) Make 'func' global
            self._tree[cmds].set_defaults(func=fn)
            arg_factory(self._tree[cmds])

    def _parse_args(self, *args, **dargs):
        return self._captured_parse_args(*args, **dargs)

    def _parse_known_args(self, *args, **dargs):
        return self._captured_parse_known_args(*args, **dargs)

    def make_parser(self):
        return self._base
