import os

# Set environment variables
os.environ['MONGODB_HOST'] = 'localhost'
os.environ['MONGODB_PORT'] = '27017'
os.environ['MONGODB_USERNAME'] = ''
os.environ['MONGODB_PASSWORD'] = ''
os.environ['MONGODB_DB_NAME'] = 'test_data'
os.environ['ALBUMS_COLLECTION_NAME'] = 'test_albums'
os.environ['ARTISTS_COLLECTION_NAME'] = 'test_artists'
os.environ['TRACKS_COLLECTION_NAME'] = 'test_tracks'

os.environ['SP_CLIENT_ID'] = 'fb8e4a3c95f64f5d846b20b0a5bea074'
os.environ['SP_CLIENT_SECRET'] = 'a8764e5f1d94424e98e335a5816569cd'
os.environ['SP_USERNAME'] = 'rockdave'
os.environ['SP_REDIRECT_URI'] = 'http://127.0.0.1:5005/callback'
os.environ['SP_SCOPE'] = 'playlist-modify-private'

os.environ['MUSIXMATCH_API_KEY'] = '5cb94e76bddfc2c7d7fce92b2f1a3c14'


from spotmux.spotmux import SpotMux

countries: list = ["GB"]
continent: str = "Europe"
categories: list = ["Summer"]
locale: str = "en_EN"

spotmux_obj: SpotMux = SpotMux(
    countries=countries,
    continent=continent,
    categories=categories)

spotmux_obj.set_up_collector()
spotmux_obj.retrieve_data()