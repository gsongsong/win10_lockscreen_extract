import os
from PIL import Image
from git import Repo
import func


def main():
    func.check_os()
    src_path = os.path.expanduser('~/Pictures/win10_lockscreen/')
    if not os.path.isdir(src_path):
        print('Repository does not exist. Exit.')
        exit()
    original_files = [f for f in os.listdir(src_path) if f.endswith('.jpg')]

    thumb_path = src_path + 'thumbnails/'
    if not os.path.isdir(thumb_path):
        print('Thumbnail folder does not exist. Create new one.')
        os.mkdir(thumb_path)
    thumb_files = [f for f in os.listdir(thumb_path) if f.endswith('.jpg')]

    for fname in original_files:
        if fname in thumb_files:
            continue
        im = Image.open(src_path + fname)
        (x, y) = im.size
        h = 270
        w = x * h / y
        im.thumbnail((w, h), Image.ANTIALIAS)
        im.save(thumb_path + fname, 'JPEG')
        thumb_files += [fname]

    html_file = open(src_path + 'index.html', 'w')
    html_file.write('<head>'
                    '<title>Windows 10 Lockscreens</title>'
                    '</head>'
                    '<div style="text-align:center;">'
                    '<h1>Windows 10 Lockscreens</h1>')
    cnt = 1
    for fname in thumb_files:
        html_file.write('<a href=' + fname + '>'
                        '<img src=thumbnails/' + fname + '> '
                        '</a>')
        cnt += 1
        if cnt % 2:
            html_file.write('<br />')
    html_file.write('</div>')

if __name__ == "__main__":
    main()
