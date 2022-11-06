from selenium import webdriver as wd 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
import logging
import pandas as pd
from bs4 import BeautifulSoup

header = {'Primary Category': [], 'Sub Category': [], 'Product Title': [],'Product Brand': [],'Old Price': [],'New Price': [],'Link URL': [] ,'Thumbnail': [],'Description': []}
df = pd.DataFrame(header)


def open_browser(driver_path):
    driver = wd.Chrome(driver_path)
    url = "https://weeklyad.target.com"
    driver.get(url)
    driver.maximize_window()
    wait = WebDriverWait(driver,20)
    view_the_weekly_ad=wait.until(EC.element_to_be_clickable((By.XPATH,"//button[text()='View the Weekly Ad']")))
    view_the_weekly_ad_url=driver.current_url[:-1]+view_the_weekly_ad.get_attribute('href')
    driver.get(view_the_weekly_ad_url)
    view_by_category = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='category-view secondary-nav-text ng-scope']")))
    view_by_category_url = view_by_category.get_attribute('href')
    driver.get(view_by_category_url)

    return driver, wait


def get_eligible_links(driver, wait):
    '''Get the Sub Category & Eligibale Items Links'''
    page_scroll(driver)
    wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@class="ng-binding"]')))
    eligible_items = driver.find_elements(By.XPATH,'//a[@class="ng-binding"]')
    eligible_links = []
    for eligible_item in eligible_items:
        sub_category = eligible_item.text
        eligible_item.click()
        Tab = driver.window_handles[1]
        driver.switch_to.window(Tab)
        eligible_links.append(driver.current_url)
        driver.close()
        Tab = driver.window_handles[0]
        driver.switch_to.window(Tab)
    return driver, eligible_links , sub_category
        
        
def page_scroll(driver):
    "Scroll to the Bottom of Page"
    hight = 100
    page_hight = driver.execute_script("return document.body.scrollHeight")
    while hight<page_hight:
        page_hight = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script(f"window.scrollTo(0,{hight})")
        time.sleep(0.5)
        hight += 100
    return driver
        

def get_page_links(driver, wait):
    links = []
    items_num = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@data-test="resultsHeading"]')))
    items_num = int(items_num.text.split()[0])
    link = driver.current_url
    links.append(link)
    if '?' in link:
        for i in range(1,1+items_num//24):
            links.append(link+f'&Nao={i*24}&moveTo=product-list-grid')
    else:
        for i in range(1,1+items_num//24):
            links.append(link+f'?Nao={i*24}&moveTo=product-list-grid')
    return links


def product_get_info(driver, wait, primary_category,sub_category):

    try:
        show_more = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@data-test='toggleContentButton']")))
        show_more.click()

        description = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-test='item-details-description']")))
        description = description.text[:350]
    except:
        description = ''

    try:
        new_price = driver.find_element(By.XPATH, "//span[@data-test='product-price']")
        new_price = new_price.text
    except:
        new_price = ''
    
    try:
        old_price = driver.find_element(By.XPATH, '//*[@data-test="product-regular-price"]')
        old_price = old_price.text
        old_price = old_price.replace('reg ','')
    except:
        old_price = ''
        
    try:
        product_title = driver.find_element(By.XPATH, "//h1[@data-test='product-title']")
        product_title = product_title.text
    except:
        product_title = ''
    
    try:
        link_url = driver.current_url
    except:
        link_url = ''
    
    try:
        product_brand = driver.find_element(By.XPATH, '//*[starts-with(., "Shop all ")]')
        product_brand = product_brand.text.split()
        product_brand = ' '.join(product_brand[2:])
    except:
        product_brand =''
    
    try:
        thumbnail = driver.find_element(By.XPATH,'//button[@data-test="product-carousel-thumb-0"]//img')
        thumbnail = thumbnail.get_attribute('src')
    except:
        thumbnail =''
    
    products_info = [primary_category,sub_category,product_title,product_brand,old_price,new_price,link_url,thumbnail,description]
    df.loc[len(df.index)] = products_info
    df.to_csv('target_scraping.csv',index=False)

    
def scrap_page(driver, wait):
    driver = page_scroll(driver)
    items_links = []
    wait.until(EC.visibility_of_element_located((By.XPATH,"//a[@data-test='product-title']")))
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    items_list = soup.find('section', class_="styles__StyledRowWrapper-sc-z8946b-1 cvsMwU")
    items = items_list.find_all('a', class_="Link__StyledLink-sc-frmop1-0 styles__StyledTitleLink-sc-h3r0um-1 iMNANe dcAXAu h-display-block h-text-bold h-text-bs")
    for item in items:
        items_links.append('https://www.target.com'+item['href'])
    return items_links

def get_category_links(driver,wait):
    time.sleep(2)  # wait page to refresh
    wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[3]/main/div[2]/div/section/div[2]/ul/li/div/div/a')))
    driver = page_scroll(driver)
    wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[3]/main/div[2]/div/section/div[2]/ul/li/div/div/a')))
    page_source = driver.page_source
    category_links = []
    soup = BeautifulSoup(page_source, 'lxml')
    categories_list = soup.find('div', class_="category-tiles")
    categories_links = categories_list.find_all('a', class_="ng-binding")
    for category in categories_links:
        category_links.append(driver.current_url+ '''&category_tree_id='''+category['id'].split('-')[-1])
    return  category_links