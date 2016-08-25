#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""spotted_on_spotify.__init__: used to setup environment variables to use the spotipy module."""


import os

with open('./etc/environment.txt', 'r') as env:
    info = env.read().splitlines()

if len(info) == 3:
    os.environ['SPOTIPY_CLIENT_ID']     = str(info[0])
    os.environ['SPOTIPY_CLIENT_SECRET'] = str(info[1])
    os.environ['SPOTIPY_REDIRECT_URI']  = str(info[2])
