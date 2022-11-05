from pymongo import MongoClient
from urllib.parse import quote_plus
import configuration as cfg
import logging


class MongoService:

    def __init__(self):
        try:
            host = cfg.db["host"]
            port = cfg.db["port"]
            database_name = cfg.db["dbname"]

            uri = "mongodb://%s:%s" % (host, port)
            mongo_client = MongoClient(uri, connect=False)
            self._database = mongo_client[database_name]
                    
        except Exception as ex:
            logging.error(ex)

    # Profile db operations
    def add_profile_db(self, data):
        self._database.profiles.insert_one(data)

    def get_profile_db(self, profile_id):
        return self._database.profiles.find_one({"_id": profile_id})

    def get_all_profiles_db(self):
        return self._database.profiles.find({})

    def update_profile_db(self, profile_id, data):
        self._database.profiles.update_one(
                                            {"_id": profile_id},
                                            {"$set": data}
                                        )

    def remove_profile_db(self, profile_id):
        self._database.profiles.delete_one({"_id": profile_id})

    def filter_profiles_db(self, filter):
        return self._database.profiles.find(filter)