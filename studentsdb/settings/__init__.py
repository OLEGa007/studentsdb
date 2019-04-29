# -*- coding: utf-8 -*-

from .base import *

try:
    from .local import *
except ImportError:
    print('Can\'t find file settings.local! Make it from local.py.skeleton')
