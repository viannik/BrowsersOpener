import os
import shutil

dict_of_browsers = {
    '0': os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data',
    '1': os.getenv('LOCALAPPDATA') + '\\BraveSoftware\\Brave-Browser\\User Data',
    '2': os.getenv('LOCALAPPDATA') + '\\Chromium\\User Data'
}

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

path = dict_of_browsers[config['browser']['type']]
count_of_profiles = int(config['browser']['count_of_profiles'])
prefix_for_profiles = config['browser']['prefix_for_profiles']

dirlist = [
    'Local Extension Settings',
    'Sync Extension Settings'
]


def copy_extensions(number):
    for dirname in dirlist:
        root_src_dir = f'{path}\\{prefix_for_profiles} 0\\{dirname}'
        root_dst_dir = f'{path}\\{prefix_for_profiles} {number + 1}\\{dirname}'

        print(f'---\n|{root_src_dir}|\n\tsetted into\n|{root_dst_dir}|\n---')
        shutil.copytree(root_src_dir, root_dst_dir, dirs_exist_ok=True)


for number in range(count_of_profiles - 1):
    copy_extensions(number)
