from pymongo import MongoClient
from urllib.parse import quote_plus
from services import configuration as cfg
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

    def add_one_db(self, collection_name, data):
        self._database[collection_name].insert_one(data)

    def add_many_db(self, collection_name, list_data): # list_data: list  of dicts/objects
        self._database[collection_name].insert_many(list_data)

    def get_one_db(self, collection_name, profile_id):
        return self._database[collection_name].find_one({"_id": profile_id})

    def get_all_db(self, collection_name):
        return self._database[collection_name].find({})

    def update_one_db(self, collection_name, profile_id, data):
        self._database[collection_name].update_one(
                                            {"_id": profile_id},
                                            {"$set": data}
                                        )

    def remove_one_db(self, collection_name, profile_id):
        self._database[collection_name].delete_one({"_id": profile_id})

    def filter_data_db(self, collection_name, filter):
        return self._database[collection_name].find(filter)

    def update_by_link(self, collection_name, data):
        self._database[collection_name].update_one(
                                            {"link_url": data.get('link_url')},
                                            {"$set": data},
                                            upsert=True
                                        )