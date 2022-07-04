import os, time, subprocess

link = 'https://droppp.queue-it.net/?c=droppp&e=dpkel1&ver=v3-php-3.7.0&cver=104&man=Kellogg%27s%20x%20Funko%20Series%201&t=https%3A%2F%2Fdroppp.io%2Freserve-drop%3Fdrop_id%3D41%26queue%3D1'

ALL_PROFILES = 3
ANTI_LAG_DELAY = 0.3

prefix_for_profiles = 'test'
chrome_exe_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

choice_kill = input("Удалять старые вкладки [y / n]: ")

if choice_kill == 'y':
	os.system('taskkill /F /IM chrome.exe /T > nul 2>&1')
	choice_kill = True
else:
	choice_kill = False

choice_extension = input("Установить расширение с папки [y / n]: ")

if choice_extension == 'y':
	choice_extension = True
else:
	choice_extension = False


def open_new_browser(number):
	extensions = ''

	if choice_extension:
		extensions = ' --load-extension='

		for extension in os.listdir("Extensions"):
			extensions += f'{os.getcwd()}\\Extensions\\{extension},'

		extensions = extensions[:-1]

	subprocess.Popen(
		f'"{chrome_exe_path}"' + ' --start-maximized' + f' --profile-directory={prefix_for_profiles}{number}' + extensions + (
			(' --restore-last-session') if choice_kill else ('')) + f' "{link}"', shell=True)

	time.sleep(ANTI_LAG_DELAY)


for number in range(ALL_PROFILES):
	open_new_browser(number)
