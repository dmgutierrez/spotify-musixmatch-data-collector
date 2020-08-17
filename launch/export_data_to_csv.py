import os
from managers.data_manager import DataManager


if __name__ == '__main__':

    # Setting up Manager
    dm: DataManager = DataManager()
    dm.set_up_spotify_connection()
    dm.set_up_mongodb_connection()
    dm.export_mongodb_collection_into_csv(directory="")


