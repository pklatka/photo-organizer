"""PhotoSegregator module for manipulating files"""

from PIL import Image
from PIL.ImageStat import Stat
from datetime import date
from shutil import copy2
from os import walk, path, mkdir, listdir

# Allowed file extensions
permitted_ext = (
    '.jpg', '.jpeg', '.tiff', '.gif', '.png', '.psd', '.bmp', '.raw', '.cr2', '.crw', '.pict', '.xmp', '.dng')
# Progress value
progress_bar = 0

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
    error_file_list = []
    progress_bar = 0
    if save_unsorted:
        size_checked_dirs = {'Unsorted': 1}
    else:
        size_checked_dirs = {}
    for dirpath, dirnames, filenames in walk(root_path):
        # Get files only with jpg extension
        for filename in filenames:
            progress_bar += 1
            try:
                if not filename.endswith(permitted_ext):
                    continue
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
                    if n[1] <= date(int(year), int(month), int(day)) <= n[2]:
                        dir_path = path.join(dest_path, n[0])
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
                error_file_list.append(filename)
                continue
    return error_file_list


def find_duplicates(root_path:str):
    """Remove duplicate photos by substracting
    sum of all pixels for each band in the image.
    """
    progress_bar = 0
    # Prepare dict with ImageObjects
    photos = {}
    for dirpath, dirnames, filenames in walk(root_path):
        # Get files only with permitted extension
        for filename in filenames:
            if not filename.endswith(permitted_ext):
                continue
            else:
                img_path = path.join(dirpath, filename)
                img = Image.open(img_path)
                photos[img_path] = img
    duplicates = []
    p = list(photos.keys())
    # O(n^2) algorithm
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            progress_bar += 1
            # Faster expression than difference method in ImageChops module
            diff = sum(Stat(photos[p[i]])._getsum())-sum(Stat(photos[p[j]])._getsum())
            if diff == 0.0:
                duplicates.append((p[i], p[j]))
            else:
                continue
    return duplicates
