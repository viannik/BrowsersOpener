import os, time, subprocess

link = 'https://djinni.co/my/dashboard/'

ALL_PROFILES = 4
ANTI_LAG_DELAY = 0.5

prefix_for_profiles = 'test'
chrome_exe_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
chrome_user_data_path = os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data'

choice_kill = input("Удалять старые вкладки [y / n]: ")

if choice_kill == 'y':
    os.system('taskkill /F /IM chrome.exe /T > nul 2>&1')
    choice_kill = True
else:
    choice_kill = False


def open_new_browser(number):
    subprocess.Popen(f'"{chrome_exe_path}"' + ' --start-maximized' + f' --profile-directory="{prefix_for_profiles} {number}"' + f' --user-data-dir="{chrome_user_data_path}"' + (' --restore-last-session' if not choice_kill else '') + f' "{link}"')
    time.sleep(ANTI_LAG_DELAY)


for number in range(ALL_PROFILES):
    open_new_browser(number)
