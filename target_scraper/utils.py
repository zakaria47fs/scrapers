from selenium import webdriver as wd 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
import pandas as pd


header = {'Primary Category': [], 'Sub Category': [], 'Product Title': [],'Product Brand': [],'Old Price': [],'New Price': [],'Link URL': [] ,'Thumbnail': [],'Description': []}
df = pd.DataFrame(header)


def open_browser():
    driver = wd.Chrome('chromedriver')
    url = "https://weeklyad.target.com"
    driver.get(url)
    driver.maximize_window()
    wait = WebDriverWait(driver,10)
    View_the_Weekly_Ad=wait.until(EC.visibility_of_element_located((By.XPATH,"//button[text()='View the Weekly Ad']")))
    View_the_Weekly_Ad_url=driver.current_url[:-1]+View_the_Weekly_Ad.get_attribute('href')
    driver.get(View_the_Weekly_Ad_url)
    View_by_Category = wait.until(EC.visibility_of_element_located((By.XPATH,"//a[@class='category-view secondary-nav-text ng-scope']")))
    View_by_Category_url = View_by_Category.get_attribute('href')
    driver.get(View_by_Category_url)

    return driver, wait


def Get_Eligible_Links(driver, wait):#changed
    '''Get the Primary Category & Eligibale Items Links'''
    Eligible_Items = wait.until(EC.element_to_be_clickable((By.XPATH,'//button[@class="btn btn-sm btn-primary"]')))
    Eligible_Items = driver.find_elements(By.XPATH,'//button[@class="btn btn-sm btn-primary"]')
    Eligible_Links=[]
    for Eligible_Item in Eligible_Items:
        Eligible_Item.click()
        Tab = driver.window_handles[1]
        driver.switch_to.window(Tab)
        Eligible_Links.append(driver.current_url)
        driver.close()
        Tab = driver.window_handles[0]
        driver.switch_to.window(Tab)
    return driver, Eligible_Links
        
        
def Page_Scroll(driver):
    "Scroll to the Bottom of Page"
    hight=100
    page_hight = driver.execute_script("return document.body.scrollHeight")
    while hight<page_hight:
        page_hight = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script(f"window.scrollTo(0,{hight})")
        time.sleep(0.5)
        hight += 100
        

def Get_Page_Links(driver, wait):
    links=[]
    Items_Num=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@data-test="resultsHeading"]')))
    Items_Num=int(Items_Num.text.split()[0])
    link = driver.current_url
    links.append(link)
    if '?' in link:
        for i in range(1,1+Items_Num//24):
            links.append(link+f'&Nao={i*24}&moveTo=product-list-grid')
    else:
        for i in range(1,1+Items_Num//24):
            links.append(link+f'?Nao={i*24}&moveTo=product-list-grid')
    return links


def Product_Get_Info(driver, wait, Primary_Category):
    try:
        New_Price = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@data-test='product-price']")))
        New_Price = New_Price.text
    except:
        New_Price =''
    
    try:
        Old_Price = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-test="product-regular-price"]')))
        Old_Price = Old_Price.text
        Old_Price = Old_Price.replace('reg ','')
    except:
        Old_Price =''
        
    try:
        Show_More = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@data-test='toggleContentButton']")))
        Show_More.click()

        Description = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@data-test='item-details-description']")))
        Description = Description.text[:350]
    except:
        Description=''
    
    try:
        Product_Title = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[@data-test='product-title']")))
        Product_Title =Product_Title.text
    except:
        Product_Title =''
    
    try:
        Link_URL = driver.current_url
    except:
        Link_URL =''
    
    try:
        Product_Brand = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[starts-with(., "Shop all ")]')))
        Product_Brand = Product_Brand.text.split()
        Product_Brand = ' '.join(Product_Brand[2:])
    except:
        Product_Brand =''
    
    try:
        Thumbnail = wait.until(EC.visibility_of_element_located((By.XPATH,'//button[@data-test="product-carousel-thumb-0"]//img')))
        Thumbnail = Thumbnail.get_attribute('src')
    except:
        Thumbnail =''
    
    Products_info=[Primary_Category,Product_Title,Product_Brand,Old_Price,New_Price,Link_URL,Thumbnail,Description]
    df.loc[len(df.index)]= Products_info
    df.to_csv('Target_Scraping.csv',index=False)


def Page_Crawler(driver, tab_url, Primary_Category):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(tab_url)
    Product_Get_Info(driver, Primary_Category)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


    
def Scrap_Page(driver, wait, Primary_Category):
    Page_Scroll(driver)
    Products = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@data-test='product-title']")))
    Products = driver.find_elements(By.XPATH, "//a[@data-test='product-title']")
    for Product in range(0,len(Products)-1):
        #sometime the page reload so we need to get Products every time
        Products = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@data-test='product-title']")))
        Products = driver.find_elements(By.XPATH, "//a[@data-test='product-title']")
        Page_Crawler(driver, Products[Product].get_attribute('href'), Primary_Category) 
