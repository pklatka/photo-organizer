from modules.PhotoSegregator import *
from datetime import date

date_ranges = [
    ('Paris 2007', date(2007, 9, 16), date(2007, 9, 16)),
    ('Cracow 2008', date(2007, 9, 16), date(2007, 9, 17)),
]

root_path = r"C:\Users\Test\Desktop\dest_dir"
dest_path = r'C:\Users\Test\Desktop\backup'

print(get_file_number(root_path))
print(order_files_by_ranges(root_path,dest_path,date_ranges,save_unsorted=False))
print(find_duplicates(root_path))