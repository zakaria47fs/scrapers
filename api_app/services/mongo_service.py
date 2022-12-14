from pymongo import MongoClient
from urllib.parse import quote_plus
from services import configuration as cfg
import logging


class MongoService:

    def __init__(self):
        try:
            host = cfg.db["host"]
            port = cfg.db["port"]
            username = cfg.db["username"]
            password = cfg.db["password"]
            database_name = cfg.db["dbname"]

            #uri = "mongodb://%s:%s" % (host, port)
            uri = "mongodb+srv://%s:%s@%s/?retryWrites=true&w=majority" % (quote_plus(username), quote_plus(password), host)
            mongo_client = MongoClient(uri, connect=False)
            self._database = mongo_client[database_name]

        except Exception as ex:
            logging.error(ex)

    def add_one_db(self, collection_name, data):
        self._database[collection_name].insert_one(data)

    def add_many_db(self, collection_name, list_data):  # list_data: list  of dicts/objects
        self._database[collection_name].insert_many(list_data)

    def get_one_db(self, collection_name, profile_id):
        return self._database[collection_name].find_one({"_id": profile_id})

    def get_all_db(self, collection_name, skip, limit):
        return self._database[collection_name].find({}).skip(skip).limit(limit)

    def get_all_cat_db(self, collection_name):
        return self._database[collection_name].find({})

    def update_one_db(self, collection_name, profile_id, data):
        self._database[collection_name].update_one(
            {"_id": profile_id},
            {"$set": data}
        )

    def remove_one_db(self, collection_name, profile_id):
        self._database[collection_name].delete_one({"_id": profile_id})

    def remove_many_db(self, collection_name, filter):
        self._database[collection_name].delete_many(filter)

    def filter_data_db(self, collection_name, skip, limit, filter):
        return self._database[collection_name].find(filter).skip(skip).limit(limit)

    def filter_by_keywords_db(self, collection_name, keywords):
        self._database[collection_name].create_index([("product_title", "text"), ("description", "text")])
        return self._database[collection_name].find({"$text": {"$search": keywords}})

    def filter_movies_by_keywords_db(self, collection_name, skip, limit, keywords):
        self._database[collection_name].create_index([("title","text"), ("titleType","text"), ("plotOutlineText","text"), ("videoDescription","text")])
        return self._database[collection_name].find({"$text": {"$search": keywords}}).skip(skip).limit(limit)

    def update_by_link(self, collection_name, data):
        self._database[collection_name].update_one(
            {"link_url": data.get('link_url')},
            {"$set": data},
            upsert=True
        )

    def update_by_field(self, collection_name, field, data):
        self._database[collection_name].update_one(
            {field: data.get(field)},
            {"$set": data},
            upsert=True
        )

    def drop_collection(self, collection_name):
        self._database.drop_collection(collection_name)
