import sys
import os
import platform
import shutil

err_msg = 'This system is not Windows 10. Exit.'
if sys.platform != 'win32':
    print(err_msg)
    exit()
if platform.release() != '10':
    print(err_msg)
    exit()

# APPDATA = os.getenv('APPDATA') # ApppData/Roaming
src_path = os.path.expanduser('~/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/')
dst_path = os.path.expanduser('~/Pictures/win10_lockscreen/')
if not os.path.isdir(dst_path):
    print('Destination folder does not exist. Create new one.')
    os.mkdir(dst_path)

list_files = os.listdir(src_path)
cnt = 0
for fname in list_files:
    src_file = src_path + fname
    fsize = os.path.getsize(src_file) / 1024  # KB
    if fsize < 400:  # temporary threshold
        continue
    dst_file = dst_path + fname + '.jpg'
    if os.path.isfile(dst_file):
        continue
    shutil.copyfile(src_file, dst_file)
    cnt += 1
print('Copied', cnt, 'items')
