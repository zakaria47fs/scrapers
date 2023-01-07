import pyautogui
import os
from walmart_scraper.utils import create_dire,save_page,max_page_graber,pages_links_graber,products_links_graber,product_scraper
import logging
from services.mongo_service import MongoService
from datetime import datetime


# logging configuration
logging.basicConfig(filename='walmart_scraper/log_app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

mongo_service = MongoService()
collection_name = 'walmart_db'

if __name__=='__main__':
    logging.info(f"Start time : {datetime.now()}")
    create_dire('walmart_page')
    save_page('https://www.walmart.com/shop/deals/trending-flash-picks','walmart_page','walmart_page')
    products_links = []
    while 1:
        try:
            max_page = max_page_graber()
            pages_links = pages_links_graber(max_page)
            pyautogui.hotkey('ctrl', 'w')
            break
        except:
            pass

    for page_link in pages_links:
        logging.info('scraping page link {}'.format(page_link))
        create_dire('walmart_page')
        save_page(page_link,'walmart_page','walmart_page')
        while 1:
            try:
                products_links = products_links_graber(products_links)
                pyautogui.hotkey('ctrl', 'w')
                break
            except:
                pass
    for product_link in products_links:
        create_dire('products_page')
        save_page(product_link,'product_page','product_page')
        while 1:
            try:
                product_path = os.path.abspath(os.getcwd())+'\\saved_pages\\products_page\\product_page.html'
                product_data = product_scraper(product_path)
                mongo_service.update_by_link(collection_name, product_data)
                pyautogui.hotkey('ctrl', 'w')
                break
            except:
                pass
    logging.info('all_item_links length: {}'.format(len(products_links)))
    logging.info("End process")
    logging.info(f"End time : {datetime.now()}")
