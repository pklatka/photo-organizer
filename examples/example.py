from modules.photo_segregator import *
from datetime import date

date_ranges = [
    ('Paris 2007', date(2007, 9, 16), date(2007, 9, 16)),
    ('Paryż 2008', date(2007, 9, 16), date(2007, 9, 17)),
]

root_path = r"C:\Users\Test\Desktop\dest_dir"
dest_path = r'C:\Users\Test\Desktop\backup'

print(get_root_path_file_number(root_path))
print(copy_files_by_ranges(root_path,dest_path,date_ranges,save_unsorted=False))
print(compare_photos(r"C:\Users\Patryk\Desktop\back\1.jpg",r"C:\Users\Patryk\Desktop\back\2.jpg"))