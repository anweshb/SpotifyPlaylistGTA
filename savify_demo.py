from savify import Savify
from savify.types import Type, Format, Quality
from savify.utils import PathHolder
from spotify_creds import client_id, client_secret

s = Savify(quality=Quality.BEST, download_format=Format.MP3, path_holder=PathHolder(downloads_path='C:\\Users\\Admin\\Music\\Savify Demo\\'),
           api_credentials=(client_id, client_secret))
s.download('https://open.spotify.com/track/3eekarcy7kvN4yt5ZFzltW?si=4cb534180791447d')