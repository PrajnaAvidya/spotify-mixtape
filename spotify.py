import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

scope = "streaming,playlist-modify-public"
spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, open_browser=False))

client = MongoClient(os.getenv('DB_CONNECTION_STRING'))
db = client.mixtape
features = db.features
features.drop() # TODO clearing every time for testing


# returns a list of recommendations ids that aren't currently in db
def get_uncached_recommendations(track_id):
    recs = spotify_client.recommendations(
        seed_tracks=[track_id],
        limit=100
    )['tracks']

    track_ids = []
    for rec in recs:
        # check if already in db
        exists = features.find_one(rec['id'])
        if exists is None:
            track_ids.append(rec['id'])

    return track_ids

def insert_track_features(track_ids):
    track_features = spotify_client.audio_features(track_ids)
    for feature in track_features:
        feature['_id'] = feature['id']
        del feature['id']
        features.insert_one(feature)
