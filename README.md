# Spotted on Spotify
### Command Line Application
[![Build Status](https://travis-ci.org/futurice/secret.svg?branch=master)](https://travis-ci.org/futurice/secret)

Have you ever gone back and forth between YouTube/SoundCloud trying to add songs to your Spotify playlist, only to waste time and find that the song is not available on Spotify? Look no further!

## Setup

* `pip install spotted-on-spotify`
* Run `spotted-on-spotify` once to prompt the user authentication which will take you [here](https://github.com/anthonymirand/SpottedOnSpotify-cmdline).
* Paste the link into the command line.

That's it! _You're authenticated and ready to go!_

## Usage

```
$ spotted-on-spotify
```

When you have a specific YouTube or SoundCloud URL that you would like to search on Spotify, run the script, paste in the URL, and choose the best match!

Running the script allows the creation and modification of a public Spotify playlist appropriately named "Spotted on Spotify" where the successful searches will be saved.

## TODO

* Catch errors from [youtube_dl](https://github.com/rg3/youtube-dl)
* Catch errors from [spotipy](https://github.com/plamere/spotipy)
* Sanitize MusicBrainz results for ASCII/Unicode characters
* Use/create a more efficient track analysis tool:
    * Implement MusicBrainz Picard for audio fingerprint recognition
    * Use [MBSpotify](https://github.com/metabrainz/mbspotify) for direct matching between MusicBrainz Identifiers and Spotify URIs
* Encrypt environment variables for safe use; shhh...
