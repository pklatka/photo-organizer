from modules.PhotoSegregator import *
from datetime import date

date_ranges = [
    ('Paris 2007', date(2007, 9, 16), date(2007, 9, 16)),
    ('Cracow 2008', date(2007, 9, 16), date(2007, 9, 17)),
]

root_path = r"C:\Users\Patryk\Desktop\!odzysk_arvika\JPG\2007"
dest_path = r'C:\Users\Patryk\Desktop\backup\xd\jeb'

print(get_file_number(root_path))
errors = order_files_by_ranges(root_path, dest_path, date_ranges, save_unsorted=False)
if len(errors) == 0:
    print("Pomyślnie posortowano zdjęcia!")
else:
    print(str(len(errors)) + " plików nie zostało pomyślnie posortowanych!")
    with open('logs.txt', "w", encoding="utf-8") as f:
        for e in errors:
            f.write(e+'\n')

# print(find_duplicates(root_path))