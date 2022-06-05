import threading, os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager


# ANTI_LAG_DELAY = 1 # nwm
ALL_PROFILES = 5
URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

brave_binary_path = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'

os.system('taskkill /F /IM chrome.exe /T > nul')
os.system('taskkill /F /IM chromedriver.exe /T > nul')


def open_browser_with_new_profile(number):
    options = webdriver.ChromeOptions()
    
    options.binary_location = brave_binary_path

    options.add_argument('--start-maximized')
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    web = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    web.get(URL)


threads = [

]

for number in range(ALL_PROFILES):
    threads.append(threading.Thread(target=open_browser_with_new_profile, args=(number, )))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f'Успешно открыто {ALL_PROFILES} профилей.')
