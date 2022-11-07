from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

from utils import get_category_links, get_eligible_links, get_page_links, scrap_page, open_browser, product_get_info
from mongo_service import MongoService


# logging configuration
logging.basicConfig(filename='log_app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

mongo_service = MongoService()
collection_name = 'target_db'


#Getting To Categories Page
driver, wait = open_browser(driver_path='chromedriver --max_old_space_size=4096')

#Scraping Categories Links And filling Category_links ARRAY  
category_links = get_category_links(driver, wait)
for category_link in category_links:
    driver.get(category_link)
    try:
        primary_category = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[starts-with(., "shop ")]')))
        primary_category = ' '.join(primary_category.text.split()[1:])
    except:
        primary_Category = ''
    driver, eligible_links, sub_category = get_eligible_links(driver, wait)
    for eligible_link in eligible_links:
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
        for item_link in items_links:
            logging.info('Scrape product: {}'.format(item_link))
            driver.get(item_link)
            product_data = product_get_info(driver,wait, primary_category,sub_category)
            # push product info to DB
            mongo_service.add_one_db(collection_name, product_data)
