import pandas as pd
import os
from pymongo.cursor import Cursor
from models.doument_models import (PlaylistDataDoc)
from managers.music_manager import MusicManager
from managers.mongodb_manager import MongoDBManager
from helper.settings import (logger,
                             db_host, db_port, db_username,
                             db_password, db_name, tracks_collection_name,
                             albums_collection_name, artists_collection_name)
from helper.thread_utils import generate_batch_thread, start_all_batch_threads, join_threads
from helper.spotify_markets import spotify_markets
from helper.utils import prepare_directory, convert_country_to_continent


class DataManager:
    def __init__(self):
        self.music_manager: MusicManager = MusicManager()
        self.mongo_manager: MongoDBManager = MongoDBManager(
            host=db_host,
            port=db_port,
            username=db_username,
            password=db_password,
            db_name=db_name)
        self.tracks_collection_name: str = tracks_collection_name
        self.albums_collection_name: str = albums_collection_name
        self.artists_collection_name: str = artists_collection_name

    def set_up_spotify_connection(self):
        self.music_manager.set_up_spotify_connection()

    def set_up_mongodb_connection(self):
        self.mongo_manager.set_up_db()

    def get_collections(self):
        return [self.tracks_collection_name,
                self.artists_collection_name,
                self.albums_collection_name]

    def get_collection_thread_names(self):
        keys: list = self.get_collections()
        values: list = [i + "_thread" for i in keys]
        return dict(zip(keys, values))

    def retrieve_spotify_data_by_countries(self, countries: list, locale: str, categories: list = None, limit: int = 50):
        try:
            # 1. Retrieve playlists per category and country
            if categories is None:
                playlists_countries_data: dict = self.music_manager.spotify_manager.get_all_countries_playlists_ids(
                    sp_api=self.music_manager.spotify_manager.sp_api, countries=countries, limit=limit)
            else:
                playlists_countries_data: dict = \
                    self.music_manager.spotify_manager.get_countries_playlists_ids_by_categories(
                        sp_api=self.music_manager.spotify_manager.sp_api,
                        categories=categories, countries=countries,
                        locale=locale, limit=limit)

            total_playlists: int = len(playlists_countries_data.keys())
            total_countries: int = len(countries)

            # 2. Retrieve tracks, artists and albums from batch of playlists
            for i, data in enumerate(playlists_countries_data.items()):
                logger.info("Processing Playlist %s/%s from country %s. Total countries %s",
                            i+1, total_playlists, data[1], total_countries)
                playlist_id: str = data[0]
                market: str = data[1][0]
                category: str = data[1][1]

                # 3. Retrieve playlist information
                playlists_data_doc: PlaylistDataDoc = self.music_manager.extract_data_from_spotify_playlist(
                    playlist_id=playlist_id,
                    market=market,
                    category=category)

                # 4. Start ingestion
                collection_thread_names: dict = self.get_collection_thread_names()
                self.start_asynchronous_ingestion(
                    playlists_data_doc=playlists_data_doc,
                    thread_names=list(collection_thread_names.values()),
                    collection_names=list(collection_thread_names.keys()))

        except Exception as e:
            logger.error(e)

    def verify_documents_in_mongodb(self, entity: dict,
                                    collection_name: str):
        not_exist: bool = True
        try:

            filter_data: dict = {"id": entity.__getattribute__("id")}

            # 2. Find document
            res_doc: Cursor = self.mongo_manager.find_document_by_filter(
                collection_name=collection_name, filter=filter_data)
            not_exist: bool = True if len(list(res_doc)) == 0 else False
        except Exception as e:
            logger.error(e)
        return not_exist

    def start_asynchronous_ingestion(self, playlists_data_doc: PlaylistDataDoc,
                                     thread_names: list, collection_names: list):
        try:
            batch_threads: list = []
            # 1. Generate threads
            for thread_name, collection_name in zip(thread_names, collection_names):
                entity_docs: list = playlists_data_doc.__getattribute__(collection_name.split("_")[-1])

                batch_threads: list = generate_batch_thread(
                    batch_threads=batch_threads,
                    thread_name=thread_name,
                    target_func=self.ingest_spotify_data_into_mongodb,
                    args=(entity_docs, collection_name,))

            # 2. Start threads
            start_all_batch_threads(batch_threads=batch_threads)

            # 5. Join threads
            join_threads(batch_threads=batch_threads, thread_names=thread_names)
        except Exception as e:
            logger.error(e)

    def ingest_spotify_data_into_mongodb(self, entity_docs: list, collection_name: str):
        try:
            for entity in entity_docs:
                # 1. Verify document
                not_exist: bool = self.verify_documents_in_mongodb(
                    entity=entity,
                    collection_name=collection_name)
                if not_exist:
                    self.mongo_manager.insert_document_to_collection(
                        collection_name=collection_name,
                        document=entity.__dict__)
        except Exception as e:
            logger.error(e)

    def export_mongodb_collection_into_csv(self, directory: str,  no_id: bool = False):
        try:
            collections: list = self.get_collections()
            for collection in collections:
                logger.info("Exporting collection %s", collection)
                # Generate Pandas DataFrame
                df: pd.DataFrame = self.mongo_manager.generate_dataframe_from_collection(
                    collection_name=collection,
                    query={},
                    no_id=no_id)
                prepare_directory(dir_path_to_check=directory)
                filepath: str = os.path.join(directory, f"{collection}.csv")
                df.to_csv(filepath)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def check_countries_by_continent(countries: list, continent: str):
        checked_countries: list = [i for i in countries if (i in spotify_markets and
                                                            convert_country_to_continent(i) == continent)]
        return checked_countries
