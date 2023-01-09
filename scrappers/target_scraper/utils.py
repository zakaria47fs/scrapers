from selenium import webdriver as wd 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone

TZ_EST = timezone('EST')

def open_browser(driver_path):
    logging.info('Start browser')
    options = wd.ChromeOptions()
    #options.add_argument('--headless')
    driver = wd.Chrome(driver_path, chrome_options=options)
    url = "https://weeklyad.target.com"
    driver.get(url)
    driver.maximize_window()
    wait = WebDriverWait(driver,10)
    view_the_weekly_ad=wait.until(EC.element_to_be_clickable((By.XPATH,"//button[text()='View the Weekly Ad']")))
    view_the_weekly_ad_url=driver.current_url[:-1]+view_the_weekly_ad.get_attribute('href')
    driver.get(view_the_weekly_ad_url)
    view_by_category = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='category-view secondary-nav-text ng-scope']")))
    time.sleep(3) # Necessary to wait for full-href load
    view_by_category = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='category-view secondary-nav-text ng-scope']")))
    view_by_category_url = view_by_category.get_attribute('href')
    driver.get(view_by_category_url)
    return driver, wait


def get_eligible_links(driver, wait):
    '''Get the Sub Category & Eligibale Items Links'''
    driver = page_scroll(driver)
    wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@class="ng-binding"]')))
    eligible_items = driver.find_elements(By.XPATH,'//a[@class="ng-binding"]')
    eligible_links = []
    for eligible_item in eligible_items:
        sub_category = eligible_item.text
        eligible_item.click()
        Tab = driver.window_handles[1]
        driver.switch_to.window(Tab)
        link = driver.current_url
        if link not in eligible_links:
            eligible_links.append(link)
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
    # maximize page nums at 20 pages
    pages_num = min(items_num//24, 5)
    if '?' in link:
        for i in range(1,1+pages_num):
            links.append(link+f'&Nao={i*24}&moveTo=product-list-grid')
    else:
        for i in range(1,1+pages_num):
            links.append(link+f'?Nao={i*24}&moveTo=product-list-grid')
    return links


def product_get_info(driver, wait, primary_category, sub_category):

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

    #The ad is updated every Sunday between midnight and 2 a.m. Central time
    #https://help.target.com/help/subcategoryarticle?childcat=Weekly+Ad&parentcat=Promotions+%26+Coupons&searchQuery=search+help
    today = datetime.now(TZ_EST)
    sunday = today + timedelta( (6-today.weekday()) % 7 )
    expiry_date = sunday.replace(hour=1, minute=0, second=0, microsecond=0)
    try:
        discount_percent = round((1-float(new_price)/float(old_price))*100)
        if not 0<discount_percent<100:
            raise ValueError
    except:
        discount_percent = None
    
    product_info = {'primary_category': primary_category, 'sub_category': sub_category, 'product_title': product_title,
                    'product_brand': product_brand, 'old_price': old_price, 'new_price': new_price, 'link_url': link_url,
                    'thumbnail': thumbnail, 'description': description, 'created_at': datetime.now(TZ_EST), 'expiry_date': expiry_date,
                    'discount_percent': f'{discount_percent}%'}

    return product_info


def scrap_page(driver, wait):
    driver = page_scroll(driver)
    items_links = []
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    items_links = []
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    items_list = soup.find('section')
    items_list = items_list.find('div')
    items = items_list.find_all('div')
    for item in items:
        item_urls = item.find_all('a')
        for item_url in item_urls:
            if item_url['href'].endswith('#lnk=sametab') :
                if 'type=scroll_to_review_section#lnk=sametab' not in item_url['href']:
                    items_links.append('https://www.target.com'+item_url['href'])
    items_links=list(dict.fromkeys(items_links))
    return items_links


def get_category_links(driver,wait):
    wait.until(EC.visibility_of_element_located((By.XPATH,'//a[@class="ng-binding"]')))
    time.sleep(2)
    driver = page_scroll(driver)
    wait.until(EC.visibility_of_element_located((By.XPATH,'//a[@class="ng-binding"]')))
    category_links = []
    soup = BeautifulSoup(driver.page_source, 'lxml')
    categories_list = soup.find('div', class_="category-tiles")
    categories_links = categories_list.find_all('a', class_="ng-binding")
    for category in categories_links:
        category_links.append(driver.current_url+ '''&category_tree_id=''' + category['id'].split('-')[-1])
    return category_links
