# SpotMux: A data collector for Spotify & MusixMatch

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

A Python library for retrieving information from both Spotify and MusixMatch regarding Tracks, Artists and Albums

# New Features!

  - Retrieve and save Tracks, Albums and Artists from Spotify in a simple way in MongoDB
  - Retrieve lyrics from Musixmatch to extract the lyrics
  - Select countries, categories and continents to query and retrieve the information
  - Export your mongoDB collections into csv for further analysis
  - Asynchronous process to speed up the ingestion

### Before Starting

*spotmux* requires the following components:
* [MongoDB](https://www.mongodb.com/) to save the retrieved data in the corresponding collections. 
* A [Spotify Developer Account](https://developer.spotify.com/) with both **CLIENT ID** and **CLIENT SECRET** credentials.
* A [MusixMatch Developer Account](https://developer.musixmatch.com/) with its corresponding **API KEY**.

### Installation

You can easily install the module via pip.

```sh
$ pip install spotmux
```

##### Setting up relevant variables variables
In order to run the module, you would need to create the following environment variables:
Environment Variable | Description
------------ | -------------
HOST | MongoDB host
PORT | MongoDB port
USERNAME | MongoDB username
PASSWORD | MongoDB password
DB_NAME | MongoDB database name
ALBUMS_COLLECTION_NAME | MongoDB albums collection name
ARTISTS_COLLECTION_NAME | MongoDB artists collection name
TRACKS_COLLECTION_NAME | MongoDB tracks collection name
SP_CLIENT_ID | Spotify Client ID
SP_CLIENT_SECRET | Spotify Client Secret
SP_USERNAME | Spotify Username
SP_REDIRECT_URI | Spotify Redirect URI
SP_SCOPE | [Spotify API Authorization Scope](https://developer.spotify.com/documentation/general/guides/scopes/)
MUSIXMATCH_API_KEY | Musixmatch API KEY 

### 3. How to use it
##### Retrieve information from a set of countries

Retrieve information from a list of countries via [country code alpha-2](https://www.iban.com/country-codes). If the continent parameter is provided, the system will only query those countries from such continent which are available in Spotify according to this [Spotify market list](https://gist.github.com/wilsonpage/503092f6cd87f9152d5a523bb82ce730).
Moreover, a list of categories can also be included in the object, otherwise, the module will retrieve all the categories associated to each country.

The data is directly stored in the different mongoDB collections according to the nature of the entity (Track, Album or Artist).

```python
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
```

##### Export your collections to csv files
Once you have finished your process, you can export your collections in different CSVs files in order to do more analysis afterwards. You only need to select the root directory where you want to store these files.

```python
root_dir: str = "path/to/store/csv"

# Create the object with default parameters
spotmux_obj: SpotMux = SpotMux(
    countries=[])
    
# Initialise the object
spotmux_obj.set_up_collector()

# Export collections into CSV files
spotmux_obj.export_collections_to_csv(root_directory=root_dir)
```

### *TODOs*

 - Write more documentation within the code
 - Generate docstrings
 - Generate Unitests
 - Publish library to be installed via Pip

License
----

MIT

### Contact

For further explanations and doubts do not hesitate to send an email to dmargutierrez@gmail.com.