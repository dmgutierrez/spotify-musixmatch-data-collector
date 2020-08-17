from managers.data_manager import DataManager
from helper.spotify_countries import spotify_countries


if __name__ == '__main__':

    countries: list = list(spotify_countries.keys())
    continent: str = "Europe"
    categories: list = ["Top Lists", "Summer", "Pop", "Hip Hop",
                        "Mood", "Workout", "Rock", "Electronic/Dance",
                        "At Home", "R&B", "Chill", "Indie", "Pride",
                        "Party", "Sleep", "Country", "Trending",
                        "Jazz", "Soul", "Afro", "Reggae", "Metal",
                        "Travel", "Punk", "Latin", "Funk"]
    locale: str = "en_EN"

    # 1. Create Data Manager Object
    dm: DataManager = DataManager()
    dm.set_up_spotify_connection()
    dm.set_up_mongodb_connection()

    # 2. Verify countries
    checked_countries: list = dm.check_countries_by_continent(
        countries=countries,
        continent=continent)

    # 3. Retrieve data from Spotify + MusixMatch
    dm.retrieve_spotify_data_by_countries(
        countries=checked_countries,
        locale=locale,
        categories=categories)