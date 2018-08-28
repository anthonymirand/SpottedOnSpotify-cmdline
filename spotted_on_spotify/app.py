#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

'''
app.app: provides entry point main().

Python script to match tracks on YouTube or SoundCloud to their counterparts
in Spotify. Runs URL through a MusicBrainz search via
[AcoustID](https://github.com/beetbox/pyacoustid) to find the matching metadata
and adds track match to user's Spotify account under a new playlist named
'Spotted on Spotify'.
'''

import sys
import os
import re
from urllib import ContentTooShortError
import acoustid
import youtube_dl

import conf
import spotted_on_spotify
import util

def youtube_dl_download(url):
  util.print_message('Downloading mp3 from URL...')
  try:
    with youtube_dl.YoutubeDL(conf.YOUTUBE_DL_OPTS) as ydl:
      ydl.download([url])
  except:
    util.print_message('Failed to download file from {}\n'
                       'Please try again...'.format(url),
                       color='red', exit=True)

def acoustid_search():
  util.print_message('Analyzing audio fingerprint...')
  try:
    search = list(acoustid.match(conf.ACOUSTID_API_KEY,
                                 conf.YOUTUBE_DL_OPTS['outtmpl']))
  except acoustid.NoBackendError:
    util.print_message('ERROR: Chromaprint library/tool not found.',
                       color='red', exit=True)
  except acoustid.FingerprintGenerationError:
    util.print_message('ERROR: Audio fingerprint could not be calculated.',
                       color='red', exit=True)
  except acoustid.WebServiceError as exc:
    util.print_message('ERROR: Web service request failed: {}.' \
                       .format(exc.message), color='red', exit=True)
  except Exception as ecx:
    util.print_message('ERROR: {}'.format(ecx.args[1]), color='red', exit=True)
  if len(search) == 0:
    util.print_message('Failed to find a match for your track in the '
                       'MusicBrainz database.', color='red', exit=True)
  return get_first_valid_encoding(sorted(search, reverse=True))

def get_first_valid_encoding(results):
  for result in results:
    if all(_ is not None for _ in result):
      result = list(result)
      try:
        result[2] = result[2].replace(u'\u2018', u'\'') \
                             .replace(u'\u2019', u'\'') \
                             .replace(u'\u201C', u'\"') \
                             .replace(u'\u201D', u'\"')
        result[2].encode('ascii', 'ignore')
        result[3] = result[3].replace(u'\u2018', u'\'') \
                             .replace(u'\u2019', u'\'') \
                             .replace(u'\u201C', u'\"') \
                             .replace(u'\u201D', u'\"')
        result[3].encode('ascii', 'ignore')
        return result
      except UnicodeEncodeError:
        continue
  util.print_message('ERROR: There were no matches for your track with valid '
                     'ascii encodings. Could not search for your track on '
                     'Spotify.', color='red', exit=True)

def clean_artist(artist):
  return re.split(' - | : |- |: ', artist)[:2][0].split(' & ')[0]

def clean_track(track):
  return re.sub(r'\[| \[[^\]]*\]|\] ', '',
                re.sub(r'\(| \([^)]*\)|\) ', '', track))


def main():
  if len(sys.argv) == 2:
    url = sys.argv[1]
  elif len(sys.argv) > 2:
    # TODO: Reject all and prompt or quit with usage.
    error_warning('WARNING: Only using first command line argument',
                  color='yellow')

  try:
    util.display_intro()

    username = raw_input('Enter your Spotify username: ')
    spotted = spotted_on_spotify.SpottedOnSpotify(username)
    spotted.login_to_spotify()
    spotted.create_playlist()

    if 'url' not in locals():
      url = raw_input('Please enter a valid YouTube/SoundCloud URL: ')

    youtube_dl_download(url)

    result = acoustid_search()
    percentage = float(result[0]) * 100
    match_track = clean_track(str(result[2]))
    match_artist = clean_artist(str(result[3]))
    util.print_message('{:04.2f}% MATCH: {} by {}' \
                       .format(percentage, match_track, match_artist),
                       color='cyan')

    track = spotted.search_song(match_track, match_artist)
    full_title = '{0} by {1}'.format(track['name'], track['artists'][0]['name'])

    while True:
      try:
        prompt = 'Would you like to add {} to {}? (y/n): ' \
                 .format(full_title, spotted.playlist['name'])
        status = raw_input(prompt).lower()[0]
        if status == 'n':
          util.print_message('Thanks for trying! Come again.', exit=True)
          return
        elif status == 'y':
          spotted.add_song_to_playlist(track)
          return
        else:
          util.print_message('Select from either Y or N.', color='red')
      except TypeError:
        util.print_message('Enter a valid option: Y or N.', color='red')

  except KeyboardInterrupt:
    util.print_message('\nExiting Spotted on Spotify...', exit=True)


if __name__ == "__main__":
  main()

