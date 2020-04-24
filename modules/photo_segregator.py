"""PhotoSegregator module for manipulating files"""

from PIL import Image, ImageChops
from datetime import date
from shutil import copy2
from os import walk, path, mkdir, listdir

permitted_ext = ('.jpg','.jpeg','.tiff','.gif','.png','.psd','.bmp','.raw','.cr2','.crw','.pict','.xmp','.dng')

def get_root_path_file_number(root_path: str) -> int:
    """Function gets number of files in paths directories and subdirectories"""
    sum = 0
    for f in walk(root_path):
        sum += len([x for x in f[2] if x.endswith(permitted_ext)])
    return sum


def copy_files_by_ranges(root_path: str, dest_path: str, date_ranges: list, *, save_unsorted: bool = True) -> list:
    """Copies all files (including subdirectories)
     from given path to destination path
     without any loss of data
     and sorts them into given subdirectories.
     """
    if save_unsorted:
        size_checked_dirs = {'Unsorted': 1}
    else:
        size_checked_dirs = {}
    error_file_list = []
    for dirpath, dirnames, filenames in walk(root_path):
        # Get files only with jpg extension
        for filename in [f for f in filenames if f.endswith(permitted_ext)]:
            try:
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

def compare_photos(path_1:str,path_2:str) -> bool:
    """Compare two photos.
        If photos are different return true
        else retrun False
    """
    img_1 = Image.open(path_1)
    img_2 = Image.open(path_2)
    diff = ImageChops.difference(img_1,img_2)
    if diff.getbbox() != None:
        return True
    else:
        return False
