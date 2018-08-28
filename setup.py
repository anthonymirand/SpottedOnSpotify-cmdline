# -*- coding: utf-8 -*-

'''setup.py: setuptools control.'''

from setuptools import setup
from spotted_on_spotify import conf

setup(
  name='spotted-on-spotify',
  version=conf.VERSION,
  description='Youtube/SoundCloud to Spotify python command line application.',
  long_description=open('README.md').read(),
  url='https://github.com/anthonymirand/SpottedOnSpotify-cmdline',
  author='Anthony Mirand',
  author_email='anthonypmirand@gmail.com',
  license='MIT',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Multimedia :: Sound/Audio :: Analysis',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
  ],
  keywords='spotify youtube soundcloud audio fingerprint',
  install_requires=[
    'ffmpeg-normalize',
    'youtube_dl',
    'pyacoustid',
    'spotipy',
    'clint',
    'audioread',
  ],
  packages=['spotted_on_spotify'],
  entry_points={
    'console_scripts': ['spotted-on-spotify = spotted_on_spotify.app:main'],
  },
  include_package_data=True
)
