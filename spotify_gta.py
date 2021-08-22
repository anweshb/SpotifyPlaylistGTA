import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from spotify_creds import username, client_id, client_secret, download_location
import youtube_dl
from youtubesearchpython import VideosSearch

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


##INSTEAD OF RETRIVING SPOTIFY URLS RETRIEVE TRACK NAME

def get_query(track_id):
    song_data = sp.track(track_id)

    song_name = str(song_data['name'])
    artist_name = str(song_data['artists'][0]['name'])

    query_name = song_name + " " + artist_name + " Official Audio"
    return query_name


def playlist_track_names(track_ids):
    query_names = []
    count = 0
    for track_id in track_ids:
        count += 1
        query_names.append(get_query(track_id))
        print("Track number: " + str(count) + " Query Name: " + get_query(track_id))

    return query_names


query_names = playlist_track_names(track_ids)


def download_songs(query_list, download_location):
    tracks_downloaded = 0
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': download_location + '/%(title)s.%(ext)s',
    }
    for query in query_list:
        videos_search = VideosSearch(query, limit=1)
        video_link = videos_search.result()['result'][0]['link']

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([str(video_link)])
                print("Downloaded " + str(tracks_downloaded) + " tracks")
            except:
                continue

        tracks_downloaded += 1


download_songs(query_list=query_names, download_location=download_location)
