# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""


from setuptools import setup

with open('./etc/version.txt', 'r') as ver:
    VERSION = ver.read().splitlines()

setup(
    name = "spotted-on-spotify",
    version = VERSION[0],
    description = "Youtube/SoundCloud to Spotify python command line application.",
    long_description = open("README.md").read(),
    url = "https://github.com/anthonymirand/SpottedOnSpotify-cmdline",
    author = "Anthony Mirand",
    author_email = "anthonypmirand@gmail.com",
    license = "MIT",
    classifiers = [
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"
    ],
    keywords = "spotify youtube soundcloud audio fingerprints",

    install_requires = [
        'ffmpeg-normalize',
        'youtube_dl',
        'pyacoustid',
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
