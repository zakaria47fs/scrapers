from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils import get_pages_link,get_product_data,get_products_link
import pandas as pd
header = {'Primary Category': [], 'Sub Category': [],'Product Title': [],'Product Brand': [],'Old Price': [],'New Price': [],'Link URL': [] ,'Thumbnail': [],'Description': []}
df = pd.DataFrame(header)
#----------------------------------------

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
    df.loc[len(df.index)] = product_data
    df.to_csv('Amazon_Scraping.csv',index=False)