#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
    spotted_on_spotify.spotted_on_spotify: provides entry point main().

    Python script to match YouTube and SoundCloud to their counterparts in Spotify.
    Runs URL through a MusicBrainz search via [AcoustID](https://github.com/beetbox/pyacoustid)
    to find the matching metadata and adds track match to user's Spotify account under
    a new playlist named 'Spotted on Spotify'.
"""

import sys, os, re
from urllib import ContentTooShortError

# Visuals
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format
from clint.textui import puts, colored

# Audio Work
import acoustid
import youtube_dl
import spotipy
import spotipy.util as util

import conf
VERSION = conf.VERSION

init(strip=not sys.stdout.isatty())
ACOUSTID_API_KEY = conf.ACOUSTID_API_KEY
SPOTIPY_SCOPE = "playlist-modify-public"

YOUTUBE_DL_OPTS = {
    'format': 'bestaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256'
    }],
    'quiet': True,
    'no_warnings': True
}


class SpottedOnSpotify:
    def __init__(self):
        self.username = None
        self.sp = None
        self.playlist = None

    def loginToSpotify(self):
        while True:
            try:
                username = raw_input("Enter your Spotify username: ")
                token = util.prompt_for_user_token(username, SPOTIPY_SCOPE)
                if token:
                    self.username = username
                    self.sp = spotipy.Spotify(auth=token)
                    break
                else:
                    errorWarning("Cannot get token for {0}".format(username), color="red")
                    errorExit("Please try again...", color="red")
            except spotipy.client.SpotifyException as exc:
                message = exc.msg.split(":\n ", 1)[1].encode('ascii', 'ignore')
                errorExit("ERROR: Spotify service request failed: {0}".format(message), color="red")

    def createPlaylist(self):
        ''' Attempts to create custom playlist if it doesn't already exist. '''
        try:
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
        except spotipy.client.SpotifyException as exc:
            message = exc.msg.split(":\n ", 1)[1].encode('ascii', 'ignore')
            errorExit("ERROR: Spotify service request failed: {0}".format(message), color="red")

    def searchSong(self, artist, track, file):
        ''' Search and loop through each track. '''
        try:
            track_results = self.sp.search(q='track:' + '\"'+track+'\"', type='track')
            tracks = track_results['tracks']['items']
            
            best_result = None
            if len(tracks) > 0:
                for item in tracks:
                    ''' Find artist match '''
                    try:
                        # convert track and artist smart quotes to regular quotes
                        search_track = str(item['name'])
                        search_track = search_track.replace(u'\u2018', u"'").replace(u'\u2019', u"'")
                        search_track = search_track.replace(u'\u201C', u'"').replace(u'\u201D', u'"')
                        search_track.encode('ascii')

                        search_artist = str(item['artists'][0]['name'])
                        search_artist = search_artist.replace(u'\u2018', u"'").replace(u'\u2019', u"'")
                        search_artist = search_artist.replace(u'\u201C', u'"').replace(u'\u201D', u'"')
                        search_artist.encode('ascii')
                    except UnicodeEncodeError:
                        continue

                    if track in search_track.lower() and artist in search_artist.lower():
                        if best_result is None:
                            best_result = item
                        elif best_result['popularity'] < item['popularity']:
                            best_result = item

        except spotipy.client.SpotifyException as exc:
            message = exc.msg.split(":\n ", 1)[1].encode('ascii', 'ignore')
            errorExit("ERROR: Spotify service request failed: {0}".format(message), file=file, color="red")

        if best_result is not None:
            return (best_result, True)
        else:
            return (None, False)


    def addSongToPlaylist(self, track, file):
        try:
            print "Adding track to {0}...".format(self.playlist['name'])
            self.sp.user_playlist_add_tracks(self.username, self.playlist['id'], [track['uri']])
            print "Success!"
        except spotipy.client.SpotifyException as exc:
            message = exc.msg.split(":\n ", 1)[1].encode('ascii', 'ignore')
            errorExit("ERROR: Spotify service request failed: {0}".format(message), file=file, color="red")

def errorWarning(message, color="white"):
    if color == "red":
        puts(colored.red(message))
    elif color == "yellow":
        puts(colored.yellow(message))
    else:
        puts(colored.white(message))

def errorExit(message, file=None, color="white"):
    if color == "red":
        puts(colored.red(message))
    elif color == "yellow":
        puts(colored.yellow(message))
    else:
        puts(colored.white(message))
    if file is not None:
        os.remove(file)
    sys.exit(1)

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
                errorExit("Thanks! Come again.")
            elif progress[0].lower() == 'y':
                print "Continuing..."
                break
            else:
                errorWarning("Select from either Y or N", color="red")
        except TypeError:
            errorWarning("Enter a valid option: Y or N", color="red")

def download(url):
    global YOUTUBE_DL_OPTS
    file = '%s/Downloads/download.temp' % os.path.expanduser('~')
    YOUTUBE_DL_OPTS['outtmpl'] = file
    
    try:
        with youtube_dl.YoutubeDL(YOUTUBE_DL_OPTS) as ydl:
            ydl.download([url])
    except ContentTooShortError:
        errorWarning("Failed to download full file from {0}".format(url), color="red")
        errorExit("Please try again...", file=file, color="red")
    except:
        errorWarning("Failed to download file from {0}".format(url), color="red")
        errorExit("Please try again...", color="red")
    return file

def AcoustIDSearch(filename):
    try:
        search = acoustid.match(ACOUSTID_API_KEY, filename)
    except acoustid.NoBackendError:
        errorExit("ERROR: Chromaprint library/tool not found", color="red")
    except acoustid.FingerprintGenerationError:
        errorExit("ERROR: Audio fingerprint could not be calculated", color="red")
    except acoustid.WebServiceError as exc:
        errorExit("ERROR: Web service request failed: {0}".format(exc.message), color="red")

    results = []
    for score, rid, title, artist in search:
        results.append([score * 100, rid, title, artist])
    return sorted(results, reverse=True)

def firstValid(results):
    result = None
    for i, entry in enumerate(results):
        if entry.count(None) == 0:
            try:
                # convert track and artist smart quotes to regular quotes
                entry[2] = entry[2].replace(u'\u2018', u"'").replace(u'\u2019', u"'")
                entry[2] = entry[2].replace(u'\u201C', u'"').replace(u'\u201D', u'"')
                entry[2].encode('ascii')

                entry[3] = entry[3].replace(u'\u2018', u"'").replace(u'\u2019', u"'")
                entry[3] = entry[3].replace(u'\u201C', u'"').replace(u'\u201D', u'"')
                entry[3].encode('ascii')
                result = entry
                break
            except UnicodeEncodeError:
                continue
    return result


def cleanArtist(artist):
    clean_artists = re.split(' - | : |- |: ', artist)[:2]
    clean_artist = clean_artists[0].split(' & ')[0]
    return clean_artist

def cleanTrack(track):
    clean_track = re.sub(r'\(| \([^)]*\)|\) ', '', track)
    clean_track = re.sub(r'\[| \[[^\]]*\]|\] ', '', clean_track)
    return clean_track


def main():

    if len(sys.argv) == 2:
        url = sys.argv[1]
    elif len(sys.argv) > 2:
        errorWarning("WARNING: Only using first command line argument", color="yellow")

    try:
        init()
        displayIntro()

        spotted = SpottedOnSpotify()
        spotted.loginToSpotify()

        warning()

        spotted.createPlaylist()

        if 'url' not in locals():
            url = raw_input("Please enter a valid YouTube/SoundCloud URL: ")

        print "Downloading mp3 from URL..."
        temp_file = download(url)
        prefix, suffix = os.path.splitext(temp_file)
        file = str(prefix) + ".mp3"

        print "Analyzing audio fingerprint..."
        results = AcoustIDSearch(file)
        result = firstValid(results)

        if result is not None:
            # Using highest percentage match for Spotify search
            percentage = int(result[0])
            hit_artist = cleanArtist(str(result[3]))
            hit_track = cleanTrack(str(result[2]))
        else:
            errorExit("Failed to find a match for your track on the MusicBrainz database", file=file, color="red")

        hit_full = "{0} by {1}".format(hit_track, hit_artist)
        puts(colored.cyan("{0:04.2f}% MATCH: {1}".format(percentage, hit_full)))
        print "Searching Spotify..."
        track, found_match = spotted.searchSong(hit_artist.lower(), hit_track.lower(), file)
        
        if found_match:
            while True:
                try:
                    full_title = "{0} by {1}".format(track['name'], track['artists'][0]['name'])
                    prompt = "Would you like to add {0} to {1}? (y/n): ".format(full_title, spotted.playlist['name'])
                    add = raw_input(prompt)
                    if add[0].lower() == 'n':
                        errorExit("Thanks for trying! Come again.", file=file)
                    elif add[0].lower() == 'y':
                        spotted.addSongToPlaylist(track, file)
                        break
                    else:
                        errorWarning("Select from either Y or N", color="red")
                except TypeError:
                    errorWarning("Enter a valid option: Y or N", color="red")
        else:
            error = "Failed to find a match for {0} by {1} on Spotify".format(hit_track, hit_artist)
            errorExit(error, file=file, color="red")

    except KeyboardInterrupt:
        if 'file' not in locals():
            errorExit("\nExiting Spotted on Spotify...")
        else:
            errorExit("\nExiting Spotted on Spotify...", file=file)

if __name__ == "__main__":
    main()
    