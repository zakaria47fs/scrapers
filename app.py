from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import logging

from services.mongo_service import MongoService


# logging configuration
logging.basicConfig(filename='log_app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


app = FastAPI()

mongo_service = MongoService()
collection_name = 'target_db'


class DataObject(BaseModel):
    primary_category: str
    sub_category: str
    product_title: str
    product_brand: str
    old_price: str
    new_price: str
    link_url: str
    thumbnail: str
    description: str


@app.get("/target_deals", response_model=List[DataObject])
def get_deals():
    data = mongo_service.get_all_db(collection_name)
    return list(data)
