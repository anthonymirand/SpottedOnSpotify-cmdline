#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""spotted_on_spotify.__init__: used to setup environment variables to use the spotipy module."""


import os
import conf

os.environ['SPOTIPY_CLIENT_ID']     = conf.SPOTIPY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = conf.SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI']  = conf.SPOTIPY_REDIRECT_URI

with open('./etc/FPCALC', 'r') as fpcalc:
    os.environ['FPCALC'] = fpcalc.name
