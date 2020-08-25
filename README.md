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

##### Setting up relevant variables
In order to run the module, you would need to consider the following variables:
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

# Fill out the parameters with your own ones
default_value: str = "xxxx"
mongodb_params: dict = {"host": "localhost",
                        "port": "27017",
                        "username": default_value,
                        "password": default_value,
                        "db_name": "test_db_spot",
                        "tracks_collection_name": "test_tracks",
                        "albums_collection_name": "test_albums",
                        "artists_collection_name": "test_artists"}

# Fill out the parameters with your own ones
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
default_value: str = "xxxx"
mongodb_params: dict = {"host": "localhost",
                        "port": "27017",
                        "username": default_value,
                        "password": default_value,
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


# Create the object with default parameters
spotmux_obj: SpotMux = SpotMux(
    mongodb_params=mongodb_params,
    music_manager_params=music_manager_params,
    countries=countries,
    countries=[])
    
# Initialise the object
spotmux_obj.set_up_collector()

# Export collections into CSV files
spotmux_obj.export_collections_to_csv(root_directory=root_dir)
```

### Data Models
#### Tracks Data Model
Attribute | Type | Description
------------ | ------------- | ------------- 
id | string | spotify track id
name | string | spotify track name
popularity | integer | spotify track popularity
preview_url | string | spotify preview url
available_markets | list | list of countries where the track is available
continents | list | list of continents where the track is available
total_markets | integer | total number of markers
disc_number | integer | spotify disc number
duration_ms | integer | track duration in ms
href | string | spotify track href
track_number | integer | spotify track number
artists_spotify_id | list | list of artist ids
album_spotify_id | string | album id
playlist_name | string | spotify playlist name
category | string | playlist category
audio_features | dictionary | spotify pre-computed audio features
lyrics | string | musixmatch lyrics

For more information, you can consult the official Spotify Web API regarding Tracks at [Get a Track](https://developer.spotify.com/documentation/web-api/reference/tracks/get-track/). 

#### Album Data Model
Attribute | Type | Description
------------ | ------------- | ------------- 
album_type | string | spotify album type
artists_ids | list | list of artists ids 
available_markets | list | list of countries where the album is available
continents | list | list of continents where the album is available
total_markets | integer | total number of markers
copyrights | string | spotify album copyrights
external_urls | list | list of external URLs associated to the album
genres | list | list of genres associate to the album
href | string | spotify album href
id | string | spotify album id
images | list | list of images associated to an album
label | string | Spotify album label
name | string | Spotify Album name
popularity | integer | spotify album popularity
release_date | string | Spotify album release date
tracks_ids | list | list of Spotify tracks ids
uri | string | album spotify uri

For more information, you can consult the official Spotify Web API regarding Albums at [Get an Album](https://developer.spotify.com/documentation/web-api/reference/albums/get-album/). 

#### Artist Data Model
Attribute | Type | Description
------------ | ------------- | ------------- 
id | string | spotify artist id
name | string | spotify artist name
popularity | integer | spotify artist popularity
followers | integer | total number of followers in Spotify
genres | list | list of Spotify genres associated to the artist
href | string | spotify artist href
images | list | list of images associated to the artist
uri | string | artist spotify uri

For more information, you can consult the official Spotify Web API regarding Artists at [Get an Artist](https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/). 

### *TODOs*

 - Write more documentation within the code
 - Include Elasticsearch Manager to be used instead of MongoDB
 - Generate Unitests

License
----

MIT License

Copyright (c) 2020 DAVID MARTIN-GUTIERREZ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the SpotMux software), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Contact

For further explanations and doubts do not hesitate to send an email to dmargutierrez@gmail.com.