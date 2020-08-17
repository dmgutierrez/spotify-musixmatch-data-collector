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

##### Setting up the project
Set up all the paths and links of the module from your root directory.

```sh
$ pip install -e .
```

##### Install dependencies
Install all the dependencies of the module.

```sh
$ pip install -r requirements.txt
```

##### Setting up environment variables
In order to run the module, you would need to create the following environment variables:
Environment Variable | Description
------------ | -------------
MONGODB_HOST | MongoDB host
MONGODB_PORT | MongoDB port
MONGODB_USERNAME | MongoDB username
MONGODB_PASSWORD | MongoDB password
MONGODB_DB_NAME | MongoDB database name
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
##### Setting your environment variables
Before working with the module, you will need to incorporate the aforementioned environment variables in your system. An example of how to proceed is provided below.

```python
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

os.environ['SP_CLIENT_ID'] = 'xxxx'
os.environ['SP_CLIENT_SECRET'] = 'xxxx'
os.environ['SP_USERNAME'] = 'xxxx'
os.environ['SP_REDIRECT_URI'] = 'http://xxxx:xxxx/callback'
os.environ['SP_SCOPE'] = 'playlist-modify-private'

os.environ['MUSIXMATCH_API_KEY'] = 'xxxx'
```

##### Retrieve information from a set of countries

Retrieve information from a list of countries via [country code alpha-2](https://www.iban.com/country-codes). If the continent parameter is provided, the system will only query those countries from such continent which are available in Spotify according to this [Spotify market list](https://gist.github.com/wilsonpage/503092f6cd87f9152d5a523bb82ce730).
Moreover, a list of categories can also be included in the object, otherwise, the module will retrieve all the categories associated to each country.

The data is directly stored in the different mongoDB collections according to the nature of the entity (Track, Album or Artist).

```python
from spotmux.spotmux import SpotMux

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