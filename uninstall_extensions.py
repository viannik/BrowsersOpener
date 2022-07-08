import winreg

extensions = [
    'nkbihfbeogaeaoehlefnkodbefgpgknn'
]

for i in range(len(extensions)):
    registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Policies\\Google\\Chrome\\ExtensionInstallForceList', 0, winreg.KEY_ALL_ACCESS)
    winreg.DeleteValue(registry_key, str(i + 100))
    winreg.CloseKey(registry_key)

print(f'Успешно удалено {len(extensions)} расширений!')
