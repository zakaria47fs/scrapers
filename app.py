import logging
from typing import List

from fastapi import FastAPI, Request

from services.mongo_service import MongoService
from utils.authentication import authorize_user
from utils.models import DataObject, PyObjectId, DataCategory, UserCategory, UserKeywords

# logging configuration
logging.basicConfig(filename='log_app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

app = FastAPI()

mongo_service = MongoService()
collection_name = 'target_db'


@app.get("/target_deals", response_model=List[DataObject])
@authorize_user
def get_deals(request: Request):
    data = mongo_service.get_all_db(collection_name)
    return list(data)


@app.get("/products/{id_item}", response_model=DataObject)
@authorize_user
def get_product_id(id_item, request: Request):
    data = mongo_service.get_one_db(collection_name, PyObjectId(id_item))
    return data


@app.get("/categories", response_model=List[DataCategory])
@authorize_user
def get_categories(request: Request):
    data = mongo_service.get_all_db(collection_name)
    return list(data)


@app.get("/products_category", response_model=List[DataObject])
@authorize_user
def get_product_category(item: UserCategory, request: Request):
    filter_ = {"primary_category": {"$in": item.categories}}
    data = mongo_service.filter_data_db(collection_name, filter_)
    return list(data)


@app.get("/products_keyword", response_model=List[DataObject])
@authorize_user
def get_product_keywords(item: UserKeywords, request: Request):
    data = mongo_service.filter_by_keywords_db(collection_name, item.keywords)
    return list(data)
