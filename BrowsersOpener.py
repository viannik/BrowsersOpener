import configparser, subprocess, time, json, winreg, pyautogui
from shutil import rmtree

profiles_data = configparser.ConfigParser()
profiles_data.read('profiles_data.ini')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

import os, shutil
import tkinter.ttk as ttk

import configparser

profiles_data = configparser.ConfigParser()
profiles_data.read('profiles_data.ini')

import sys
import tkinter as tk

root = tk.Tk()
create_group_count = tk.StringVar()
create_group_name = tk.StringVar()
alarm_label_text = tk.StringVar()
type_of_browser = tk.StringVar()
groups_of_browser = tk.StringVar()
link_open = tk.StringVar()
type_of_browser.set('Chrome')


def get_browser_info():
    global browser_type
    global browser_exe_path
    global user_data
    global js_rename_path

    dict_of_browsers = {
        'chrome': [
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data',
            'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section.expanded > settings-people-page").shadowRoot.querySelector("#pages > settings-subpage > settings-manage-profile").shadowRoot.querySelector("#name").shadowRoot.querySelector("#input")'
        ],
        'brave': [
            'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe',
            os.getenv('LOCALAPPDATA') + '\\BraveSoftware\\Brave-Browser\\User Data',
            'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section.expanded > brave-settings-getting-started").shadowRoot.querySelector("settings-people-page").shadowRoot.querySelector("#pages > settings-subpage > settings-manage-profile").shadowRoot.querySelector("#name").shadowRoot.querySelector("#input")'
        ],
        'chromium': [
            os.getenv('LOCALAPPDATA') + '\\Chromium\\Application\\chrome.exe',
            os.getenv('LOCALAPPDATA') + '\\Chromium\\User Data',
            'document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section.expanded > settings-people-page").shadowRoot.querySelector("#pages > settings-subpage > settings-manage-profile").shadowRoot.querySelector("#name").shadowRoot.querySelector("#input")'
        ]
    }

    browser_type = type_of_browser.get().lower()
    browser_exe_path = dict_of_browsers[browser_type][0]
    user_data = dict_of_browsers[browser_type][1]
    js_rename_path = dict_of_browsers[browser_type][2]


browser_type = ''
browser_exe_path = ''
user_data = ''
js_rename_path = ''

get_browser_info()

link_open.set(profiles_data[browser_type]['last_link'])
extension_input = tk.StringVar()


def alarm(text):
    alarm_label_text.set(text)


def open_window_create_group():
    global _top3, _w3
    _top3 = tk.Toplevel(root)
    _w3 = Create_group(_top3)


def button_create_group():
    global browser_type
    if not create_group_count.get().isdigit():
        alarm('Incorrect input: count is only number!')
        return

    if create_group_name.get() == '':
        alarm('Incorrect input: name error!')
        return

    if create_group_name.get() in profiles_data[browser_type]['profiles']:
        alarm('Error: this name is already in use!')
        return

    get_browser_info()

    def rename_default_profile(name):
        global browser_type
        global browser_exe_path
        global user_data
        global js_rename_path

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.binary_location = browser_exe_path

        options.add_argument(f'--user-data-dir={user_data}')
        options.add_argument(f'--profile-directory=Default')

        browser = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
        type_ = 'chrome'
        if browser_type == 'brave':
            type_ = 'brave'
        browser.get(f"{type_}://settings/manageProfile")

        profileInput = browser.execute_script(f'return {js_rename_path}')
        profileInput.clear()
        profileInput.send_keys(name)
        profileInput.send_keys(Keys.ENTER)

        time.sleep(1)

        browser.close()
        browser.quit()

    def rename_profile(number):
        global browser_type
        global browser_exe_path
        global user_data
        global js_rename_path

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.binary_location = browser_exe_path

        options.add_argument(f'--user-data-dir={user_data}')
        options.add_argument(f'--profile-directory=BrowsersOpener_profile {number}')

        browser = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
        type_ = 'chrome'
        if browser_type == 'brave':
            type_ = 'brave'
        browser.get(f"{type_}://settings/manageProfile")

        profileInput = browser.execute_script(f'return {js_rename_path}')
        profileInput.click()
        profileInput.clear()
        profileInput.send_keys(
            f"{create_group_name.get()} {number - int(profiles_data[browser_type]['last_number']) + 1}")
        profileInput.send_keys(Keys.ENTER)

        time.sleep(1)

        browser.close()
        browser.quit()

    rename_default_profile('Default Profile')

    for number in range(int(profiles_data[browser_type]['last_number']),
                        int(create_group_count.get()) + int(
                            profiles_data[browser_type]['last_number'])):
        rename_profile(number)

    alarm(
        f'Group {int(profiles_data[browser_type]["last_group"])} ({create_group_name.get()} 0-{int(create_group_count.get())}) created!')

    old = profiles_data[browser_type]["profiles"]
    new = old + f"{create_group_name.get()};{int(profiles_data[browser_type]['last_number'])};{int(create_group_count.get()) + int(profiles_data[browser_type]['last_number']) - 1},"
    profiles_data.set(browser_type, 'profiles', new)

    profiles_data.set(browser_type, 'last_number', str(int(create_group_count.get()) + int(
        profiles_data[browser_type]['last_number'])))
    profiles_data.set(browser_type, 'last_group', str(int(profiles_data[browser_type]["last_group"]) + 1))

    with open('profiles_data.ini', 'w') as configfile:
        profiles_data.write(configfile)

    update_group_spinbox()


def new_type_of_browser():
    try:
        update_group_spinbox()
    except:
        pass
    try:
        update_extension_listbox()
    except:
        pass


spinboxt_groups = None


def update_group_spinbox():
    global spinboxt_groups
    spinboxt_groups.configure(state="normal")
    try:
        spinboxt_groups.delete(0, "end")
    except:
        pass
    get_browser_info()
    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    number = 0
    new_list = []
    for element in array:
        mini_array = element.split(';')
        new_list.append(f'Group {number} ({mini_array[0]} 1-{int(mini_array[2]) - int(mini_array[1]) + 1})')
        number += 1

    spinboxt_groups.configure(values=new_list)
    spinboxt_groups.configure(state="readonly")


listbot_groups = None


def update_extension_listbox():
    global listbot_groups
    try:
        listbot_groups.delete(0, "end")
    except:
        pass
    get_browser_info()
    array = profiles_data[browser_type]['extensions'].split(',')[:-1]

    for i in array:
        listbot_groups.insert(tk.END, i)


def delete_current_group():
    global _top5, _w5
    _top5 = tk.Toplevel(root)
    _w5 = Deleting_group(_top5)


def delete_current_group_confirm():
    get_browser_info()

    global browser_type
    global browser_exe_path
    global user_data
    global js_rename_path

    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    mini_array = array[int(groups_of_browser.get().split(' ')[1])].split(';')

    for number in range(int(mini_array[1]), int(mini_array[2]) + 1):
        rmtree(f'{user_data}\\BrowsersOpener_profile {number}')

    text = f'{groups_of_browser.get()} successfully deleted.'

    with open(f'{user_data}\\Local State', 'r') as file:
        data = json.load(file)

    removes_list = []

    for number in range(int(mini_array[1]), int(mini_array[2]) + 1):
        for i in data['profile']['info_cache']:
            if i == f'BrowsersOpener_profile {number}':
                removes_list.append(i)
    for i in removes_list:
        del data['profile']['info_cache'][i]

    data['profile']['last_used'] = 'Default'
    with open(f'{user_data}\\Local State', 'w') as file:
        json.dump(data, file)

    new_profiles = profiles_data[browser_type]['profiles'].replace(
        array[int(groups_of_browser.get().split(' ')[1])] + ',', '')
    profiles_data.set(browser_type, 'profiles', new_profiles)
    profiles_data.set(browser_type, 'last_group', str(int(profiles_data[browser_type]['last_group']) - 1))
    with open('profiles_data.ini', 'w') as configfile:
        profiles_data.write(configfile)
    update_group_spinbox()

    alarm(text)


def open_current_group():
    if groups_of_browser.get() == '':
        alarm('Error: you need to select a group!')
        return

    if link_open.get() == '':
        alarm('Error: you need to enter a link!')
        return

    get_browser_info()
    global browser_type
    global browser_exe_path
    global user_data
    global js_rename_path

    ANTI_LAG_DELAY = 0.5

    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    mini_array = array[int(groups_of_browser.get().split(' ')[1])].split(';')

    def open_new_browser(number):
        global browser_type
        global browser_exe_path
        global user_data
        global js_rename_path
        subprocess.Popen(
            f'"{browser_exe_path}"' + ' --start-maximized' + f' --user-data-dir="{user_data}"' + f' --profile-directory="BrowsersOpener_profile {number}"' + (
                " --restore-last-session" if profiles_data[browser_type][
                                                 "save_tabs"] == "1" else '') + f' "{link_open.get()}"')
        time.sleep(ANTI_LAG_DELAY)

    for number in range(int(mini_array[1]), int(mini_array[2]) + 1):
        open_new_browser(number)

    profiles_data.set(browser_type, 'last_link', link_open.get())
    profiles_data.set(browser_type, 'save_tabs', '0')

    with open('profiles_data.ini', 'w') as configfile:
        profiles_data.write(configfile)

    alarm(f'{groups_of_browser.get()} successfully opened.')


def open_window_open_from_to():
    get_browser_info()
    # global _top4, _w4
    # _top4 = tk.Toplevel(root)
    # _w4 = Open_from_to(_top4)
    global user_data
    with open(f'{user_data}\\Local State', 'r') as file:
        data = json.load(file)

    removes_list = []

    data['profile']['last_used'] = 'Default'
    print(data['profile']['last_used'])

    with open(f'{user_data}\\Local State', 'w') as file:
        json.dump(data, file)


def close_without_saving_tabs():
    get_browser_info()
    global browser_type

    if browser_type == 'brave':
        os.system('taskkill /F /IM brave.exe /T > nul 2>&1')
    else:
        os.system('taskkill /F /IM chrome.exe /T > nul 2>&1')

    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    mini_array = array[int(groups_of_browser.get().split(' ')[1])].split(';')

    for number in range(int(mini_array[1]), int(mini_array[2]) + 1):
        with open(f'{user_data}\\BrowsersOpener_profile {number}\\Preferences', 'r') as file:
            data = file.read()
            new_data = data.replace('"exit_type":"Crashed"', '"exit_type":"Normal"')

        with open(f'{user_data}\\BrowsersOpener_profile {number}\\Preferences', 'w') as file:
            file.write(new_data)

    alarm(f'{groups_of_browser.get()} successfully closed.')


def close_with_trying_to_save_tabs():
    get_browser_info()
    global browser_type

    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    mini_array = array[int(groups_of_browser.get().split(' ')[1])].split(';')

    for number in range(int(mini_array[1]), int(mini_array[2]) + 1):
        if browser_type == 'brave':
            os.system('taskkill /IM brave.exe > nul 2>&1')
        else:
            os.system('taskkill /IM chrome.exe > nul 2>&1')

    profiles_data.set(browser_type, 'save_tabs', '1')
    with open('profiles_data.ini', 'w') as configfile:
        profiles_data.write(configfile)

    alarm(f'{groups_of_browser.get()} successfully closed.')


def open_window_extensions():
    global _top5, _w5
    _top5 = tk.Toplevel(root)
    _w5 = Extensions(_top5)


def uninstall_extension():
    get_browser_info()
    global browser_type

    if listbot_groups.get(tk.ANCHOR) == '':
        alarm("Error: select an extension from the list!")
        return

    number = listbot_groups.get(tk.ANCHOR).split('. ')[0]

    dict_of_browsers = {
        'chrome': ['Google', 'Chrome'],
        'brave': ['BraveSoftware', 'Brave'],
        'chromium': ['Chromium']
    }

    profiles_data.set(browser_type, 'extensions',
                      profiles_data[browser_type]['extensions'].replace(f"{listbot_groups.get(tk.ANCHOR)},", ''))
    with open('profiles_data.ini', 'w') as configfile:
        profiles_data.write(configfile)

    browser_registry = ''
    for i in dict_of_browsers[browser_type]:
        browser_registry += i + '\\'

    str_for_ping_extensions = '{ '
    for i in profiles_data[browser_type]['extensions'].split(',')[:-1]:
        str_for_ping_extensions += f'"{i}":' + ' {"toolbar_pin": "force_pinned", "installation_mode": "normal_installed", "update_url": "https://clients2.google.com/service/update2/crx"},'
    str_for_ping_extensions += ' }'

    registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'SOFTWARE\\Policies\\{browser_registry}', 0,
                                  winreg.KEY_WRITE)
    winreg.SetValueEx(registry_key, 'ExtensionSettings', 0, winreg.REG_SZ, str_for_ping_extensions)
    winreg.CloseKey(registry_key)

    update_extension_listbox()

    alarm(f'Extension successfully uninstalled.')


def install_extension():
    if extension_input.get() == '':
        alarm('Error: you need to enter a extension ID!')
        return

    get_browser_info()
    global browser_type

    if extension_input.get() in profiles_data[browser_type]['extensions']:
        alarm('Error: this extension is already installed and pinned!')
        return

    dict_of_browsers = {
        'chrome': ['Google', 'Chrome'],
        'brave': ['BraveSoftware', 'Brave'],
        'chromium': ['Chromium']
    }

    browser_registry = ''
    for i in dict_of_browsers[browser_type]:
        browser_registry += i + '\\'

    profiles_data.set(browser_type, 'extensions',
                      f"{profiles_data[browser_type]['extensions']}{extension_input.get()},")

    with open('profiles_data.ini', 'w') as configfile:
        profiles_data.write(configfile)

    str_for_ping_extensions = '{ '
    for i in profiles_data[browser_type]['extensions'].split(',')[:-1]:
        str_for_ping_extensions += f'"{i}":' + ' {"toolbar_pin": "force_pinned", "installation_mode": "normal_installed", "update_url": "https://clients2.google.com/service/update2/crx"},'
    str_for_ping_extensions += ' }'

    registry_key = None

    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'SOFTWARE\\Policies\\{browser_registry}', 0,
                                      winreg.KEY_WRITE)
    except:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'SOFTWARE\\Policies', 0, winreg.KEY_WRITE)
        winreg.CreateKey(registry_key, f'{browser_registry}')
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'SOFTWARE\\Policies\\{browser_registry}', 0,
                                      winreg.KEY_WRITE)

    registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f'SOFTWARE\\Policies\\{browser_registry}', 0,
                                  winreg.KEY_WRITE)
    winreg.SetValueEx(registry_key, 'ExtensionSettings', 0, winreg.REG_SZ, str_for_ping_extensions)
    winreg.CloseKey(registry_key)

    update_extension_listbox()

    alarm(f'Extension successfully installed and pinned.')


def open_window_special_options():
    global _top7, _w7
    _top7 = tk.Toplevel(root)
    _w7 = Special_options(_top7)


def login_metamasks():
    if groups_of_browser.get() == '':
        alarm('Error: you need to select a group!')
        return

    get_browser_info()
    global browser_type
    global browser_exe_path
    global user_data
    global js_rename_path

    with open(f'metamasks.txt', 'r') as file:
        data = file.read()

    phrases = data.split('\n')

    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    mini_array = array[int(groups_of_browser.get().split(' ')[1])].split(';')

    from_ = int(mini_array[1])
    to_ = int(mini_array[2]) + 1

    if to_ - from_ != len(phrases):
        alarm("Error: group profiles = metamasks.txt phrases!")
        return

    len_of_phrase = 12

    number = 0
    for j in range(from_, to_):
        while True:
            os.system('taskkill /F /IM chromedriver.exe /T > nul 2>&1')

            try:
                phrase = phrases[number].split(',')

                options = webdriver.ChromeOptions()
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.binary_location = browser_exe_path

                options.add_argument(f'--user-data-dir={user_data}')
                options.add_argument(f'--profile-directory=BrowsersOpener_profile {j}')

                browser = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
                browser.get(
                    f'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/create-password/import-with-seed-phrase')

                for i in range(len_of_phrase):
                    while True:
                        try:
                            phrase_input = browser.execute_script(
                                f'return document.querySelector("#import-srp__srp-word-{i}")')
                            phrase_input.click()
                            phrase_input.send_keys(phrase[i])
                            phrase_input.send_keys(Keys.ENTER)
                            break
                        except:
                            time.sleep(0.5)
                            continue

                password_input = browser.execute_script(f'return document.querySelector("#password")')
                password_input.click()
                password_input.send_keys(phrase[-1])
                password_input.send_keys(Keys.ENTER)

                confirm_password_input = browser.execute_script(f'return document.querySelector("#confirm-password")')
                confirm_password_input.click()
                confirm_password_input.send_keys(phrase[-1])
                confirm_password_input.send_keys(Keys.ENTER)

                check_box = browser.execute_script(
                    f'return document.querySelector("#create-new-vault__terms-checkbox")')
                check_box.click()

                time.sleep(0.5)

                confirm_button = browser.execute_script(
                    f'return document.querySelector("#app-content > div > div.main-container-wrapper > div > div > div.first-time-flow__import > form > button")')
                confirm_button.click()

                number += 1
                while True:
                    try:
                        last_button = browser.execute_script(
                            'return document.querySelector("#app-content > div > div.main-container-wrapper > div > div > button")')
                        last_button.click()
                        break
                    except:
                        time.sleep(0.5)
                        continue

                time.sleep(3)
                browser.quit()
                break
            except:
                time.sleep(0.5)
                continue

    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    mini_array = array[int(groups_of_browser.get().split(' ')[1])].split(';')

    for number in range(int(mini_array[1]), int(mini_array[2]) + 1):
        with open(f'{user_data}\\BrowsersOpener_profile {number}\\Preferences', 'r') as file:
            data = file.read()
            new_data = data.replace('"exit_type":"Crashed"', '"exit_type":"Normal"')

        with open(f'{user_data}\\BrowsersOpener_profile {number}\\Preferences', 'w') as file:
            file.write(new_data)

    alarm(f"Group successfully filled metamasks.txt phrases!")


def login_proxies():
    if groups_of_browser.get() == '':
        alarm('Error: you need to select a group!')
        return

    get_browser_info()
    global browser_type
    global browser_exe_path
    global user_data
    global js_rename_path

    with open(f'proxies.txt', 'r') as file:
        data = file.read()

    proxies = data.split('\n')

    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    mini_array = array[int(groups_of_browser.get().split(' ')[1])].split(';')

    from_ = int(mini_array[1])
    to_ = int(mini_array[2]) + 1

    if to_ - from_ != len(proxies):
        alarm("Error: group profiles = proxies.txt proxies!")
        return

    number = 0
    for j in range(from_, to_):
        while True:
            os.system('taskkill /F /IM chromedriver.exe /T > nul 2>&1')

            try:
                proxy = proxies[number].split(':')

                options = webdriver.ChromeOptions()
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.binary_location = browser_exe_path

                options.add_argument(f'--user-data-dir={user_data}')
                options.add_argument(f'--profile-directory=BrowsersOpener_profile {j}')

                browser = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
                browser.get('chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy')

                while True:
                    try:
                        server_input = browser.execute_script(
                            f'return document.querySelector("body > div.container-fluid > main > div:nth-child(3) > div > section.settings-group.settings-group-fixed-servers > div > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(3) > input")')
                        server_input.click()
                        server_input.clear()
                        server_input.send_keys(proxy[0])
                        server_input.send_keys(Keys.ENTER)
                        break
                    except:
                        time.sleep(0.5)
                        continue

                port_input = browser.execute_script(
                    f'return document.querySelector("body > div.container-fluid > main > div:nth-child(3) > div > section.settings-group.settings-group-fixed-servers > div > table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4) > input")')
                port_input.click()
                port_input.clear()
                port_input.send_keys(proxy[1])
                port_input.send_keys(Keys.ENTER)

                button_lock = browser.execute_script(
                    'return document.querySelector("body > div.container-fluid > main > div:nth-child(3) > div > section.settings-group.settings-group-fixed-servers > div > table > tbody:nth-child(2) > tr:nth-child(1) > td.proxy-actions > button > span")').click()

                while True:
                    try:
                        username_input = browser.execute_script(
                            f'return document.querySelector("body > div.modal.fade.ng-isolate-scope.in > div > div > form > div.modal-body > div:nth-child(2) > div > div > input")')
                        username_input.click()
                        username_input.send_keys(proxy[2])
                        break
                    except:
                        time.sleep(0.5)
                        continue

                password_input = browser.execute_script(
                    f'return document.querySelector("body > div.modal.fade.ng-isolate-scope.in > div > div > form > div.modal-body > div:nth-child(3) > div > input")')
                password_input.click()
                password_input.send_keys(proxy[3])

                button_save_user_pass = browser.execute_script(
                    'return document.querySelector("body > div.modal.fade.ng-isolate-scope.in > div > div > form > div.modal-footer > button.btn.btn-primary.ng-binding")').click()
                button_apply_changes = browser.execute_script(
                    'return document.querySelector("body > div.container-fluid > header > nav > li:nth-child(12) > a")').click()

                browser.get('chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/ui')

                while True:
                    try:
                        button_switcher = browser.execute_script(
                            f'return document.querySelector("body > div.container-fluid > main > section:nth-child(4) > div.form-group > div > div > button > span:nth-child(3)")').click()
                        break
                    except:
                        time.sleep(0.5)
                        continue

                button_proxy = browser.execute_script(
                    'return document.querySelector("body > div.container-fluid > main > section:nth-child(4) > div.form-group > div > div > ul > li:nth-child(3) > a")').click()
                button_apply_changes = browser.execute_script(
                    'return document.querySelector("body > div.container-fluid > header > nav > li:nth-child(12) > a")').click()

                number += 1
                time.sleep(2)
                browser.quit()
                break
            except:
                time.sleep(0.5)
                continue

    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    mini_array = array[int(groups_of_browser.get().split(' ')[1])].split(';')

    for number in range(int(mini_array[1]), int(mini_array[2]) + 1):
        with open(f'{user_data}\\BrowsersOpener_profile {number}\\Preferences', 'r') as file:
            data = file.read()
            new_data = data.replace('"exit_type":"Crashed"', '"exit_type":"Normal"')

        with open(f'{user_data}\\BrowsersOpener_profile {number}\\Preferences', 'w') as file:
            file.write(new_data)

    alarm(f"Group successfully filled proxies.txt proxies!")


def auto_log_metamask():
    if groups_of_browser.get() == '':
        alarm('Error: you need to select a group!')
        return

    get_browser_info()
    global browser_type
    global browser_exe_path
    global user_data
    global js_rename_path

    with open(f'metamasks.txt', 'r') as file:
        data = file.read()

    phrases = data.split('\n')

    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    mini_array = array[int(groups_of_browser.get().split(' ')[1])].split(';')

    from_ = int(mini_array[1])
    to_ = int(mini_array[2]) + 1

    if to_ - from_ != len(phrases):
        alarm("Error: group profiles = metamasks.txt phrases!")
        return

    len_of_phrase = 12

    number = 0
    for j in range(from_, to_):
        password = phrases[number].split(',')[-1]

        subprocess.Popen(
            f'"{browser_exe_path}"' + ' --start-maximized' + f' --user-data-dir="{user_data}"' + f' --profile-directory="BrowsersOpener_profile {j}"' + ' "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#unlock"')

        time.sleep(3)

        loaded = pyautogui.locateCenterOnScreen('area.png')

        while loaded is None:
            loaded = pyautogui.locateCenterOnScreen('area.png')

        pyautogui.write(password)
        pyautogui.press('enter')

        time.sleep(2)

        pyautogui.hotkey('ctrl', 'w')

    alarm(f"Group successfully logged Metamasks!")


def copy_extension_settings():
    if groups_of_browser.get() == '':
        alarm('Error: you need to select a group!')
        return

    get_browser_info()
    global browser_type
    global browser_exe_path
    global user_data
    global js_rename_path

    array = profiles_data[browser_type]['profiles'].split(',')[:-1]
    mini_array = array[int(groups_of_browser.get().split(' ')[1])].split(';')

    from_ = int(mini_array[1])
    to_ = int(mini_array[2]) + 1

    dirlist = [
        'Local Extension Settings',
        'Sync Extension Settings'
    ]

    for j in range(from_ + 1, to_):
        for dirname in dirlist:
            root_src_dir = f'{user_data}\\BrowsersOpener_profile {from_}\\{dirname}'
            root_dst_dir = f'{user_data}\\BrowsersOpener_profile {j}\\{dirname}'

            shutil.copytree(root_src_dir, root_dst_dir, dirs_exist_ok=True)

    alarm(f"Extensions settings successfully copied!")


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = 'gray40'  # X11 color: #666666
        _ana1color = '#c3c3c3'  # Closest X11 color: 'gray76'
        _ana2color = 'beige'  # X11 color: #f5f5dc
        _tabfg1 = 'black'
        _tabfg2 = 'black'
        _tabbg1 = 'grey75'
        _tabbg2 = 'grey89'
        _bgmode = 'light'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("300x470+476+140")
        top.minsize(120, 1)
        top.maxsize(1540, 825)
        top.resizable(0, 0)
        top.title("Browsers Opener")
        top.configure(background="#d9d9d9")
        top.configure(cursor="arrow")

        self.top = top

        self.Spinbox1 = tk.Spinbox(self.top, from_=1.0, to=100.0)
        self.Spinbox1.place(x=10, y=10, height=20, width=88)
        self.Spinbox1.configure(activebackground="#f9f9f9")
        self.Spinbox1.configure(background="white")
        self.Spinbox1.configure(buttonbackground="#d9d9d9")
        self.Spinbox1.configure(disabledforeground="#a3a3a3")
        self.Spinbox1.configure(font="TkDefaultFont")
        self.Spinbox1.configure(foreground="black")
        self.Spinbox1.configure(state="readonly")
        self.Spinbox1.configure(highlightbackground="black")
        self.Spinbox1.configure(highlightcolor="black")
        self.Spinbox1.configure(insertbackground="black")
        self.Spinbox1.configure(selectbackground="#c4c4c4")
        self.Spinbox1.configure(selectforeground="black")
        self.value_list = ['Chrome', 'Brave', 'Chromium', ]
        self.Spinbox1.configure(values=self.value_list)
        self.Spinbox1.configure(values=self.value_list)
        self.Spinbox1.configure(textvariable=type_of_browser)
        self.Spinbox1.configure(command=new_type_of_browser)

        self.Spinbox2 = tk.Spinbox(self.top, from_=1.0, to=100.0)
        self.Spinbox2.place(x=110, y=10, height=20, width=178)
        self.Spinbox2.configure(activebackground="#f9f9f9")
        self.Spinbox2.configure(background="white")
        self.Spinbox2.configure(buttonbackground="#d9d9d9")
        self.Spinbox2.configure(disabledforeground="#a3a3a3")
        self.Spinbox2.configure(font="TkDefaultFont")
        self.Spinbox2.configure(foreground="black")
        self.Spinbox2.configure(state="readonly")
        self.Spinbox2.configure(highlightbackground="black")
        self.Spinbox2.configure(highlightcolor="black")
        self.Spinbox2.configure(insertbackground="black")
        self.Spinbox2.configure(selectbackground="#c4c4c4")
        self.Spinbox2.configure(selectforeground="black")
        self.Spinbox2.configure(textvariable=groups_of_browser)

        global spinboxt_groups
        spinboxt_groups = self.Spinbox2

        self.Button1 = tk.Button(self.top)
        self.Button1.place(x=10, y=52, height=34, width=277)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=open_window_create_group)
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Create Group''')

        self.Button2 = tk.Button(self.top)
        self.Button2.place(x=10, y=94, height=34, width=277)
        self.Button2.configure(activebackground="beige")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(command=delete_current_group)
        self.Button2.configure(compound='left')
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Delete Group''')

        self.TSeparator1 = ttk.Separator(self.top)
        self.TSeparator1.place(x=0, y=136, width=300)

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.TSeparator1_1 = ttk.Separator(self.top)
        self.TSeparator1_1.place(x=0, y=42, width=300)

        self.Button3 = tk.Button(self.top)
        self.Button3.place(x=10, y=146, height=34, width=277)
        self.Button3.configure(activebackground="beige")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(command=open_current_group)
        self.Button3.configure(compound='left')
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''Open the link in the selected Group''')

        self.Button4 = tk.Button(self.top)
        # self.Button4.place(x=10, y=188, height=34, width=277)
        self.Button4.configure(activebackground="beige")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#d9d9d9")
        self.Button4.configure(command=open_window_open_from_to)
        self.Button4.configure(compound='left')
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''Open from-to''')

        self.TSeparator2 = ttk.Separator(self.top)
        self.TSeparator2.place(x=0, y=230, width=300)

        self.Button5 = tk.Button(self.top)
        self.Button5.place(x=10, y=240, height=34, width=277)
        self.Button5.configure(activebackground="beige")
        self.Button5.configure(activeforeground="#000000")
        self.Button5.configure(background="#d9d9d9")
        self.Button5.configure(command=open_window_extensions)
        self.Button5.configure(compound='left')
        self.Button5.configure(disabledforeground="#a3a3a3")
        self.Button5.configure(foreground="#000000")
        self.Button5.configure(highlightbackground="#d9d9d9")
        self.Button5.configure(highlightcolor="black")
        self.Button5.configure(pady="0")
        self.Button5.configure(text='''Extensions''')

        self.TSeparator3 = ttk.Separator(self.top)
        self.TSeparator3.place(x=0, y=282, width=300)

        # close without saving tabs
        self.Button6 = tk.Button(self.top)
        self.Button6.place(x=10, y=292, height=34, width=277)
        self.Button6.configure(activebackground="beige")
        self.Button6.configure(activeforeground="#000000")
        self.Button6.configure(background="#d9d9d9")
        self.Button6.configure(command=close_without_saving_tabs)
        self.Button6.configure(compound='left')
        self.Button6.configure(disabledforeground="#a3a3a3")
        self.Button6.configure(foreground="#000000")
        self.Button6.configure(highlightbackground="#d9d9d9")
        self.Button6.configure(highlightcolor="black")
        self.Button6.configure(pady="0")
        self.Button6.configure(text='''Close browser without saving tabs''')

        self.Button7 = tk.Button(self.top)
        self.Button7.place(x=10, y=334, height=34, width=277)
        self.Button7.configure(activebackground="beige")
        self.Button7.configure(activeforeground="#000000")
        self.Button7.configure(background="#d9d9d9")
        self.Button7.configure(command=close_with_trying_to_save_tabs)
        self.Button7.configure(compound='left')
        self.Button7.configure(disabledforeground="#a3a3a3")
        self.Button7.configure(foreground="#000000")
        self.Button7.configure(highlightbackground="#d9d9d9")
        self.Button7.configure(highlightcolor="black")
        self.Button7.configure(pady="0")
        self.Button7.configure(text='''Close browser with trying to save tabs''')

        self.TSeparator4 = ttk.Separator(self.top)
        self.TSeparator4.place(x=0, y=376, width=300)

        self.Button8 = tk.Button(self.top)
        self.Button8.place(x=10, y=386, height=34, width=277)
        self.Button8.configure(activebackground="beige")
        self.Button8.configure(activeforeground="#000000")
        self.Button8.configure(background="#d9d9d9")
        self.Button8.configure(command=open_window_special_options)
        self.Button8.configure(compound='left')
        self.Button8.configure(disabledforeground="#a3a3a3")
        self.Button8.configure(foreground="#000000")
        self.Button8.configure(highlightbackground="#d9d9d9")
        self.Button8.configure(highlightcolor="black")
        self.Button8.configure(pady="0")
        self.Button8.configure(text='''Special options''')

        self.TSeparator5 = ttk.Separator(self.top)
        self.TSeparator5.place(x=0, y=428, width=300)

        self.Label1 = tk.Label(self.top)
        self.Label1.place(x=10, y=439, height=22, width=274)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(compound='center')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''''')
        self.Label1.configure(textvariable=alarm_label_text)

        self.Entry1 = tk.Entry(self.top)
        self.Entry1.place(relx=0.033, rely=0.395, height=20, relwidth=0.913)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(textvariable=link_open)


class Create_group:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = 'gray40'  # X11 color: #666666
        _ana1color = '#c3c3c3'  # Closest X11 color: 'gray76'
        _ana2color = 'beige'  # X11 color: #f5f5dc
        _tabfg1 = 'black'
        _tabfg2 = 'black'
        _tabbg1 = 'grey75'
        _tabbg2 = 'grey89'
        _bgmode = 'light'

        top.geometry("200x100+775+141")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(0, 0)
        top.title("Create Group")
        top.configure(background="#d9d9d9")

        self.top = top

        self.Label1 = tk.Label(self.top)
        self.Label1.place(x=10, y=10, height=21, width=104)
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Count of profiles:''')

        self.Label1 = tk.Label(self.top)
        self.Label1.place(x=10, y=30, height=21, width=104)
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Name of profiles:''')

        self.Entry1 = tk.Entry(self.top)
        self.Entry1.place(x=110, y=5, height=20, width=74)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(textvariable=create_group_count)

        self.Entry1 = tk.Entry(self.top)
        self.Entry1.place(x=110, y=30, height=20, width=74)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(textvariable=create_group_name)

        self.Button1 = tk.Button(self.top)
        self.Button1.place(x=10, y=60, height=24, width=177)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=button_create_group)
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Create''')


class Open_from_to:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = 'gray40'  # X11 color: #666666
        _ana1color = '#c3c3c3'  # Closest X11 color: 'gray76'
        _ana2color = 'beige'  # X11 color: #f5f5dc
        _tabfg1 = 'black'
        _tabfg2 = 'black'
        _tabbg1 = 'grey75'
        _tabbg2 = 'grey89'
        _bgmode = 'light'

        top.geometry("200x200+774+271")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(0, 0)
        top.title("Open from-to")
        top.configure(background="#d9d9d9")

        self.top = top

        self.Listbox1 = tk.Listbox(self.top)
        self.Listbox1.place(x=10, y=10, height=86, width=175)
        self.Listbox1.configure(background="white")
        self.Listbox1.configure(disabledforeground="#a3a3a3")
        self.Listbox1.configure(font="TkFixedFont")
        self.Listbox1.configure(foreground="#000000")

        self.Entry1 = tk.Entry(self.top)
        self.Entry1.place(x=10, y=110, height=30, width=84)
        self.Entry1.configure(background="white")
        self.Entry1.configure(cursor="fleur")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        self.Entry1 = tk.Entry(self.top)
        self.Entry1.place(x=100, y=110, height=30, width=84)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        self.Button1 = tk.Button(self.top)
        self.Button1.place(x=10, y=150, height=34, width=177)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=lambda: print('open_open'))
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Open''')


class Extensions:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = 'gray40'  # X11 color: #666666
        _ana1color = '#c3c3c3'  # Closest X11 color: 'gray76'
        _ana2color = 'beige'  # X11 color: #f5f5dc
        _tabfg1 = 'black'
        _tabfg2 = 'black'
        _tabbg1 = 'grey75'
        _tabbg2 = 'grey89'
        _bgmode = 'light'

        top.geometry("368x200+775+502")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(0, 0)
        top.title("Extensions")
        top.configure(background="#d9d9d9")

        self.top = top

        self.Listbox1 = tk.Listbox(self.top)
        self.Listbox1.place(x=10, y=10, height=66, width=350)
        self.Listbox1.configure(background="white")
        self.Listbox1.configure(disabledforeground="#a3a3a3")
        self.Listbox1.configure(font="TkFixedFont")
        self.Listbox1.configure(foreground="#000000")

        global listbot_groups
        listbot_groups = self.Listbox1
        update_extension_listbox()

        self.Button1 = tk.Button(self.top)
        self.Button1.place(x=10, y=90, height=34, width=350)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=uninstall_extension)
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Uninstall''')

        self.Entry1 = tk.Entry(self.top)
        self.Entry1.place(x=10, y=130, height=20, width=350)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(textvariable=extension_input)

        self.Button1 = tk.Button(self.top)
        self.Button1.place(x=10, y=160, height=34, width=350)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=install_extension)
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Install''')


class Special_options:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = 'gray40'  # X11 color: #666666
        _ana1color = '#c3c3c3'  # Closest X11 color: 'gray76'
        _ana2color = 'beige'  # X11 color: #f5f5dc
        _tabfg1 = 'black'
        _tabfg2 = 'black'
        _tabbg1 = 'grey75'
        _tabbg2 = 'grey89'
        _bgmode = 'light'

        top.geometry("470x170+976+141")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(0, 0)
        top.title("Special Options")
        top.configure(background="#d9d9d9")

        self.top = top

        self.Button1 = tk.Button(self.top)
        self.Button1.place(x=10, y=10, height=34, width=450)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(command=login_metamasks)
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Metamask''')

        self.Button1 = tk.Button(self.top)
        self.Button1.place(x=10, y=50, height=34, width=450)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(command=auto_log_metamask)
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Login Metamask''')

        self.Button1 = tk.Button(self.top)
        self.Button1.place(x=10, y=90, height=34, width=450)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(command=login_proxies)
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Proxy''')

        self.Button1 = tk.Button(self.top)
        self.Button1.place(x=10, y=130, height=34, width=450)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(command=copy_extension_settings)
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Copy extension settings from GroupName 0 to all Group''')


class Deleting_group:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = 'gray40'  # X11 color: #666666
        _ana1color = '#c3c3c3'  # Closest X11 color: 'gray76'
        _ana2color = 'beige'  # X11 color: #f5f5dc
        _tabfg1 = 'black'
        _tabfg2 = 'black'
        _tabbg1 = 'grey75'
        _tabbg2 = 'grey89'
        _bgmode = 'light'

        top.geometry("202x60+976+272")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(0, 0)
        top.title("Deleting Group")
        top.configure(background="#d9d9d9")

        self.top = top

        self.Button1 = tk.Button(self.top)
        self.Button1.place(relx=0.05, rely=0.167, height=34, width=177)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(compound='left')
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Confrim''')
        self.Button1.configure(command=delete_current_group_confirm)


def main():
    '''Main entry point for the application.'''
    global root
    global create_group_count
    global create_group_name
    global alarm_label_text
    global type_of_browser
    global groups_of_browser
    global link_open
    global extension_input

    root.protocol('WM_DELETE_WINDOW', root.destroy)
    global _top1, _w1
    _top1 = root
    _w1 = Toplevel1(_top1)
    update_group_spinbox()
    root.mainloop()


main()
