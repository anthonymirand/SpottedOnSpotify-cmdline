#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
spotted_on_spotify.__init__:
  used to setup environment variables to use the spotipy module.
'''

import sys, os

try:
  'FPCALC' in os.environ
except KeyError:
  from clint.textui import puts, colored
  puts(colored.yellow("Please set the environment variable FPCALC"))
  sys.exit(1)
