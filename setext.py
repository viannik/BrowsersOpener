import os
import shutil

path=os.getenv('LOCALAPPDATA')+'\\Google\\Chrome\\User Data\\'

ALL_PROFILES = 3
prefix_for_profiles = 'test'
dirlist=[
        'Local Extension Settings',
        'Sync Extension Settings']


def set_ext(number):
    for dirname in dirlist:
        root_src_dir = f"{path}{prefix_for_profiles}0\{dirname}"
        root_dst_dir = f'{path}{prefix_for_profiles}{number+1}\{dirname}'

        print(root_src_dir, '\t', root_dst_dir)
        shutil.copytree(root_src_dir, root_dst_dir, dirs_exist_ok=True)


for number in range(ALL_PROFILES-1):
    set_ext(number)
