import os
import util
import pathlib

dir = "D:\\picsHres\\1950s\\1959-05-15 Baba Badi Ma Wedding"
lst = os.listdir(dir)
util.pprint(lst)

nlst = [os.path.splitext(x)[1] for x in lst]
print(nlst)

def is_media(file):
    ext = os.path.splitext(file)[1]
    return ext in ['.jpg', '.png', '.gif', '.mov']

files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and is_media(f)]
util.pprint(files)

pathlib.Path('abc.tar.gz.jpg').suffix

dirnames = [d for d in lst if os.path.isdir(os.path.join(dir,d))]
util.pprint(dirnames)