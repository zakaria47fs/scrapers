import logging
from typing import List
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from pytz import timezone
import threading

from services.mongo_service import MongoService
from utils.authentication import authorize_user
from utils.models import DataObject, PyObjectId, DataCategory, UserCategory, UserKeywords, MovieDataObject
from utils.utils import clear_expired_deals


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
rapidapi_om_collection = 'rapidapi_om_db'

TZ_EST = timezone('EST')
yesterday_date = (datetime.now(TZ_EST) - timedelta(1)).replace(hour=1, minute=0, second=0, microsecond=0)
week_date = (datetime.now(TZ_EST) - timedelta(7)).replace(hour=1, minute=0, second=0, microsecond=0)


@app.get("/target/deals", response_model=List[DataObject], tags=['Target'])
@authorize_user
def get_deals(request: Request, skip: int = 0, limit: int = 0):
    logging.info(f"{request.method} {request.url}")
    #data = mongo_service.get_all_db(target_collection, skip, limit)
    filter_ = {"created_at": {"$gte": week_date}}
    data = mongo_service.filter_data_db(target_collection, skip, limit, filter_)
    return list(data)


@app.get("/target/products/{id_item}", response_model=DataObject, tags=['Target'])
@authorize_user
def get_product_id(id_item, request: Request):
    logging.info(f"{request.method} {request.url}")
    data = mongo_service.get_one_db(target_collection, PyObjectId(id_item))
    return data


@app.get("/target/categories", response_model=List[DataCategory], tags=['Target'])
@authorize_user
def get_categories(request: Request):
    logging.info(f"{request.method} {request.url}")
    data = mongo_service.get_all_cat_db(target_collection)
    return list(data)


@app.post("/target/products_category", response_model=List[DataObject], tags=['Target'])
@authorize_user
def get_product_category(item: UserCategory, request: Request):
    logging.info(f"{request.method} {request.url}")
    filter_ = {"primary_category": {"$in": item.categories}}
    data = mongo_service.filter_data_db(target_collection, filter_)
    return list(data)


@app.post("/target/products_keyword", response_model=List[DataObject], tags=['Target'])
@authorize_user
def get_product_keywords(item: UserKeywords, request: Request):
    logging.info(f"{request.method} {request.url}")
    data = mongo_service.filter_by_keywords_db(target_collection, item.keywords)
    return list(data)


@app.get("/amazon/deals", response_model=List[DataObject], tags=['Amazon'])
@authorize_user
def get_deals(request: Request, skip: int = 0, limit: int = 0):
    logging.info(f"{request.method} {request.url}")
    filter_ = {"created_at": {"$gte": yesterday_date}}
    data = mongo_service.filter_data_db(amazon_collection, skip, limit, filter_)
    return list(data)


@app.get("/amazon/products/{id_item}", response_model=DataObject, tags=['Amazon'])
@authorize_user
def get_product_id(id_item, request: Request):
    logging.info(f"{request.method} {request.url}")
    data = mongo_service.get_one_db(amazon_collection, PyObjectId(id_item))
    return data


@app.get("/amazon/categories", response_model=List[DataCategory], tags=['Amazon'])
@authorize_user
def get_categories(request: Request):
    logging.info(f"{request.method} {request.url}")
    data = mongo_service.get_all_cat_db(amazon_collection)
    return list(data)


@app.post("/amazon/products_category", response_model=List[DataObject], tags=['Amazon'])
@authorize_user
def get_product_category(item: UserCategory, request: Request):
    logging.info(f"{request.method} {request.url}")
    filter_ = {"primary_category": {"$in": item.categories}}
    data = mongo_service.filter_data_db(amazon_collection, filter_)
    return list(data)


@app.post("/amazon/products_keyword", response_model=List[DataObject], tags=['Amazon'])
@authorize_user
def get_product_keywords(item: UserKeywords, request: Request):
    logging.info(f"{request.method} {request.url}")
    data = mongo_service.filter_by_keywords_db(amazon_collection, item.keywords)
    return list(data)


@app.get("/walmart/deals", response_model=List[DataObject], tags=['Walmart'])
@authorize_user
def get_deals(request: Request, skip: int = 0, limit: int = 0):
    logging.info(f"{request.method} {request.url}")
    filter_ = {"created_at": {"$gte": week_date}}
    data = mongo_service.filter_data_db(walmart_collection, skip, limit, filter_)
    return list(data)


@app.get("/walmart/products/{id_item}", response_model=DataObject, tags=['Walmart'])
@authorize_user
def get_product_id(id_item, request: Request):
    logging.info(f"{request.method} {request.url}")
    data = mongo_service.get_one_db(walmart_collection, PyObjectId(id_item))
    return data


@app.get("/walmart/categories", response_model=List[DataCategory], tags=['Walmart'])
@authorize_user
def get_categories(request: Request):
    logging.info(f"{request.method} {request.url}")
    data = mongo_service.get_all_cat_db(walmart_collection)
    return list(data)


@app.post("/walmart/products_category", response_model=List[DataObject], tags=['Walmart'])
@authorize_user
def get_product_category(item: UserCategory, request: Request):
    logging.info(f"{request.method} {request.url}")
    filter_ = {"primary_category": {"$in": item.categories}}
    data = mongo_service.filter_data_db(walmart_collection, filter_)
    return list(data)


@app.post("/walmart/products_keyword", response_model=List[DataObject], tags=['Walmart'])
@authorize_user
def get_product_keywords(item: UserKeywords, request: Request):
    logging.info(f"{request.method} {request.url}")
    data = mongo_service.filter_by_keywords_db(walmart_collection, item.keywords)
    return list(data)


@app.get("/movie/comingsoon", response_model=List[MovieDataObject], tags=['Movies'])
@authorize_user
def get_deals(request: Request, skip: int = 0, limit: int = 0, keywords: str = ''):
    logging.info(f"{request.method} {request.url}")
    filters = {"videoUrl": {"$ne": None}}
    if keywords:
        data = mongo_service.filter_movies_by_keywords_db(rapidapi_om_collection, skip, limit, keywords, filters)
    else:
        data = mongo_service.filter_data_db(rapidapi_om_collection, skip, limit, filters)
    return list(data)


@app.get("/movie/{id_item}", response_model=MovieDataObject, tags=['Movies'])
@authorize_user
def get_product_id(id_item, request: Request):
    logging.info(f"{request.method} {request.url}")
    data = mongo_service.get_one_db(rapidapi_om_collection, PyObjectId(id_item))
    return data


# thread to clear expired deals
@app.on_event("startup")
async def startup_event():
    thread = threading.Thread(target=clear_expired_deals)
    thread.start()
