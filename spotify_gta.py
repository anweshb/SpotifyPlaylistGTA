import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from spotify_creds import username, client_id, client_secret
scope = 'playlist-read-private'
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret,
                                   redirect_uri='http://localhost:8888/')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret,
                                               redirect_uri='http://localhost:8888/'))

pl_id = "spotify:playlist:1i2jb32Fh9ddVBwS5GqU9q"


def show_tracks(results, uriArray):
    for i, item in enumerate(results['items']):
        track = item['track']
        uriArray.append(track['id'])


def get_playlist_track_id(username, playlist_id):
    track_id = []
    results = sp.user_playlist(username, playlist_id)
    tracks = results['tracks']
    show_tracks(tracks, track_id)
    while tracks['next']:
        tracks = sp.next(tracks)
        show_tracks(tracks, track_id)
    return track_id


track_ids = get_playlist_track_id(username, pl_id)


def get_track_url(track_id):
    song_data = sp.track(track_id)

    song_url = str(song_data['external_urls']['spotify'])

    return song_url


def playlist_track_urls(track_ids):
    track_urls = []
    count = 0
    for track_id in track_ids:
        count += 1
        track_urls.append(get_track_url(track_id))
        print("Track number: " + str(count) + " Track Link: " + get_track_url(track_id))

    return track_urls


playlist_track_urls(track_ids)
