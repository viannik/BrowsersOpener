import os

os.system('taskkill /F /IM brave.exe /T > nul 2>&1')
os.system('taskkill /F /IM chrome.exe /T > nul 2>&1')
os.system('taskkill /F /IM chromedriver.exe /T > nul 2>&1')
