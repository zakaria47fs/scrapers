from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils import get_pages_link,get_product_data,get_products_link
import pandas as pd

from services.mongo_service import MongoService


# logging configuration
logging.basicConfig(filename='log_app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

mongo_service = MongoService()
collection_name = 'amazon_db'


#Getting To Categories Page
driver, wait = open_browser(driver_path='chromedriver --max_old_space_size=4096')


if __name__=='__main__':
  driver = wd.Chrome('C:\Program Files (x86)\chromedriver.exe')
  url = "https://www.amazon.com/gp/goldbox?ref_=nav_cs_gb"
  driver.get(url)
  driver.maximize_window()
  lightning_deals = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//*[text()='Lightning Deals']")))
  lightning_deals.click()
  available = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#grid-main-container > div.GridFilters-module__gridFilterSection_36xNFAVppWfx4i4otzVc2Y > span:nth-child(2) > ul > li:nth-child(2) > div > a")))
  available.click()
  discount50 = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#grid-main-container > div.GridFilters-module__gridFilterSection_36xNFAVppWfx4i4otzVc2Y > span:nth-child(4) > ul > li:nth-child(4) > div > a")))
  discount50.click()
  review = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#grid-main-container > div.GridFilters-module__gridFilterSection_36xNFAVppWfx4i4otzVc2Y > span:nth-child(5) > ul > li:nth-child(1) > div > a")))
  review.click()

  driver,page_links = get_pages_link(driver)
  driver,productslinks = get_products_link(driver,page_links)

  for productslink in productslinks:
      driver.get(productslink)
      driver,product_data = get_product_data(driver)
      # push product info to DB
      mongo_service.update_by_link(collection_name, product_data)
      logging.info('all_item_links length: {}'.format(len(all_item_links)))

    logging.info("End process")
