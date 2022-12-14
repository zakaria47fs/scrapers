from amazon_scraper.utils import get_pages_link,get_product_data,get_products_link,open_browser, TZ_EST
import logging
from datetime import datetime, timedelta

from services.mongo_service import MongoService


#logging configuration
logging.basicConfig(filename='amazon_scraper/log_app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

mongo_service = MongoService()
collection_name = 'amazon_db'


#Getting To Categories Page
driver= open_browser(driver_path='chromedriver --max_old_space_size=4096')


if __name__=='__main__':
    logging.info(f"Start time : {datetime.now()}")

    driver,page_links = get_pages_link(driver)
    driver,productslinks = get_products_link(driver,page_links)

    for productslink in productslinks:
      try:
        driver.get(productslink)
        driver,product_data = get_product_data(driver)
        # push product info to DB
        mongo_service.update_by_link(collection_name, product_data)
      except:
        pass
    logging.info("End process")
    logging.info(f"End time : {datetime.now()}")
