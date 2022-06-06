import os, time, subprocess

ALL_PROFILES = 3
ANTI_LAG_DELAY = 0.3

prefix_for_profiles = 'Viannik'
chrome_exe_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'


if input("Удалять старые вкладки [y / n]: "):
    os.system('taskkill /F /IM chrome.exe /T > nul 2>&1')


def open_new_browser(number):
    subprocess.Popen(f'"{chrome_exe_path}"' + ' --start-maximized' + f' --profile-directory={prefix_for_profiles}{number}' +' --restore-last-session' + ' http://google.com', shell = True)
    time.sleep(ANTI_LAG_DELAY)


for number in range(ALL_PROFILES):
    open_new_browser(number)
