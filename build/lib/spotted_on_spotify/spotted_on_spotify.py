#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
    spotted_on_spotify.spotted_on_spotify: provides entry point main().

    Python script to match YouTube and SoundCloud to their counterparts in Spotify.
    Runs URL through a MusicBrainz search via [AudioJack](https://github.com/Blue9/AudioJack)
    to find the matching metadata and adds track match to user's Spotify account under
    a new playlist named 'Spotted on Spotify'.
"""


from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format
from clint.textui import puts, colored

import audiojack

import sys, os
import spotipy
import spotipy.util as util

with open('./etc/version.txt', 'r') as ver:
    VERSION = ver.read().splitlines()

audiojack.set_useragent("Spotted on Spotify", VERSION)
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
SPOTIPY_SCOPE = "playlist-modify-public"


class SpottedOnSpotify:

    def __init__(self):
        self.username = None
        self.sp = None
        self.playlist = None

    def loginToSpotify(self):
        while True:
            username = raw_input("Enter your Spotify username: ")
            token = util.prompt_for_user_token(username, SPOTIPY_SCOPE)
            if token:
                self.username = username
                self.sp = spotipy.Spotify(auth=token)
                break
            else:
                puts(colored.red("Cannot get token for {0}".format(username)))
                puts(colored.red("Please try again..."))

    def createPlaylist(self):
        ''' Attempts to create custom playlist if it doesn't already exist. '''
        playlists = self.sp.user_playlists(self.username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == self.username:
                if playlist['name'] == "Spotted on Spotify":
                    self.playlist = playlist
                    break
        else:
            print "Creating 'Spotted on Spotify' playlist..."
            while True:
                playlist = self.sp.user_playlist_create(self.username, "Spotted on Spotify")
                if playlist['name'] == "Spotted on Spotify":
                    self.playlist = playlist
                    print "Completed creating playlist..."
                    break
                else:
                    self.sp.user_playlist_delete(self.username, playlist['name'])

    def searchSong(self, artist, track, album):
        ''' Search and loop through each track. '''
        track_results = self.sp.search(q='track:' + track, type='track')
        tracks = track_results['tracks']['items']

        if len(tracks) > 0:
            best_result = None
            for item in tracks:
                ''' Find artist match (and album match if possible). '''
                temp_track = str(item['name'].lower())
                temp_artist = str(item['artists'][0]['name'].lower())
                if temp_track == track and temp_artist == artist:
                    if best_result is None:
                        best_result = item
                    elif str(item['album']).lower() == album:
                        best_result = item
                    elif best_result['popularity'] < item['popularity']:
                        best_result = item

        if best_result is not None:
            return (best_result, True)
        else:
            return (None, False)

    def addSongToPlaylist(self, track):
        print "Adding {0} by {1} to {2}...".format(track['name'], track['artists'][0]['name'], self.playlist['name'])
        self.sp.user_playlist_add_tracks(self.username, self.playlist['id'], [track['uri']])
        print "Success!"
    

def displayIntro():
    print 
    cprint(figlet_format("( SPOT ) IFY", font="standard"), "green")
    puts(colored.green("          Welcome to Spotted on Spotify!\n"))

def warning():
    puts(colored.yellow("ALERT: Continuing allows this program to access your public "))
    puts(colored.yellow("       playlists and create/modify a new playlist."))

    while True:
        try:
            progress = raw_input("Would you like to continue? (y/n): ")
            if progress[0].lower() == 'n':
                print "Thanks! Come again."
                sys.exit()
            elif progress[0].lower() == 'y':
                print "Continuing..."
                break
            else:
                puts(colored.red("Select from either Y or N."))
        except TypeError:
            puts(colored.red("Enter a valid option: Y or N."))

# TODO: fix sanitizing parameter list for ASCII/Unicode
# TODO: only list tracks that are available on Spotify
def narrowSearch(results):
    ''' Reduces results from MusicBrainz search to search Spotify. '''
    if len(results) == 1:
        return results[0]

    index = 0
    selected_track = None
    valid_results = []

    print
    while True:
        print " %s %30.30s | %s" % ("INDEX", "ARTIST", "TRACK")
        for item in results:
            try:
                item[0].decode('ascii')
                item[1].decode('ascii')
            except UnicodeEncodeError:
                continue
            else:
                print "   %d %32.32s | %s" % (index, item[0], item[1])
                valid_results.append(item)
                index += 1
        else:
            index = 0

        try:
            selection = raw_input("Please enter the matching index of your song: ")
            if int(selection) < 0 or len(results) <= int(selection):
                error = "Enter a valid index: 0 - %d." % len(results) - 1
                puts(colored.red(error))
                continue
        except (TypeError, ValueError):
            error = "Enter a valid integer index: 0 - %d." % len(results) - 1
            puts(colored.red(error))
        else:
            selected_track = valid_results[int(selection)]
            break

    return selected_track

def main():
    try:
        init()
        displayIntro()

        spotted = SpottedOnSpotify()
        spotted.loginToSpotify()

        warning()

        spotted.createPlaylist()

        url = raw_input("Please enter a valid YouTube/SoundCloud URL: ")
        print "Finding matches..."

        results = audiojack.get_results(url)
        hit = narrowSearch(results)

        track, found_match = spotted.searchSong(hit[0].lower(), hit[1].lower(), hit[2].lower())
        if found_match:
            spotted.addSongToPlaylist(track)
        else:
            error = "Failed to find a match for %s by %s on Spotify" % (hit[1], hit[0])
            puts(colored.red(error))

    except KeyboardInterrupt:
        print "\nExiting Spotted on Spotify..."
        sys.exit(1)

if __name__ == "__main__":
    main()
    