import pyautogui
import os
from utils import create_dire,save_page,page_num_graber,pages_links_graber,soup_maker,products_link_graber,product_scraper
import logging
from services.mongo_service import MongoService
from datetime import datetime

# logging configuration
logging.basicConfig(filename='log_app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

mongo_service = MongoService()
collection_name = 'walmart_db'

if __name__=='__main__':
    logging.info(f"Start time : {datetime.now()}")
    create_dire('walmart_page')
    save_page('https://www.walmart.com/shop/deals/trending-flash-picks?affinityOverride=default','walmart_page','walmart_page')
    all_item_links = 1
    while 1:
        try:
            pages_num = page_num_graber()
            break
        except:
            pass
    pages_links = pages_links_graber(pages_num)
    pyautogui.hotkey('ctrl', 'w')
    for page_link in pages_links:
        logging.info('scraping page link {}'.format(page_link))
        create_dire('walmart_page')
        save_page(page_link,'walmart_page','walmart_page')
        while 1:
            try:
                file_path = os.path.abspath(os.getcwd())+'\\saved_pages\\walmart_page\\walmart_page.html'
                soup = soup_maker(file_path)
                pyautogui.hotkey('ctrl', 'w')
                product_links = products_link_graber(soup)
                for product_link in product_links:
                    all_item_links = all_item_links+1
                    logging.info('Scrape product: {}'.format(product_link))
                    create_dire('products_page')
                    save_page(product_link,'product_page','products_page')
                    while 1:
                        try:
                            product_path = os.path.abspath(os.getcwd())+'\\saved_pages\\products_page\\product_page.html'
                            soup = soup_maker(product_path)
                            product_data = product_scraper(product_path)
                            mongo_service.update_by_link(collection_name, product_data)
                            break
                        except:
                            pass
                    pyautogui.hotkey('ctrl', 'w')
                break
            except:
                pass
    logging.info('all_item_links length: {}'.format(all_item_links))
    logging.info("End process")
    logging.info(f"End time : {datetime.now()}")
