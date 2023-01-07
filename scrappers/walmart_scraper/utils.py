import webbrowser
import pyautogui
import pyperclip
import time
import os
import json
import shutil
import logging
from bs4 import BeautifulSoup
import requests
from random import randint,uniform
import win32com.shell.shell as shell
from datetime import datetime, timedelta
from pytz import timezone

TZ_EST = timezone('EST')
PROXY_API_KEY = "pn38574a8d73ce40pfr7fq9e2sgyfnamb8kekd4x"

# save webpage 
def save_page(url,file_name,page_type):
    proxy_rotation()
    time.sleep(uniform(1,1.5))
    logging.info('Start browser')
    webbrowser.open(url)
    time.sleep(5)
    for i in range(0,30):
        pyautogui.press('space')
    # To simulate a Save As dialog. You can remove this since you'll be saving/downloading a file from a link
    pyautogui.hotkey('ctrl', 's')
    # Wait for the Save As dialog to load. Might need to increase the wait time on slower machines
    time.sleep(2)
    # File path + name
    if page_type=='walmart_page' :
        file_path = os.path.abspath(os.getcwd())+'\\saved_pages\\walmart_page'+f'\\{file_name}.html'
        pyperclip.copy(file_path)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("tab")
        pyautogui.hotkey("down")
        pyautogui.hotkey("up")
        #Hit Enter to save
        pyautogui.hotkey('enter')
        pyautogui.hotkey('enter')
        time.sleep(2)
    elif page_type=='product_page':
        file_path = os.path.abspath(os.getcwd())+'\\saved_pages\\products_page'+f'\\{file_name}.html'
        # Type the file path and name is Save AS dialog
        pyperclip.copy(file_path)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("tab")
        pyautogui.hotkey("down")
        pyautogui.hotkey("up")
        #Hit Enter to save
        pyautogui.hotkey('enter')
        pyautogui.hotkey('enter')
        time.sleep(2)

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
    
def product_scraper(file_path):
    soup=soup_maker(file_path)
    try:
        link_url = soup.find("meta",property="og:url")['content']
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
        txt = soup.find('head').find_all('script')
        data = json.loads(txt[2].get_text())
        description = data["description"].replace('<br>','').replace('<b>','').replace('<p>','').replace('<strong>','')
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
        thumbnail = soup.find('img','loading'=="eager")['srcset'].split('1x,\n          ')[-1].replace(' 2x','')
    except:
        thumbnail =''

    expiry_date = (datetime.now(TZ_EST) + timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        discount_percent = round((1-float(new_price)/float(old_price))*100)
        if not 0<discount_percent<100:
            raise ValueError
    except:
        discount_percent = None

    product_data = {'primary_category': primary_category, 'sub_category': sub_category, 'product_title': product_title,
                    'product_brand': product_brand, 'old_price': old_price,'new_price': new_price, 'link_url': link_url,
                    'thumbnail': thumbnail, 'description': description, 'created_at': datetime.now(), 'expiry_date': expiry_date,
                    'discount_percent': f'{discount_percent}%'}
    return product_data

def soup_maker(file_path):
    # Opening the html file
    HTMLFile = open(file_path,encoding="utf8")

    # Reading the file
    index = HTMLFile.read()

    # Creating a BeautifulSoup object and specifying the parser
    soup = BeautifulSoup(index, 'lxml')
    return soup

def pages_links_graber(max_page):
    pages_links=[]
    for page_num in range(1,max_page+1):
        pages_links.append(f'https://www.walmart.com/shop/deals/trending-flash-picks?page={page_num}')
    return pages_links

def max_page_graber():
    file_path = os.path.abspath(os.getcwd())+'\\saved_pages\\walmart_page\\walmart_page.html'  
    soup = soup_maker(file_path)
    next_data = soup.find(id="__NEXT_DATA__").text
    data = json.loads(next_data)
    max_page = data['props']['pageProps']['initialData']['searchResult']['paginationV2']['maxPage']
    return max_page

def products_links_graber(products_links):
    file_path = os.path.abspath(os.getcwd())+'\\saved_pages\\walmart_page\\walmart_page.html'  
    soup = soup_maker(file_path)
    next_data = soup.find(id="__NEXT_DATA__").text
    data = json.loads(next_data)
    products_dic = data['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items']
    for product_dic in products_dic:
        products_links.append('https://www.walmart.com/'+product_dic['canonicalUrl'])
    return products_links

# proxy roration 

def proxy_cmd(proxy):
    command = 'netsh winhttp reset proxy'
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+command)
    command = f'netsh winhttp set proxy {proxy}'
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+command)

def get_proxies():
    r = requests.get("https://proxy.webshare.io/api/proxy/list/?page=1&countries=US-FR", headers={"Authorization": PROXY_API_KEY})
    data = r.json()
    proxies = []
    for proxy in data['results']:
        proxies.append(str(proxy['proxy_address'])+':'+str(proxy['ports']['http']))
    return proxies    

def proxy_rotation():
    url = "http://httpbin.org/ip"
    proxies = get_proxies()
    proxy = proxies[randint(0,len(proxies)-1)]
    while 1:
        try:
            requests.get(url, proxies = {"http":proxy, "https":proxy})
            break
        except:
            pass
    proxy_cmd(proxy)
