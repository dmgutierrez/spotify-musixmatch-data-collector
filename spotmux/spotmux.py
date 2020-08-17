from .helper.settings import logger
from .managers.data_manager import DataManager


class SpotMux(object):
    def __init__(self, countries: list, continent: str = None, categories: list = None,
                 locale: str = "en_EN"):
        self.countries: list = countries
        self.categories: list = categories
        self.continent: str = continent
        self.locale: str = locale
        self.data_collector: DataManager = DataManager()

    def set_up_collector(self):
        try:
            self.data_collector.set_up_spotify_connection()
            self.data_collector.set_up_mongodb_connection()
        except Exception as e:
            logger.error(e)

    def retrieve_data(self):
        try:
            # 1. Verify countries
            logger.info("Verifying input countries in Spotify ... ")
            if self.continent is not None:

                checked_countries: list = self.data_collector.check_countries_by_continent(
                    countries=self.countries,
                    continent=self.continent)
            else:
                checked_countries: list = self.data_collector.check_countries(
                    countries=self.countries)

            # 2. Retrieve data from Spotify + MusixMatch
            logger.info("Starting Data Ingestion")
            self.data_collector.retrieve_spotify_data_by_countries(
                countries=checked_countries,
                locale=self.locale,
                categories=self.categories)
            logger.info("Done!")
        except Exception as e:
            logger.error(e)

    def export_collections_to_csv(self, root_directory: str):
        try:
            logger.info("Exporting data into csv ... ")
            self.data_collector.export_mongodb_collection_into_csv(
                directory=root_directory)
        except Exception as e:
            logger.error(e)