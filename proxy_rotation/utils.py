import os
import shutil
from random import randint,uniform
import requests
import time

PROXY_API_KEY = "pn38574a8d73ce40pfr7fq9e2sgyfnamb8kekd4x"


def proxy_rotation():
    command = 'cmd /c'+'''reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f
taskkill /f /im SystemSettings.exe && start ms-settings:network-proxy
taskkill /f /im SystemSettings.exe'''
    os.system(command)
    time.sleep(2)
    proxy = get_proxie()
    command= 'cmd /c'+f'''reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d {proxy} /f
taskkill /f /im SystemSettings.exe && start ms-settings:network-proxy
taskkill /f /im SystemSettings.exe'''
    os.system(command)
    command = 'cmd /c'+'''reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f
taskkill /f /im SystemSettings.exe && start ms-settings:network-proxy
taskkill /f /im SystemSettings.exe'''
    os.system(command)
def get_proxie():
    r = requests.get("https://proxy.webshare.io/api/proxy/list/?page=1&countries=US-FR", headers={"Authorization": PROXY_API_KEY})
    data = r.json()
    proxies = []
    for proxy in data['results']:
        proxies.append(str(proxy['proxy_address'])+':'+str(proxy['ports']['http']))
    return proxies[randint(0,len(proxies)-1)]  
