import os

import configparser
config = configparser.ConfigParser()
config.read('config.ini')


for number in range(int(config['browser']['count_of_profiles'])):
    os.system('taskkill /IM chrome.exe > nul 2>&1')
    os.system('taskkill /IM brave.exe > nul 2>&1')