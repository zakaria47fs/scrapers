from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
from pytz import timezone

TZ_EST = timezone('EST')

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
        thumbnail = soup.find(id="landingImage")
        if thumbnail != None:
            thumbnail = thumbnail['src']
        else:
            thumbnail = soup.find(id="unrolledImgNo0")
            if thumbnail != None:
                img = soup.find("img")
                thumbnail = img['src'] 
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

    expiry_date = None
    #expiry_date = (datetime.now(TZ_EST) + timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        discount_percent = round((1-float(new_price)/float(old_price))*100)
        if not 0<discount_percent<100:
            raise ValueError
    except:
        discount_percent = None

    product_info = {'primary_category': primary_category, 'sub_category': sub_category, 'product_title': product_title,
                    'product_brand': product_brand, 'old_price': old_price,'new_price': new_price, 'link_url': link_url,
                    'thumbnail': thumbnail, 'description': description, 'created_at': datetime.now(), 'expiry_date': expiry_date,
                    'discount_percent': f'{discount_percent}%'}
    return driver,product_info

def get_pages_link(driver):
    pagelinks=[]
    pagelinks=[]
    pagenum = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div[21]/div/div/div/div[3]/div/ul/li[2]")))
    pagenum = pagenum.get_attribute("aria-label")
    pagenum = int(pagenum.split('of ')[-1])
    for i in range(pagenum):
        pagelinks.append(f"https://www.amazon.com/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A{60*i}%252C%2522presetId%2522%253A%2522AB48D68973BA06D9DFD05723DA760601%2522%252C%2522discountRanges%2522%253A%255B%257B%2522sectionText%2522%253A%2522Discount%2522%252C%2522optionText%2522%253A%252210%2525%2520off%2520or%2520more%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Discount%2522%252C%2522optionText%2522%253A%252225%2525%2520off%2520or%2520more%2522%252C%2522from%2522%253A25%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Discount%2522%252C%2522optionText%2522%253A%252250%2525%2520off%2520or%2520more%2522%252C%2522from%2522%253A50%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%252C%257B%2522sectionText%2522%253A%2522Discount%2522%252C%2522optionText%2522%253A%252270%2525%2520off%2520or%2520more%2522%252C%2522from%2522%253A70%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%255D%252C%2522prime%2522%253Atrue%252C%2522dealState%2522%253A%2522AVAILABLE%2522%252C%2522dealType%2522%253A%2522LIGHTNING_DEAL%2522%252C%2522sorting%2522%253A%2522BY_SCORE%2522%252C%2522starRating%2522%253A4%257D")
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


def open_browser(driver_path):
    logging.info('Start browser')
    options = wd.ChromeOptions()
    #options.add_argument('--headless')
    driver = wd.Chrome(driver_path, chrome_options=options)
    url = "https://www.amazon.com/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522AB48D68973BA06D9DFD05723DA760601%2522%252C%2522discountRanges%2522%253A%255B%257B%2522sectionText%2522%253A%2522Discount%2522%252C%2522optionText%2522%253A%252210%2525%2520off%2520or%2520more%2522%252C%2522from%2522%253A10%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Discount%2522%252C%2522optionText%2522%253A%252225%2525%2520off%2520or%2520more%2522%252C%2522from%2522%253A25%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%252C%257B%2522sectionText%2522%253A%2522Discount%2522%252C%2522optionText%2522%253A%252250%2525%2520off%2520or%2520more%2522%252C%2522from%2522%253A50%252C%2522to%2522%253Anull%252C%2522selected%2522%253Atrue%257D%252C%257B%2522sectionText%2522%253A%2522Discount%2522%252C%2522optionText%2522%253A%252270%2525%2520off%2520or%2520more%2522%252C%2522from%2522%253A70%252C%2522to%2522%253Anull%252C%2522selected%2522%253Afalse%257D%255D%252C%2522prime%2522%253Atrue%252C%2522dealState%2522%253A%2522AVAILABLE%2522%252C%2522dealType%2522%253A%2522LIGHTNING_DEAL%2522%252C%2522sorting%2522%253A%2522BY_SCORE%2522%252C%2522starRating%2522%253A4%257D"
    driver.get(url)
    driver.maximize_window()
    try:
        lightning_deals = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//*[text()='Lightning Deals']")))
        lightning_deals.click()
        available = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#grid-main-container > div.GridFilters-module__gridFilterSection_36xNFAVppWfx4i4otzVc2Y > span:nth-child(2) > ul > li:nth-child(2) > div > a")))
        available.click()
        discount50 = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#grid-main-container > div.GridFilters-module__gridFilterSection_36xNFAVppWfx4i4otzVc2Y > span:nth-child(4) > ul > li:nth-child(4) > div > a")))
        discount50.click()
        review = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#grid-main-container > div.GridFilters-module__gridFilterSection_36xNFAVppWfx4i4otzVc2Y > span:nth-child(5) > ul > li:nth-child(1) > div > a")))
        review.click()
    except:
        pass
    return driver
