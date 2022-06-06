import threading, os, time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager


choice = input("Сохранять сессию или нет? [y / n]: ")
choice = True if choice == 'y' else False

ALL_PROFILES = 3
URL = "https://temp-mail.org"

prefix_for_profiles = 'Test'
chrome_profile_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '\\\\') + '\\Profile Data'

os.system('taskkill /F /IM chrome.exe /T > nul 2>&1')
os.system('taskkill /F /IM chromedriver.exe /T > nul 2>&1')


def open_browser_with_new_profile_with_saving_session(number):
    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("allow-profiles-outside-user-dir")
    
    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    options.add_argument(f"--user-data-dir={chrome_profile_path}\\Profile{number}")
    options.add_argument(f"--profile-directory={prefix_for_profiles}{number}")
    
    web = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    web.get(URL)


def open_browser_with_new_profile_without_saving_session(number):
    options = webdriver.ChromeOptions()

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
    if choice:
        threads.append(threading.Thread(target=open_browser_with_new_profile_with_saving_session, args=(number, )))
    else:
        threads.append(threading.Thread(target=open_browser_with_new_profile_without_saving_session, args=(number, )))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

os.system('cls||clear')
print(f'Успешно открыто {ALL_PROFILES} профилей.')
