# -*- coding: utf-8 -*-

__author__ = 'Brian Rossa'
__email__ = 'br@f0cal.com'
__version__ = '0.0.1'

from .decorators import *
from .parserfactory import ParserFactory

def scan_and_run(package_name, base_parser=None):
    parser = base_parser or __import__('argparse').ArgumentParser()
    factory = ParserFactory(base=parser)
    factory.read_package(__import__(package_name))
    parser = factory.make_parser()
    ns = parser.parse_args()
    return ns.func(ns, parser)
