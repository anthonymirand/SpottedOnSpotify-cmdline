import conf
import spotipy
import spotipy.util
import util

class SpottedOnSpotify:
  def __init__(self, username):
    self.username = username
    self.sp = None
    self.playlist = None

  def _spotify_access_warning(self):
    util.print_message('ALERT: Continuing allows this program to access your '
                       'public playlists and create/modify a new playlist.',
                       color='yellow')
    while True:
      try:
        status = raw_input('Would you like to continue? (y/n): ')[0].lower()
        if status == 'n':
          util.print_message('Thanks! Come again.', exit=True)
        elif status == 'y':
          util.print_message('Continuing...')
          return
        else:
          util.print_message('Select from either Y or N.', color='red')
      except TypeError:
        util.print_message('Enter a valid option: Y or N.', color='red')

  def login_to_spotify(self):
    try:
      token = spotipy.util.prompt_for_user_token(
                  self.username,
                  scope=conf.SPOTIPY_SCOPE,
                  client_id=conf.SPOTIPY_CLIENT_ID,
                  client_secret=conf.SPOTIPY_CLIENT_SECRET,
                  redirect_uri=conf.SPOTIPY_REDIRECT_URI)
      if token:
        self._spotify_access_warning()
        self.sp = spotipy.Spotify(auth=token)
      else:
        util.print_message('Cannot get token for {}. Please try again...' \
                           .format(self.username), color='red', exit=True)
    except spotipy.client.SpotifyException as exc:
      # message = exc.msg.split(":\n ", 1)[1].encode('ascii', 'ignore')
      util.print_message('ERROR: Spotify service request failed: {}' \
                         .format(exc.msg), color='red', exit=True)

  def create_playlist(self):
    ''' Attempts to create custom playlist if it doesn't already exist. '''
    try:
      playlists = self.sp.user_playlists(self.username)
      for playlist in playlists['items']:
        if playlist['owner']['id'] == self.username and \
           playlist['name'] == 'Spotted on Spotify':
          self.playlist = playlist
          return
      else:
        util.print_message('Creating \"Spotted on Spotify\" playlist...')
        playlist = self.sp.user_playlist_create(self.username,
                                                'Spotted on Spotify')
        if playlist['name'] == 'Spotted on Spotify':
          self.playlist = playlist
          util.print_message('Completed creating playlist...')
          return
        else:
          self.sp.user_playlist_delete(self.username, playlist['name'])
          raise spotipy.client.SpotifyException('Failed creating \"Spotted on'
                                                'Spotify\" playlist.')
    except spotipy.client.SpotifyException as exc:
      # message = exc.msg.split(":\n ", 1)[1].encode('ascii', 'ignore')
      util.print_message('ERROR: Spotify service request failed: {}' \
                         .format(exc.msg), color='red', exit=True)

  def search_song(self, target_track, target_artist):
    ''' Search and loop through each track. '''
    util.print_message('Searching Spotify for {} by {}...' \
                       .format(target_track, target_artist))
    try:
      track_results = self.sp.search(q='track:\"{}\"'.format(target_track),
                                     type='track')
      tracks = track_results['tracks']['items']
      if len(tracks) == 0:
        util.print_message('No search results for {} by {}' \
                           .format(target_track, target_artist), exit=True)
      best_result = tracks[0]
      for track in tracks[1:]:
        try:
          search_track = str(track['name']) \
                             .replace(u'\u2018', u'\'') \
                             .replace(u'\u2019', u'\'') \
                             .replace(u'\u201C', u'\"') \
                             .replace(u'\u201D', u'\"')
          search_track.encode('ascii')
          search_artist = str(track['artists'][0]['name']) \
                              .replace(u'\u2018', u"'") \
                              .replace(u'\u2019', u"'") \
                              .replace(u'\u201C', u'"') \
                              .replace(u'\u201D', u'"')
          search_artist.encode('ascii')
        except UnicodeEncodeError:
          continue
        if target_track.lower() in search_track.lower() and \
           target_artist.lower() in search_artist.lower():
          best_result = max(best_result, track, key=lambda x: x['popularity'])
    except spotipy.client.SpotifyException as exc:
      # message = exc.msg.split(":\n ", 1)[1].encode('ascii', 'ignore')
      util.print_message('ERROR: Spotify service request failed: {}' \
                         .format(exc.msg), color='red', exit=True)
    return best_result

  def add_song_to_playlist(self, track):
    try:
      util.print_message('Adding track to {}...'.format(self.playlist['name']))
      self.sp.user_playlist_add_tracks(self.username,
                                       self.playlist['id'],
                                       [track['uri']])
      util.print_message('Success!', color='green')
    except spotipy.client.SpotifyException as exc:
      # message = exc.msg.split(":\n ", 1)[1].encode('ascii', 'ignore')
      util.print_message('ERROR: Spotify service request failed: {}' \
                         .format(exc.msg), color='red', exit=True)
