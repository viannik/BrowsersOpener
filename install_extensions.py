import winreg

extensions = [
    'nkbihfbeogaeaoehlefnkodbefgpgknn'
]

for i in range(len(extensions)):
    registry_key = None

    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Policies\\Google\\Chrome\\ExtensionInstallForcelist', 0, winreg.KEY_WRITE)
    except:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Policies', 0, winreg.KEY_WRITE)
        winreg.CreateKey(registry_key, 'Google')
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Policies\\Google', 0, winreg.KEY_WRITE)
        winreg.CreateKey(registry_key, 'Chrome')
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Policies\\Google\\Chrome', 0, winreg.KEY_WRITE)
        winreg.CreateKey(registry_key, 'ExtensionInstallForcelist')
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Policies\\Google\\Chrome\\ExtensionInstallForcelist', 0, winreg.KEY_WRITE)

    winreg.SetValueEx(registry_key, str(i + 100), 0, winreg.REG_SZ, f'{extensions[i]};https://clients2.google.com/service/update2/crx')
    winreg.CloseKey(registry_key)

print(f'Успешно установлено {len(extensions)} расширений!')
