import sys
import os
import platform
import numpy as np
import scipy.misc as misc
from PIL import Image
import shutil
import func


def check_already_copied(fname, copied_files):
    for c in copied_files:
        if fname in c:
            return True
    return False


def main():
    func.check_os()

    # APPDATA = os.getenv('APPDATA') # ApppData/Roaming
    src_path = os.path.expanduser('~/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/'
                                  'LocalState/Assets/')
    dst_path = os.path.expanduser('~/Pictures/win10_lockscreen/images/')
    if not os.path.isdir(dst_path):
        print('Destination folder does not exist. Create new one.')
        os.mkdir(dst_path)
    copied_files = [f for f in os.listdir(dst_path) if f.endswith('.jpg')]

    list_files = os.listdir(src_path)
    cnt = 0
    list_land = []
    list_port = []
    for fname in list_files:
        src_file = src_path + fname
        try:
            im = Image.open(src_file)
        except OSError:
            continue
        (x, y) = im.size
        im.close()
        if not check_already_copied(fname, copied_files):
            if x == 1920 and y == 1080:
                list_land += [fname]
            if x == 1080 and y == 1920:
                list_port += [fname]
    print('Following new items will be copied:')
    print('Landscape:', list_land)
    print('Portrait: ', list_port)

    err_all = []
    for land in list_land:
        im_land = np.array(Image.open(src_path + land))
        im_land = im_land[:, (960-304):(960+304), :]
        err = []
        for port in list_port:
            im_port = np.array(Image.open(src_path + port))
            im_port = misc.imresize(im_port, (1080, 608))
            err += [np.sum((im_land - im_port) ** 2) / (608 * 1080)]
        err_all += [np.array(err)]

    while True:
        n = len(list_land)
        m = len(list_port)
        if not n:
            break

        (arg_land, arg_port) = np.unravel_index(np.argmin(err_all), (n, m))
        shutil.copyfile(src_path + list_land[arg_land],
                        dst_path + list_land[arg_land] + '-land-' + list_port[arg_port] + '.jpg')
        shutil.copyfile(src_path + list_port[arg_port],
                        dst_path + list_land[arg_land] + '-port-' + list_port[arg_port] + '.jpg')
        cnt += 1

        del list_land[arg_land], list_port[arg_port]
        err_all = np.delete(err_all, arg_land, 0)
        err_all = np.delete(err_all, arg_port, 1)

    print('Copied', cnt, 'pair(s)')
    return cnt

if __name__ == "__main__":
    main()
