import pymongo
from pymongo import MongoClient, results, ASCENDING
from pymongo.database import Database
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from helper.settings import logger
from typing import Optional
import pandas as pd


class MongoDBManager:
    def __init__(self, host: str, port: str, username: str = "", password: str = "",
                 db_name: str = "default"):

        self.db_port: int = int(port)
        self.db_host: str = host
        self.username: str = username
        self.password: str = password

        self.db_url = ("mongodb://" + self.username + ":"+ self.password + "@" +
                       self.db_host + ":" + str(self.db_port) + "/")

        self.db_name: str = db_name
        self.db_client: Optional[MongoClient] = None
        self.db:  Optional[Database] = None
        self.status = 200

    def establish_client_connection(self):
        try:
            logger.info("Connection established with MongoDB at {}:{}".format(
                self.db_host, self.db_port
            ))
            self.db_client: MongoClient = MongoClient(self.db_host, self.db_port)
        except Exception as e:
            logger.error(e)

    def set_up_db(self):
        try:
            # Establish connection
            self.establish_client_connection()
            # Create new instance of the db
            self.db = self.db_client[self.db_name]
        except Exception as e:
            logger.error(e)

    def create_index_at_collection(self, collection_name: str, unique_uuid_col: str):
        try:
            self.db[collection_name].create_index([(unique_uuid_col, ASCENDING)],
                                                  unique=True)
        except Exception as e:
            logger.error(e)

    def check_dbManager(self):
        """
        Checks if dbManager has started. If not, initialize dbManager.
        """
        try:
            if self.db_client is None:
                # If no exists
                if not self.check_database_exists():
                    logger.info("A new DB has been created")
                self.establish_client_connection()
                self.db = self.db_client[self.db_name]
        except Exception as e:
            logger.error(e)
            self.status = 500

    def check_database_exists(self):
        response: bool = False
        try:
            dblist: list = self.db_client.list_database_names()
            if self.db_name in dblist:
                response: bool = True
                self.status: int = 200
        except Exception as e:
            logger.error(e)
            self.status: int = 404
        return response

    def insert_document_to_collection(self, collection_name: str, document: dict):
        response: bool = False
        try:
            self.check_dbManager()
            if self.db is not None:
                self.db[collection_name].insert_one(document)
                response: bool = True
            else:
                logger.warning("Unable to insert data into collection %s", collection_name)
        except Exception as e:
            logger.error(e)
            self.status = 404
        return response

    def close_connection(self):
        try:
            self.db_client.close()
        except Exception as e:
            logger.error(e)

    def get_all_documents_from_collection(self, collection_name: str, filter_data: dict):
        documents: list = []
        try:
            if self.db is not None:
                documents: list = list(self.db[collection_name].find({}, filter_data))
        except Exception as e:
            logger.error(e)
        return documents

    def get_document_by_id(self, collection_name: str, uuid: str):
        document: dict = {}
        try:
            document: dict = self.db[collection_name].find_one({"_id": ObjectId(uuid)})
        except Exception as e:
            logger.error(e)
        return document

    def remove_all_documents_from_collection(self, collection_name: str):
        try:
            docs: results.DeleteResult = self.db[collection_name].delete_many({})
            logger.info("%s documents deleted from %s", docs.deleted_count, collection_name)
        except Exception as e:
            logger.error(e)

    def find_document_by_filter(self, collection_name: str, filter: dict):
        doc: Optional[Cursor] = None
        try:
            doc: Cursor = self.db[collection_name].find(filter)
        except Exception as e:
            logger.error(e)
        return doc

    def find_sorted_docs_by_id(self, collection_name: str):
        docs: Optional[Cursor] = None
        try:
            docs: Cursor = self.db[collection_name].find({}).sort(
                [("_id", pymongo.ASCENDING)])
        except Exception as e:
            logger.error(e)
        return docs

    def find_and_replace_document(self, collection_name: str, filter: dict, updated_doc: dict):
        doc: Optional[results.UpdateResult] = None
        try:
            doc: results.UpdateResult = self.db[collection_name].replace_one(
                filter=filter,
                replacement=updated_doc)
            logger.warning("Document Updated!")
        except Exception as e:
            logger.error(e)
        return doc

    def find_one_document(self, collection_name: str):
        doc: dict = {}
        try:
            doc: dict = self.db[collection_name].find_one()
        except Exception as e:
            logger.error(e)
        return doc

    def find_all_document_ids(self, collection_name: str):
        doc_ids: iter = iter([])
        try:
            response: list = self.db[collection_name].distinct("_id")
            doc_ids: iter = iter([str(i) for i in response])
        except Exception as e:
            logger.error(e)
        return doc_ids

    def generate_dataframe_from_collection(self, collection_name: str, query: dict, no_id=False):
        df: pd.DataFrame = pd.DataFrame([])
        try:
            # Make a query to the specific DB and Collection
            cursor = self.db[collection_name].find(query)

            # Expand the cursor and construct the DataFrame
            df = pd.DataFrame(list(cursor))

            # Delete the _id
            if no_id and '_id' in df:
                del df['_id']
        except Exception as e:
            logger.error(e)
        return df