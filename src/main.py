"""Main command line script"""

import PhotoSegregator as ps
import PathGetter as pg

import os

# Clear terminal function
def clear_terminal():
    if os.name == 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear') 

# Start main script
try:
    print("Photo organizer\n(C) Patryk Klatka 2021\n")
    input("Press any key to continue... ")
    choice = 1
    while choice != "0":
        clear_terminal()
        print("\nSelect option:\n[0] - Exit\n[1] - Sort and copy photos by creation date\n[2] - Generate list with photo duplicates\n[3] - Extract photo duplicates in a folder/s\n[4] - Extract other files than photos in a folder/s\n")
        choice = input("Your choice: ")
        # Sort photos by date
        if choice == "1":
            load_file = ''
            while load_file != 'y' and load_file != 'n':
                load_file = input("Do you have a file with date ranges and folder names? [y/n]: ").lower()
                if load_file == 'y':
                    save_unsorted = ''
                    while save_unsorted != 'y' and save_unsorted != 'n':
                        save_unsorted = input("Do you want to create separate folder with unsorted photos? [y/n]: ").lower()
                    if save_unsorted == 'y':
                        save_unsorted = True
                    elif save_unsorted == 'n':
                        save_unsorted = False
                    path = ''
                    path = pg.ask_for_file("Enter the location of the file")
                    date_ranges = []
                    file = open(path)
                    for l in file:
                        if "###" in l:
                            continue
                        date_ranges.append([f.strip() for f in l.split(',')])
                    root_path = pg.ask_for_dir("Select a folder with photos to sort")
                    dest_path = pg.ask_for_dir("Select destination folder")
                    errors = ps.order_files_by_ranges(root_path, dest_path, date_ranges, save_unsorted=save_unsorted)
                    if len(errors) == 0:
                        print("Images successfully sorted!")
                    else:
                        print(str(len(errors)) + " files were not successfully sorted!")
                        with open('logs-sorting.txt', "w", encoding="utf-8") as f:
                            for e in errors:
                                f.write(e + '\n')
                    input("\nPress any key to continue... ")
                elif load_file == 'n':
                    path = pg.ask_for_dir("Specify where to save the file")
                    path += '/data.txt'
                    if not os.path.exists(path):
                        with open(path, "w", encoding="utf-8") as f:
                            f.write("### Here you can specify date ranges and folder names.\n")
                            f.write("### Appearance of one entry: Start date (DD.MM.YYYY) , End date (DD.MM.YYYY) , Folder name.\n")
                            f.write("### Example: 28.02.2001,29.02.2001,Photos 2001\n")
                    os.startfile(path)
                    print("Fill out the file and try again later!")
                    input("\nPress any key to continue... ")
        # Duplicate list
        elif choice == "2":
            dirs_num = ''
            while not dirs_num.isdigit():
                dirs_num = input("Specify the number of directories to check for photo duplicates: ")
            dirs_num = int(dirs_num)
            dirs = []
            for i in range(1,dirs_num+1):
                dir_path = pg.ask_for_dir(f'Select folder no. {i}')
                dirs.append(dir_path)
            for i,path in enumerate(dirs):
                print(f'Folder no. {i+1}')
                duplicates = ps.find_duplicates(path)
                if len(duplicates) == 0:
                    print("\nNo photo duplicates!")
                else:
                    with open(os.path.join(path,f'duplicates-no-{i+1}.txt'), "w", encoding="utf-8") as f:
                        f.write(f'Directory: {path}')
                        for j,duplicate in enumerate(duplicates):
                            f.write(f'\n#{j+1} {"; ".join(duplicate)}')
                    print(f"\nDuplicates in folder no. {j+1} were found! Paths were provided in the text file created in folders directory.")
            input("\nPress any key to continue... ")
        # Move duplicates
        elif choice == "3":
            dirs_num = ''
            while not dirs_num.isdigit():
                dirs_num = input("Specify the number of directories to check for photo duplicates: ")
            dirs_num = int(dirs_num)
            dirs = []
            for i in range(1,dirs_num+1):
                dir_path = pg.ask_for_dir(f'Select folder no. {i}')
                dirs.append(dir_path)
            for i,path in enumerate(dirs):
                print(f'\nFolder no. {i+1}')
                duplicates = ps.find_duplicates(path)
                if len(duplicates) == 0:
                    print("\nNo photo duplicates!")
                else:
                    files_to_move = []
                    for d in duplicates:
                        file_to_save = min(d,key=len)
                        d.remove(file_to_save)
                        files_to_move.append(d)
                    dir_name = f'{path}/duplicates'
                    if not os.path.exists(dir_name):
                        os.mkdir(dir_name)
                    err_list = ps.move_duplicates(dir_name,files_to_move)
                    if len(err_list) == 0:
                        print("\nAll files were transferred correctly!")
                    else:
                        print('\n'+str(len(err_list)) + " files have not been transferred successfully!")
                        with open('logs-duplicates.txt', "w", encoding="utf-8") as f:
                            f.write("Error files:\n")
                            for e in err_list:
                                f.write(e + '\n')
            input("\nPress any key to continue... ")
        # Move photos to separate folder
        elif choice == "4":
            dirs_num = ''
            while not dirs_num.isdigit():
                dirs_num = input("Enter the number of directories to check for duplicates: ")
            dirs_num = int(dirs_num)
            dirs = []
            for i in range(1, dirs_num + 1):
                dir_path = pg.ask_for_dir(f'Select folder no. {i}')
                dirs.append(dir_path)
            for i, path in enumerate(dirs):
                print(f'\nFolder no. {i + 1}')
                err = ps.segregate_photos(path)
                if len(err) == 0:
                    print("Files were sorted successfully!")
                else:
                    print('\n' + str(len(err)) + " files have not been transferred successfully!")
                    with open('logs-moving.txt', "w", encoding="utf-8") as f:
                        f.write("Error files:\n")
                        for e in err:
                            f.write(e + '\n')
            input("\nPress any key to continue... ")

except Exception as e:
    print(str(e))
    print("\nSomething went wrong... Please try again!")
    input("\nPress any key to continue... ")
