import os
from PIL import Image, ImageChops
import numpy as np


def main():
    # path = os.path.expanduser('~/Pictures/win10_lockscreen/')
    path = os.path.expanduser('~/Desktop/tmp/')
    # img_path = path + 'images/'
    img_path = path

    files = [f for f in os.listdir(img_path) if f.endswith('.jpg')]
    n = len(files)
    confusion_matrix = np.zeros((n, n))
    for idx1, f1 in enumerate(files):
        print(f1)
        im1 = np.array(Image.open(path + f1)).astype(int) / 255
        for idx2, f2 in enumerate(files):
            if f1 == f2:
                confusion_matrix[idx1, idx2] = 1
                continue
            im2 = np.array(Image.open(path + f2)).astype(int) / 255
            if im1.shape != im2.shape:
                # confusion_matrix[idx1, idx2] = np.max(im1.size, im2.size)
                confusion_matrix[idx1, idx2] = 0
                continue
            # diff = np.abs(im1 - im2)
            # dist = np.sum(diff) / im1.size / 3
            # confusion_matrix[idx1, idx2] = dist
            dot_prod = np.sum(np.multiply(im1, im2))
            norm1 = np.sqrt(np.sum(im1 ** 2))
            norm2 = np.sqrt(np.sum(im2 ** 2))
            sim = dot_prod / norm1 / norm2
            confusion_matrix[idx1, idx2] = sim
    print(confusion_matrix)

if __name__ == "__main__":
    main()
