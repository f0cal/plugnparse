# -*- coding: utf-8 -*-
"""
    Setup file for plugnparse.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.2.3.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
import sys
import os

from pkg_resources import VersionConflict, require
from setuptools import setup

try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

argcomplete_activation_script = f"{os.environ['VIRTUAL_ENV']}/lib/python{sys.version_info[0]}.{sys.version_info[1]}/site-packages/plugnparse/activate-argcomplete.sh"
venv_activate = os.environ['VIRTUAL_ENV'] + '/bin/activate'

argcomplete_activation_call = f"\n\n# activates f0cal namespace tab completion \nsource {argcomplete_activation_script}"

with open(venv_activate, 'r') as f:
    if f.read().find(argcomplete_activation_call) == -1:
        with open(venv_activate, 'a') as g:
            g.write(argcomplete_activation_call)


if __name__ == "__main__":
    setup(use_pyscaffold=True,
          scripts=['src/plugnparse/activate-argcomplete.sh']
          )
