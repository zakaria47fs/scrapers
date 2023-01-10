from time import sleep
from datetime import datetime, timedelta
import logging
from pytz import timezone

from services.mongo_service import MongoService


TZ_EST = timezone('EST')
mongo_service = MongoService()
target_collection = 'target_db'
amazon_collection = 'amazon_db'
walmart_collection = 'walmart_db'
rapidapi_om_collection = 'rapidapi_om_db'

def clear_expired_deals():
    while True:
        logging.info('Running clear_expired_deals')

        today = datetime.now(TZ_EST)
        yesterday = (today-timedelta(1)).replace(hour=1, minute=0, second=0, microsecond=0)
        previous_sunday = (today + timedelta( (6-today.weekday())%7 - 7 )).replace(hour=1, minute=0, second=0, microsecond=0)

        mongo_service.remove_many_db(amazon_collection, filter={'$or': [{'created_at': None}, {'created_at': {'$lt': yesterday}}]})
        mongo_service.remove_many_db(walmart_collection, filter={'$or': [{'created_at': None}, {'created_at': {'$lt': yesterday}}]})
        mongo_service.remove_many_db(target_collection, filter={'$or': [{'created_at': None}, {'created_at': {'$lt': previous_sunday}}]})
        sleep(3600)
