from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging
from datetime import datetime, timedelta

from target_scraper.utils import get_category_links, get_eligible_links, get_page_links, scrap_page, open_browser, product_get_info, TZ_EST
from services.mongo_service import MongoService


# logging configuration
logging.basicConfig(filename='target_scraper/log_app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

mongo_service = MongoService()
collection_name = 'target_db'


#Getting To Categories Page
driver, wait = open_browser(driver_path='chromedriver --max_old_space_size=4096')


if __name__=='__main__':
    logging.info(f"Start time : {datetime.now()}")

    #Scraping Categories Links And filling Category_links ARRAY  
    category_links = get_category_links(driver, wait)
    all_item_links = []
    all_eligible_links = []
    
    for category_link in category_links:
        logging.info('scraping category {}'.format(category_link))
        driver.get(category_link)
        try:
            primary_category = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[starts-with(., "shop ")]')))
            primary_category = ' '.join(primary_category.text.split()[1:])
        except:
            primary_Category = ''
        driver, eligible_links, sub_category = get_eligible_links(driver, wait)
        for eligible_link in eligible_links:
            
            # filter duplicates
            if eligible_link in all_eligible_links:
                logging.info("duplicate eligible_link {}".format(eligible_link))
                continue
            else:
                all_eligible_links.append(eligible_link)

            logging.info('scraping eligible link {}'.format(eligible_link))
            driver.get(eligible_link)
            try:
                show_all = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[text()='Show all']")))
                show_all_url = show_all.get_attribute('href')
                driver.get(show_all_url)
            except:
                pass
            page_links = get_page_links(driver, wait)
            items_links = []
            for link in page_links:
                driver.get(link)
                items_links=items_links+scrap_page(driver, wait)

            #filter duplicates
            filtred_items_links = []
            for item in items_links:
                if item in all_item_links:
                    logging.info("duplicate {}".format(item))
                else:
                    filtred_items_links.append(item)
                    all_item_links.append(item)

            for item_link in filtred_items_links:
                logging.info('Scrape product: {}'.format(item_link))
                driver.get(item_link)
                product_data = product_get_info(driver,wait, primary_category,sub_category)
                # push product info to DB
                mongo_service.update_by_link(collection_name, product_data)

            logging.info('all_item_links length: {}'.format(len(all_item_links)))
    logging.info(f"End time : {datetime.now()}")
    logging.info("End process")
