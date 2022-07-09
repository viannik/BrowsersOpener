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
    registry_key = None

    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'SOFTWARE\\Policies\\{browser_registry}ExtensionInstallForcelist', 0, winreg.KEY_WRITE)
    except:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'SOFTWARE\\Policies', 0, winreg.KEY_WRITE)
        winreg.CreateKey(registry_key, f'{browser_registry}ExtensionInstallForcelist')
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'SOFTWARE\\Policies\\{browser_registry}ExtensionInstallForcelist', 0, winreg.KEY_WRITE)

    winreg.SetValueEx(registry_key, str(i + 100), 0, winreg.REG_SZ, f'{extensions[i]};https://clients2.google.com/service/update2/crx')
    winreg.CloseKey(registry_key)

print(f'Успешно установлено {len(extensions)} расширений!')
