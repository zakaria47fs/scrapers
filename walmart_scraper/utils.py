import webbrowser
import pyautogui
import pyperclip
import time
import os
import requests
import shutil
import logging
from bs4 import BeautifulSoup, Comment
import win32com.shell.shell as shell
# save webpage 
def save_page(url,file_name,page_type):
    #proxy_rotation()
    logging.info('Start browser')
    webbrowser.open(url)
    time.sleep(5)
    for i in range(0,20):
        pyautogui.press('space')
    # To simulate a Save As dialog. You can remove this since you'll be saving/downloading a file from a link
    pyautogui.hotkey('ctrl', 's')
    # Wait for the Save As dialog to load. Might need to increase the wait time on slower machines
    time.sleep(2)
    # File path + name
    if page_type=='walmart_page':
        file_path = os.path.abspath(os.getcwd())+'\\saved_pages\\walmart_page'+f'\\{file_name}.html'
    else :
        file_path = os.path.abspath(os.getcwd())+'\\saved_pages\\products_page'+f'\\{file_name}.html'
    # Type the file path and name is Save AS dialog
    pyperclip.copy(file_path)
    pyautogui.hotkey("ctrl", "v")
    #Hit Enter to save
    pyautogui.hotkey('enter')
    time.sleep(2)

# get page number

def page_num_graber():
    file_path = os.path.abspath(os.getcwd())+'\\saved_pages\\walmart_page\\walmart_page.html'
    soup=soup_maker(file_path)
    try:
        pages_num_ul=soup.find('ul',class_='list flex items-center justify-center pa0')
        pages_num_lis=pages_num_ul.find_all('li')
        pages_num_list = []
        for page_num_li in pages_num_lis:
            pages_num_list.append(page_num_li.text)
        pages_num=[]
        for page_num_list in pages_num_list:
            try:
                pages_num.append(int(page_num_list))
            except:
                pass
        pages_num = max(pages_num)
    except:
        pages_num = 1
    return pages_num

# get page links

def pages_links_graber(pages_num):
    pages_links=[]
    page_num = 1
    while page_num <= pages_num :
        pages_links.append(f'https://www.walmart.com/shop/deals/trending-flash-picks?affinityOverride=default&page={page_num}')
        page_num+=1
    return pages_links

# parse page

def soup_maker(file_path):
    # Opening the html file
    HTMLFile = open(file_path,encoding="utf8")

    # Reading the file
    index = HTMLFile.read()

    # Creating a BeautifulSoup object and specifying the parser
    soup = BeautifulSoup(index, 'lxml')
    return soup

# create / delete directory

def create_dire(page_type):
    path = os.path.abspath(os.getcwd())
    if page_type=='walmart_page':
        path = path+'\\saved_pages\\walmart_page'
    else:
        path = path+'\\saved_pages\\products_page'
    try:
        # delet directory
        shutil.rmtree(path)
    except :
        # directory doesn't exists
        pass    
    try:
        # create directory
        os.makedirs(path)
    except :
        # directory already exists
        pass
    
# product info

def product_scraper(file_path):
    soup=soup_maker(file_path)
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    try:
        link_url = 'https:'+comments[0].split('https:')[1]
    except:
        link_url =''
    try:
        product_title = soup.find('h1',class_="b lh-copy dark-gray mt1 mb2 f3").get_text()
    except:
        product_title = ''
    try:
        product_brand  = soup.find('a',class_='bg-transparent bn lh-solid pa0 sans-serif tc underline inline-button mid-gray pointer f6').get_text()
    except:
        product_brand  = ''
    try:
        new_price = soup.find('span',class_="inline-flex flex-column").get_text()
        new_price = new_price.split('Now ')[-1]
    except:
        new_price = ''
    try:
        old_price = soup.find('span',class_="mr2 f6 gray strike").get_text()
    except:
        old_price = ''
    try:
        description = soup.find('div',class_="dangerous-html mb3").get_text().replace('Description','').replace(' ','').replace('\xa0','')
        description = description[:350]
    except:
        description =''
    try:
        category = soup.find_all('a',class_="w_MSFl gray underline")
        primary_category = category[0].get_text()
        sub_category = category[1].get_text()
    except:
        primary_category = ''
        sub_category = ''
    try:
        thumbnail = soup.find('img',class_='noselect db')['src']
        thumbnail = soup.find('img',class_='noselect db')['src']
        thumbnail = thumbnail.replace('./product_page_files/','').replace('(1)','')
        thumbnail = 'https://i5.walmartimages.com/asr/'+thumbnail
    except:
        thumbnail =''
    product_data = {'primary_category': primary_category, 'sub_category': sub_category, 'product_title': product_title,
                    'product_brand': product_brand, 'old_price': old_price,'new_price': new_price, 'link_url': link_url,
                    'thumbnail': thumbnail, 'description': description}
    return product_data

# products link from pages

def products_link_graber(soup):
    products = soup.find_all('a',class_='absolute w-100 h-100 z-1 hide-sibling-opacity')
    product_links=[]
    for product in products:
        product_links.append(product['href'])
    return product_links

# proxy roration 

def proxy_cmd(proxy):
    command = 'netsh winhttp reset proxy'
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+command)
    command = f'netsh winhttp set proxy {proxy}'
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+command)

def proxy_rotation():
    url = "http://httpbin.org/ip"
    proxies = []

    for proxy in proxies:
        try:
            response = requests.get(url, proxies = {"http":proxy, "https":proxy})
            break
        except:
            pass
    proxy_cmd(proxy)
