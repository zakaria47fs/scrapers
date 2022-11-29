from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup

def get_product_data(driver):
    page_source = driver.page_source
    link_url = driver.current_url
    soup = BeautifulSoup(page_source, 'lxml')
    price_container = soup.find(id="centerCol")
    try:
        new_price = price_container.find('span',class_='a-offscreen').text
    except:
        new_price = ''
    try:
        old_price = price_container.find(attrs={"data-a-strike":"true"})
        old_price = old_price.find(attrs={"aria-hidden":"true"}).text
    except:
        old_price = ''
    if  old_price == new_price and '$' in old_price:
        prices = price_container.find_all('span',class_='a-offscreen')
        price_list = []
        for price in prices:
            price_list.append(price.text)
        if price_list[0]==price_list[1]:
            price_list[1] = price_list[2]
        if float(price_list[0].replace('$',''))>float(price_list[1].replace('$','')):
            new_price = price_list[1]
            old_price = price_list[0]
        else:
            new_price = price_list[0]
            old_price = price_list[1]
    if price_container.find('span',class_="a-price-range")!=None:
        new_price_list = price_container.find('span',class_="a-price-range").text.replace(' ','').split('$')
        new_price = '$'+new_price_list[2]+'$'+new_price_list[3]    
    
    try:
        if soup.find(id="landingImage") == None:
            thumbnail = soup.find(id="imgBlkFront")['src']
        else:
            thumbnail = soup.find(id="landingImage")['src']
    except:
        thumbnail = ''
    try:
        if soup.find(id="featurebullets_feature_div")==None:
            description = soup.find('div',class_="a-expander-content a-expander-partial-collapse-content").get_text()
        else:
            description = soup.find(id="featurebullets_feature_div").get_text()
        description = description.replace('\n','').replace('About this item','').replace('› See more product details','')
        description = description.replace('Make sure this fits by entering your model number.','')
        description = description.replace('This fits your','')
        description = description.replace('\xa0.','')
        description = description.strip()[:350]
    except:
        description = ''

    try:    
        brand = soup.find(id="bylineInfo")
        if brand != None:
            product_brand = brand.get_text().split('the')[-1].split('Store')[0].strip()
            product_brand = product_brand.split('Brand:')[-1].strip()
            product_brand = product_brand.replace(', and more.   See search results for this author','')
            product_brand = product_brand.replace('author','').strip()
        brand = soup.find(id="amznStoresBylineLogoTextContainer")
        if brand != None:
            product_brand = brand.get_text()
            product_brand = product_brand.split('Visit the Store')[0].strip()
        if 'Actor' in product_brand :
            product_container = soup.find(id="detailBullets_feature_div")
            lis = product_container.find_all('li')
            for li in lis:
                if 'Studio' in li.get_text():
                    product_brand = li.get_text().split('Studio')[-1].replace(' ','').split()[-1]
    except:
        product_brand = ''
    try:
        title = soup.find(id="productTitle")
        product_title = title.get_text().strip()
    except:
         product_title = ''
    try:
        category_container = soup.find(id="wayfinding-breadcrumbs_container")
        categories = category_container.find_all('a')
        category_list = []
        for category in categories:
            category_list.append(category.get_text().replace('\n','').strip())
        primary_category = category_list[0]
        sub_category = category_list[1]
    except:
        primary_category = ''
        sub_category = ''
    product_data =[primary_category, sub_category, product_title,product_brand,old_price,new_price,link_url,thumbnail,description]
    return driver,product_data

def get_pages_link(driver):
    pagelinks=[]
    pageurl = driver.current_url
    pagesurl = pageurl.split('A0')
    pagenum = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#slot-7 > div > div > div.GridContainer-module__gridFooter_VLpWMDEvOFj3taV1CiY8J > div > ul > li.a-selected")))
    pagenum = pagenum.get_attribute("aria-label")
    pagenum = int(pagenum.split('of ')[-1])
    for i in range(pagenum):
        pagelinks.append(pagesurl[0]+'A'+str(i)+pagesurl[1])
    return driver,pagelinks

def get_products_link(driver,pagelinks):
    productslinks = []
    for pagelink in pagelinks:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        driver.get(pagelink)
        product_container = soup.find('div',class_="Grid-module__gridDisplayGrid_2X7cDTY7pjoTwwvSRQbt9Y")
        all_products_links  = product_container.find_all('a',class_="a-link-normal DealCardDynamic-module__linkOutlineOffset_2XU8RDGmNg2HG1E-ESseNq")
        for products_link in all_products_links:
            productslinks.append(products_link['href'])
    return driver,productslinks