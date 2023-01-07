import pyautogui
import os
from utils import create_dire,save_page,max_page_graber,pages_links_graber,products_links_graber,product_scraper
import logging
from services.mongo_service import MongoService
from datetime import datetime
import time
pyautogui.FAILSAFE = False
logging.basicConfig(filename='log_app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

mongo_service = MongoService()
collection_name = 'walmart_db'

if __name__=='__main__':
    logging.info(f"Start time : {datetime.now()}")
    create_dire('walmart_page')
    products_links = []
    while 1:
        try:
            save_page('https://www.walmart.com/shop/deals/trending-flash-picks','walmart_page','walmart_page')
            time.sleep(5)
            max_page = max_page_graber()
            pages_links = pages_links_graber(max_page)
            pyautogui.hotkey('Ctrl','Shift', 'w')
            break
        except:
            pass
    for page_link in pages_links:
        logging.info('scraping page link {}'.format(page_link))
        create_dire('walmart_page')
        while 1:
            try:
                save_page(page_link,'walmart_page','walmart_page')
                time.sleep(5)
                products_links = products_links_graber(products_links)
                pyautogui.hotkey('Ctrl','Shift', 'w')
                break
            except:
                pass
    for product_link in products_links:
        create_dire('products_page')
        logging.info('scraping product page {}'.format(product_link))
        start_time = datetime.now()
        while 1:
            stop_time = datetime.now()
            try:
                if (stop_time-start_time).seconds/60>=1:
                    break
                save_page(product_link,'product_page','product_page')
                time.sleep(5)
                product_path = os.path.abspath(os.getcwd())+'\\saved_pages\\products_page\\product_page.html'
                product_data = product_scraper(product_path)
                mongo_service.update_by_link(collection_name, product_data)
                pyautogui.hotkey('Ctrl','Shift', 'w')
                break
            except:
                pass
    logging.info('all_item_links length: {}'.format(len(products_links)))
    logging.info("End process")
    logging.info(f"End time : {datetime.now()}")
