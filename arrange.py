import os
from PIL import Image, ImageChops
import numpy as np
import shutil
import func
import git


def filter(item_list, keyword):
    return [i for i in item_list if keyword in i]


def cosine2d(a, b):
    dot_prod = np.sum(np.multiply(a, b))
    norm1 = np.sqrt(np.sum(a ** 2))
    norm2 = np.sqrt(np.sum(b ** 2))
    return dot_prod / norm1 / norm2


def build_confusionmatrix(path, new_files, old_files):
    files_all = new_files + old_files
    n = len(new_files)
    m = len(files_all)
    confusion_matrix = np.zeros((n, m))
    for idx1, f1 in enumerate(new_files):
        im1 = np.array(Image.open(path + f1)).astype(int) / 255
        for idx2, f2 in enumerate(files_all):
            if idx2 % 100 == 99:
                print('+', end='')
            elif idx2 % 10 == 9:
                print('-', end='')
            else:
                print('.', end='')
            if idx2 < idx1:
                confusion_matrix[idx1, idx2] = -1
                continue
            im2 = np.array(Image.open(path + f2)).astype(int) / 255
            if im1.shape != im2.shape:
                confusion_matrix[idx1, idx2] = 0
                continue
            confusion_matrix[idx1, idx2] = cosine2d(im1, im2)
        print('')
    return confusion_matrix


def arrange_duplicates(img_path, new_files_land, new_files_port, old_files_land, old_files_port, confusion_matrix):
    files_all_land = new_files_land + old_files_land
    files_all_port = new_files_port + old_files_port
    for idx1, file_land1 in enumerate(new_files_land):
        n = np.argmax(confusion_matrix[idx1, :])
        file_port1 = new_files_port[idx1]
        file_land2 = files_all_land[n]
        file_port2 = files_all_port[n]
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

    repo = git.Repo(path)
    old_files = [e[0][7:] for e in repo.index.entries if e[0].startswith('images/') and e[0].endswith('.jpg')]
    old_files_land = filter(old_files, 'land')
    old_files_port = filter(old_files, 'port')
    new_files = [f[7:] for f in repo.untracked_files if f.startswith('images/') and f.endswith('.jpg')]
    new_files_land = filter(new_files, 'land')
    new_files_port = filter(new_files, 'port')
    print(len(new_files_land), 'new pair(s) will be compared with', len(old_files_land), 'old pair(s)')
    print('Building confusion matrix...')
    confusion_matrix = build_confusionmatrix(img_path, new_files_land, old_files_land)
    print('Arranging files in the folder...')
    arrange_duplicates(img_path, new_files_land, new_files_port, old_files_land, old_files_port, confusion_matrix)

if __name__ == "__main__":
    main()
