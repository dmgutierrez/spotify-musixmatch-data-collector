import os
import coloredlogs, logging

# Create a logger object.
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


# ================================================================
# MONGODB Params
db_host: str = os.getenv("MONGODB_HOST") if "MONGODB_HOST" in os.environ else "localhost"
db_port: str = os.getenv("MONGODB_PORT") if "MONGODB_PORT" in os.environ else "27017"
db_username: str = os.getenv("MONGODB_USERNAME") if "MONGODB_USERNAME" in os.environ else ""
db_password: str = os.getenv("MONGODB_PASSWORD") if "MONGODB_PASSWORD" in os.environ else ""
db_name: str = os.getenv("MONGODB_DB_NAME") if "MONGODB_DB_NAME" in os.environ else "spotify_musicmatch"
tracks_collection_name: str = os.getenv("TRACKS_COLLECTION_NAME") if "TRACKS_COLLECTION_NAME" in\
                                                               os.environ else "spotify_tracks"
albums_collection_name: str = os.getenv("ALBUMS_COLLECTION_NAME") if "ALBUMS_COLLECTION_NAME" in\
                                                               os.environ else "spotify_albums"
artists_collection_name: str = os.getenv("ARTISTS_COLLECTION_NAME") if "ARTISTS_COLLECTION_NAME" in\
                                                               os.environ else "spotify_artists"

# ================================================================
# Spotify Params
sp_client_id: str = os.getenv("SP_CLIENT_ID") if "SP_CLIENT_ID" in os.environ \
    else "fb8e4a3c95f64f5d846b20b0a5bea074"
sp_client_secret: str = os.getenv("SP_CLIENT_SECRET") if "SP_CLIENT_SECRET" in os.environ \
    else "a8764e5f1d94424e98e335a5816569cd"
sp_username = os.getenv("SP_USERNAME") if "SP_USERNAME" in os.environ \
    else "rockdave"
sp_redirect_uri: str = os.getenv("SP_REDIRECT_URI") if "SP_REDIRECT_URI" in os.environ \
    else "http://127.0.0.1:5005/callback"
sp_scope: str = os.getenv("SP_SCOPE") if "SP_SCOPE" in os.environ \
    else "playlist-modify-private"
# ================================================================
#

musixmatch_api_key: str = os.getenv("MUSIXMATCH_API_KEY") if "MUSIXMATCH_API_KEY" in os.environ \
    else "5cb94e76bddfc2c7d7fce92b2f1a3c14"

http_response_500: str = "Internal Server Error"
http_response_200: str = "Successful Operation"
http_response_422: str = "Invalid Input"
http_response_400: str = "Bad Request"
http_response_403: str = "HTTP Connection Error"
