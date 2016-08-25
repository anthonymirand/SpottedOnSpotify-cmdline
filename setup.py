# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""


import re
from setuptools import setup

with open('./etc/version.txt', 'r') as ver:
    VERSION = ver.read().splitlines()

setup(
    name = "spotted-on-spotify",
    version = VERSION[0],
    description = "Youtube/SoundCloud to Spotify python command line application.",
    long_description = open("README.md").read(),
    url = "http://www.github.com/anthonymirand/SpottedOnSpotify",
    author = "Anthony Mirand",
    author_email = "anthonypmirand@gmail.com",
    license = "MIT",
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",

        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"
    ],
    keywords = "spotify youtube soundcloud",

    install_requires = [
        # AudioJack dependencies
        'ffmpeg-normalize',
        'mutagen',
        'musicbrainzngs',
        'youtube_dl',

        # Spotted on Spotify dependencies
        'spotipy',
        'clint',
        'colorama',
        'termcolor',
        'pyfiglet'
    ],
    packages = [ 'spotted_on_spotify', 'etc' ],
    entry_points = {
        "console_scripts": ['spotted-on-spotify = spotted_on_spotify.spotted_on_spotify:main']
        }
    )
