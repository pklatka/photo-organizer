"""PhotoSegregator module for manipulating files"""

from PIL import Image, ImageFile
from PIL.ImageStat import Stat
from datetime import date
from shutil import copy2
from os import walk, path, mkdir, listdir, replace
from tqdm import tqdm
from sys import stdout

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Allowed file extensions
permitted_ext = (
    '.jpg', '.jpeg', '.tiff', '.gif', '.png', '.psd', '.bmp', '.raw', '.cr2', '.crw', '.pict', '.xmp', '.dng')

def get_file_number(root_path: str) -> int:
    """Function gets number of files in paths directories and subdirectories with permitted extension"""
    sum = 0
    for f in walk(root_path):
        sum += len([x for x in f[2] if x.endswith(permitted_ext)])
    return sum

def order_files_by_ranges(root_path: str, dest_path: str, date_ranges: list, *, save_unsorted: bool = True) -> list:
    """Copies all files (including subdirectories)
     from given path to destination path
     without any loss of data
     and groups them into given subdirectories.
     """
    t = tqdm(range(get_file_number(root_path)),unit=' img',desc='Progress',file=stdout)
    error_file_list = []
    if save_unsorted:
        size_checked_dirs = {'Unsorted': 1}
    else:
        size_checked_dirs = {}
    for dirpath, dirnames, filenames in walk(root_path):
        # Get files only with jpg extension
        for filename in filenames:
            try:
                if not filename.endswith(permitted_ext):
                    continue
                t.update(1)
                t.refresh()
                # Get EXIF file data
                tmp_path = path.join(dirpath, filename)
                img = Image.open(tmp_path)
                exif_data = img._getexif()
                # Get year, month and day from EXIF dictionary
                year, month, day = exif_data[36867][:10].split(':')
                # Check if date is in range
                # Else check if image was copied (why not for/else - user can select ranges that overlap each other)
                copied = False
                for n in date_ranges:
                    d1 = n[0].split('.')
                    d1 = date(int(d1[2]),int(d1[1]),int(d1[0]))
                    d2 = n[1].split('.')
                    d2 = date(int(d2[2]),int(d2[1]),int(d2[0]))
                    if d1 <= date(int(year), int(month), int(day)) <= d2:
                        dir_path = path.join(dest_path, n[2])
                        # Get size of directory to estimate zfill value
                        if dir_path not in size_checked_dirs.keys():
                            size_checked_dirs[dir_path] = [1, len(str(len(listdir(dirpath))))]
                        # Create folder if doesn't exists
                        if not path.isdir(dir_path):
                            mkdir(dir_path)
                        photo_id = str(size_checked_dirs[dir_path][0]).zfill(size_checked_dirs[dir_path][1])
                        copy2(tmp_path, path.join(dir_path, f'{year}-{month}-{day} - {photo_id}.jpg'))
                        size_checked_dirs[dir_path][0] += 1
                        copied = True
                if save_unsorted and not copied:
                    dir_path = path.join(dest_path, 'Unsorted')
                    if not path.isdir(dir_path):
                        mkdir(dir_path)
                    photo_id = str(size_checked_dirs['Unsorted']).zfill(5)
                    copy2(tmp_path, path.join(dir_path, f'{year}-{month}-{day} - {photo_id}.jpg'))
                    size_checked_dirs['Unsorted'] += 1
            except:
                error_file_list.append(tmp_path)
                continue
    t.close()
    return error_file_list


def find_duplicates(root_path:str):
    """Remove duplicate photos by substracting
    sum of all pixels for each band in the image.
    """
    # Prepare dict with ImageObjects
    photos = {}
    print("\nIndeksowanie plików...")
    files = listdir(root_path)
    t1 = tqdm(range(len(files)),unit=' img',file=stdout,desc='Progress')
    for filename in files:
        # Get files only with permitted extension
        err = []
        t1.update(1)
        t1.refresh()
        if not filename.endswith(permitted_ext):
            continue
        else:
            try:
                img_path = path.join(root_path, filename).replace('\\','/')
                img = Image.open(img_path)
                photos[img_path] = sum(Stat(img)._getsum())
            except:
                err.append(filename)
                continue
    t1.close()
    if len(err) > 0:
        print("\nNie udało się zindexować wszystkich plików!\nLista plików dostępna w logs-indexing.txt")
        with open('logs-indexing.txt', "w", encoding="utf-8") as f:
            for e in err:
                f.write(e + '\n')
    print("\nSprawdzanie plików...")
    t2 = tqdm(range(len(photos)),unit=' img',desc='Progress',file=stdout)
    duplicates = []
    p = list(photos.keys())
    # O(n^2) algorithm
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            # Faster expression than difference method in ImageChops module
            try:
                img1 = photos[p[i]]
                diff = img1 - photos[p[j]]
                if diff == 0.0:
                    exists_tuple = [i for i,x in enumerate(duplicates) if x[0] == img1]
                    if len(exists_tuple) == 0:
                        duplicates.append([img1,p[i], p[j]])
                    else:
                        if p[i] not in duplicates[exists_tuple[0]]:
                            duplicates[exists_tuple[0]].append(p[i])
                        if p[j] not in duplicates[exists_tuple[0]]:
                            duplicates[exists_tuple[0]].append(p[j])
                else:
                    continue
            except Exception as e:
                print(str(e))
        t2.update(1)
        t2.refresh()
    if len(duplicates) > 0:
        for duplicate in duplicates:
            duplicate.pop(0)
    t2.close()
    return duplicates

def move_duplicates(dest_path:str, duplicates:list):
    print("\nPrzenoszenie duplikatów...")
    t = tqdm(range(len(duplicates)),unit=' img',desc='Progress',file=stdout)
    err = []
    for duplicate in duplicates:
        for file in duplicate:
            move_path = dest_path+'/'+file.split('/')[-1]
            try:
                replace(file,move_path)
            except:
               err.append(move_path)
            t.update(1)
            t.refresh()
    t.close()
    return err

def segregate_photos(root_path:str):
    dst_path = root_path + '/other'
    if not path.exists(dst_path):
        mkdir(dst_path)
    files = listdir(root_path)
    t = tqdm(range(len(files)),unit=' img',desc='Progress',file=stdout)
    err = []
    for filename in files:
        t.update(1)
        t.refresh()
        try:
            file_path = path.join(root_path, filename).replace('\\', '/')
            # Get files only with permitted extension
            if not filename.endswith(permitted_ext) and not path.isdir(file_path):
                replace(file_path, root_path + '/other/' + filename)
            else:
                continue
        except:
            err.append(filename)
    t.close()
    return err