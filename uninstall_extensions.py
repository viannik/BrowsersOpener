import winreg

dict_of_browsers = {
    '0': ['Google', 'Chrome'],
    '1': ['BraveSoftware', 'Brave'],
    '2': ['Chromium']
}

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

extensions = config['extension']['extensions'].split(',')
browser_registry = ''
for i in dict_of_browsers[config['browser']['type']]:
    browser_registry += i + '\\'

for i in range(len(extensions)):
    registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'SOFTWARE\\Policies\\{browser_registry}ExtensionInstallForcelist', 0, winreg.KEY_ALL_ACCESS)
    winreg.DeleteValue(registry_key, str(i + 100))
    winreg.CloseKey(registry_key)

print(f'Успешно удалено {len(extensions)} расширений!')
