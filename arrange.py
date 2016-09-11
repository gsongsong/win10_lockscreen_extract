import os
from PIL import Image, ImageChops
import numpy as np
import shutil
import func


def cosine2d(a, b):
    dot_prod = np.sum(np.multiply(a, b))
    norm1 = np.sqrt(np.sum(a ** 2))
    norm2 = np.sqrt(np.sum(b ** 2))
    return dot_prod / norm1 / norm2


def build_confusionmatrix(path, files):
    n = len(files)
    confusion_matrix = np.zeros((n, n))
    for idx1, f1 in enumerate(files):
        print(idx1 + 1, '/', n)
        im1 = np.array(Image.open(path + f1)).astype(int) / 255
        for idx2, f2 in enumerate(files):
            if idx2 < idx1:
                confusion_matrix[idx1, idx2] = -1
                continue
            if f1 == f2:
                confusion_matrix[idx1, idx2] = -1
                continue
            im2 = np.array(Image.open(path + f2)).astype(int) / 255
            if im1.shape != im2.shape:
                # confusion_matrix[idx1, idx2] = np.max(im1.size, im2.size)
                confusion_matrix[idx1, idx2] = 0
                continue
            confusion_matrix[idx1, idx2] = cosine2d(im1, im2)
    return confusion_matrix


def arrange_duplicates(img_path, list_land, list_port, confusion_matrix):
    for idx1, file_land1 in enumerate(list_land):
        n = np.argmax(confusion_matrix[idx1, :])
        file_land2 = list_land[n]
        file_port1 = list_port[idx1]
        file_port2 = list_port[n]
        if confusion_matrix[idx1, n] > 0.98:
            size1 = os.path.getsize(img_path + file_land1)
            size2 = os.path.getsize(img_path + file_land2)
            smaller_file_land = file_land1 if size1 < size2 else file_land2
            smaller_file_port = file_port1 if size1 < size2 else file_port2
            shutil.move(img_path + smaller_file_land, img_path + 'dups/' + smaller_file_land)
            shutil.move(img_path + smaller_file_port, img_path + 'dups/' + smaller_file_port)


def main():
    func.check_os()
    path = os.path.expanduser('~/Pictures/win10_lockscreen/')
    img_path = path + 'images/'

    files = [f for f in os.listdir(img_path) if f.endswith('.jpg')]
    list_land = [f for f in files if 'land' in f]
    list_port = [f for f in files if 'port' in f]
    print('Building confusion matrix...')
    confusion_matrix = build_confusionmatrix(img_path, list_land)
    arrange_duplicates(img_path, list_land, list_port, confusion_matrix)

if __name__ == "__main__":
    main()
