import os
import numpy as np
import cv2

def main():
    list_files = [f for f in os.listdir() if f.endswith('.jpg')]
    list_im = {'land': [], 'port': []}
    for f in list_files:
        im = cv2.imread(f)
        (y, x, _) = im.shape
        if x == 1920 and y == 1080:
            list_im['land'] += [f]
        elif x == 1080 and y == 1920:
            list_im['port'] += [f]

    err_all = []
    for land in list_im['land']:
        im_land = cv2.imread(land)
        im_land = im_land[:, (960 - 304):(960 + 304)]
        err = []
        for port in list_im['port']:
            im_port = cv2.imread(port)
            im_port = cv2.resize(im_port, (608, 1080))
            err += [np.sum((im_land - im_port) ** 2) / (608 * 1080)]
        err_all += [err]
    err_all = np.array(err_all)

    while True:
        n = len(list_im['land'])
        if not n:
            break

        (arg_land, arg_port) = np.unravel_index(np.argmin(err_all), (n, n))
        print(list_im['land'][arg_land], list_im['port'][arg_port])

        del list_im['land'][arg_land]
        del list_im['port'][arg_port]
        err_all = np.delete(err_all, arg_land, 0)
        err_all = np.delete(err_all, arg_port, 1)

if __name__ == "__main__":
    main()

