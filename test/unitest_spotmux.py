from spotmux.spotmux import SpotMux

default_value: str = "xxxx"
mongodb_params: dict = {"host": "localhost", "port": "27017",
                        "db_name": "test_db_spot",
                        "tracks_collection_name": "test_tracks",
                        "albums_collection_name": "test_albums",
                        "artists_collection_name": "test_artists"}

music_manager_params: dict = {"sp_client_id": default_value,
                              "sp_client_secret": default_value,
                              "sp_username": default_value,
                              "sp_redirect_uri": default_value,
                              "sp_scope": default_value,
                              "musixmatch_api_key":default_value}

# List of countries
countries: list = ["GB", "DE"]
# Continent (Optional)
continent: str = "Europe"
# List of categories (Optional)
categories: list = ["Summer"]
# Language of the queries for Spotify API
locale: str = "en_EN"

# Create the object
spotmux_obj: SpotMux = SpotMux(
    mongodb_params=mongodb_params,
    music_manager_params=music_manager_params,
    countries=countries,
    continent=continent,
    categories=categories)

# Initialise the object
spotmux_obj.set_up_collector()

# Start asynchronous process to retrieve data
spotmux_obj.retrieve_data()