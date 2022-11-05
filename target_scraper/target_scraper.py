from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

from utils import Page_Scroll, Get_Eligible_Links, Get_Page_Links, Scrap_Page, open_browser


# logging configuration
logging.basicConfig(filename='log_app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


#Getting To Categories Page
driver, wait = open_browser()

#----------------------------------
#Scraping Categories Links And filling Category_links ARRAY  
Category_links=[]
Page_Scroll(driver)
Categories = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[3]/main/div[2]/div/section/div[2]/ul/li/div/div/a')))
Categories = driver.find_elements(By.XPATH,'/html/body/div[3]/main/div[2]/div/section/div[2]/ul/li/div/div/a')
for Category in range(0,len(Categories)-1):
    #sometime the page reload so we need to get Categories every time
    Categories = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[3]/main/div[2]/div/section/div[2]/ul/li/div/div/a')))
    Categories = driver.find_elements(By.XPATH,'/html/body/div[3]/main/div[2]/div/section/div[2]/ul/li/div/div/a')
    Category_id = Categories[Category].get_attribute('id')
    Category_links.append(driver.current_url+ '''&category_tree_id='''+Category_id.split('-')[1])

for Category_link in Category_links:
    driver.get(Category_link)
    try:
        Primary_Category=wait.until(EC.visibility_of_element_located((By.XPATH,'//*[starts-with(., "shop ")]')))
        Primary_Category=' '.join(Primary_Category.text.split()[1:])
    except:
        Primary_Category=''
    driver, Eligible_Links = Get_Eligible_Links(driver, wait)
    for Eligible_Link in Eligible_Links:
        driver.get(Eligible_Link)
        try:
            Show_all = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[text()='Show all']")))
            Show_all_url=Show_all.get_attribute('href')
            driver.get(Show_all_url)
        except:
            pass
        Page_Links = Get_Page_Links(driver, wait)
    for link in Page_Links:
        driver.get(link)
        Scrap_Page(driver, wait, Primary_Category)


