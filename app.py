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
target_collection = 'target_db'
amazon_collection = 'amazon_db'
walmart_collection = 'walmart_db'


@app.get("/target/deals", response_model=List[DataObject], tags=['Target'])
@authorize_user
def get_deals(request: Request, skip: int = 0, limit: int = 0):
    data = mongo_service.get_all_db(target_collection, skip, limit)
    return list(data)


@app.get("/target/products/{id_item}", response_model=DataObject, tags=['Target'])
@authorize_user
def get_product_id(id_item, request: Request):
    data = mongo_service.get_one_db(target_collection, PyObjectId(id_item))
    return data


@app.get("/target/categories", response_model=List[DataCategory], tags=['Target'])
@authorize_user
def get_categories(request: Request):
    data = mongo_service.get_all_cat_db(target_collection)
    return list(data)


@app.post("/target/products_category", response_model=List[DataObject], tags=['Target'])
@authorize_user
def get_product_category(item: UserCategory, request: Request):
    filter_ = {"primary_category": {"$in": item.categories}}
    data = mongo_service.filter_data_db(target_collection, filter_)
    return list(data)


@app.post("/target/products_keyword", response_model=List[DataObject], tags=['Target'])
@authorize_user
def get_product_keywords(item: UserKeywords, request: Request):
    data = mongo_service.filter_by_keywords_db(target_collection, item.keywords)
    return list(data)


@app.get("/amazon/deals", response_model=List[DataObject], tags=['Amazon'])
@authorize_user
def get_deals(request: Request, skip: int = 0, limit: int = 0):
    data = mongo_service.get_all_db(amazon_collection, skip, limit)
    return list(data)


@app.get("/amazon/products/{id_item}", response_model=DataObject, tags=['Amazon'])
@authorize_user
def get_product_id(id_item, request: Request):
    data = mongo_service.get_one_db(amazon_collection, PyObjectId(id_item))
    return data


@app.get("/amazon/categories", response_model=List[DataCategory], tags=['Amazon'])
@authorize_user
def get_categories(request: Request):
    data = mongo_service.get_all_cat_db(amazon_collection)
    return list(data)


@app.post("/amazon/products_category", response_model=List[DataObject], tags=['Amazon'])
@authorize_user
def get_product_category(item: UserCategory, request: Request):
    filter_ = {"primary_category": {"$in": item.categories}}
    data = mongo_service.filter_data_db(amazon_collection, filter_)
    return list(data)


@app.post("/amazon/products_keyword", response_model=List[DataObject], tags=['Amazon'])
@authorize_user
def get_product_keywords(item: UserKeywords, request: Request):
    data = mongo_service.filter_by_keywords_db(amazon_collection, item.keywords)
    return list(data)


@app.get("/walmart/deals", response_model=List[DataObject], tags=['Walmart'])
@authorize_user
def get_deals(request: Request, skip: int = 0, limit: int = 0):
    data = mongo_service.get_all_db(walmart_collection, skip, limit)
    return list(data)


@app.get("/walmart/products/{id_item}", response_model=DataObject, tags=['Walmart'])
@authorize_user
def get_product_id(id_item, request: Request):
    data = mongo_service.get_one_db(walmart_collection, PyObjectId(id_item))
    return data


@app.get("/walmart/categories", response_model=List[DataCategory], tags=['Walmart'])
@authorize_user
def get_categories(request: Request):
    data = mongo_service.get_all_cat_db(walmart_collection)
    return list(data)


@app.post("/walmart/products_category", response_model=List[DataObject], tags=['Walmart'])
@authorize_user
def get_product_category(item: UserCategory, request: Request):
    filter_ = {"primary_category": {"$in": item.categories}}
    data = mongo_service.filter_data_db(walmart_collection, filter_)
    return list(data)


@app.post("/walmart/products_keyword", response_model=List[DataObject], tags=['Walmart'])
@authorize_user
def get_product_keywords(item: UserKeywords, request: Request):
    data = mongo_service.filter_by_keywords_db(walmart_collection, item.keywords)
    return list(data)