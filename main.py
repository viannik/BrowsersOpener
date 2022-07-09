import os
import time
import subprocess

ANTI_LAG_DELAY = 0.5  # CONST

dict_of_browsers = {
    '0': ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data'],
    '1': ['C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe', os.getenv('LOCALAPPDATA') + '\\BraveSoftware\\Brave-Browser\\User Data'],
    '2': [os.getenv('LOCALAPPDATA') + '\\Chromium\\Application\\chrome.exe', os.getenv('LOCALAPPDATA') + '\\Chromium\\User Data']
}

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

browser = dict_of_browsers[config['browser']['type']][0]
user_data = dict_of_browsers[config['browser']['type']][1]
prefix_for_profiles = config['browser']['prefix_for_profiles']
count_of_profiles = int(config['browser']['count_of_profiles'])
link = config['browser']['link']

choice_kill = input("Удалять старые вкладки [y / n]: ")

if choice_kill == 'y':
    if dict_of_browsers[config['browser']['type']] == 1:
        os.system('taskkill /F /IM brave.exe /T > nul 2>&1')
    else:
        os.system('taskkill /F /IM chrome.exe /T > nul 2>&1')
    choice_kill = True
else:
    choice_kill = False


def open_new_browser(number):
    subprocess.Popen(f'"{browser}"' + ' --start-maximized' + f' --profile-directory="{prefix_for_profiles} {number}"' + f' --user-data-dir="{user_data}"' + (' --restore-last-session' if not choice_kill else '') + f' "{link}"')
    time.sleep(ANTI_LAG_DELAY)


for number in range(count_of_profiles):
    open_new_browser(number)
