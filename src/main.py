# Main command line script
from modules import PhotoSegregator as ps, PathGetter as pg

import os

# Clear terminal function
def clear_terminal():
    if os.name == 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear') 

# Start main script
try:
    print("Photo organizer\n(C) Patryk Klatka 2020\n")
    input("Naciśnij dowolny klawisz aby kontynuować... ")
    choise = 1
    while choise != "0":
        clear_terminal()
        print("\nWybierz opcję:\n[0] - Wyjście\n[1] - Sortowanie zdjęć\n[2] - Lista duplikatów\n[3] - Usuwanie duplikatów\n")
        choise = input("Twój wybór: ")
        # Sort photos by date
        if choise == "1":
            load_file = ''
            while load_file != 't' and load_file != 'n':
                load_file = input("Czy posiadasz plik z przedziałami dat zdjęć oraz z nazwami folderów? [t/n]: ").lower()
                if load_file == 't':
                    save_unsorted = ''
                    while save_unsorted != 't' and save_unsorted != 'n':
                        save_unsorted = input("Czy chcesz utworzyć osobny folder ze zdjęciami nieposortowanymi [t/n]: ").lower()
                    if save_unsorted == 't':
                        save_unsorted = True
                    elif save_unsorted == 'f':
                        save_unsorted = False
                    path = ''
                    path = pg.ask_for_file("Podaj lokalizację pliku")
                    date_ranges = []
                    file = open(path)
                    for l in file:
                        if "###" in l:
                            continue
                        date_ranges.append([f.strip() for f in l.split(',')])
                    root_path = pg.ask_for_dir("Podaj folder ze zdjęciami do posortowania")
                    dest_path = pg.ask_for_dir("Podaj folder docelowy")
                    errors = ps.order_files_by_ranges(root_path, dest_path, date_ranges, save_unsorted=save_unsorted)
                    if len(errors) == 0:
                        print("Pomyślnie posortowano zdjęcia!")
                    else:
                        print(str(len(errors)) + " plików nie zostało pomyślnie posortowanych!")
                        with open('logs.txt', "w", encoding="utf-8") as f:
                            for e in errors:
                                f.write(e + '\n')
                    input("\nNaciśnij dowolny klawisz aby kontynuować... ")
                elif load_file == 'n':
                    path = pg.ask_for_dir("Podaj miejsce zapisu pliku")
                    path += '/data.txt'
                    if not os.path.exists(path):
                        with open(path, "w", encoding="utf-8") as f:
                            f.write("### Tutaj możesz podawać zakresy dat oraz nazwy folderów\n")
                            f.write("### Wygląd jednego wpisu: Początkowa data , Końcowa data , Nazwa folderu\n")
                            f.write("### np: 28.02.2001,29.02.2001,Folder 2001\n")
                    os.startfile(path)
                    print("Wypełnij plik i spróbuj ponownie później!")
                    input("\nNaciśnij dowolny klawisz aby kontynuować... ")
        # Duplicate list
        elif choise == "2":
            dirs_num = ''
            while not dirs_num.isdigit():
                dirs_num = input("Podaj liczbę katalogów do sprawdzenia duplikatów: ")
            dirs_num = int(dirs_num)
            dirs = []
            for i in range(1,dirs_num+1):
                dir_path = pg.ask_for_dir(f'Wybierz folder nr {i}')
                dirs.append(dir_path)
            for i,path in enumerate(dirs):
                print(f'Folder nr {i+1}')
                duplicates = ps.find_duplicates(path)
                if len(duplicates) == 0:
                    print("\nBrak duplikatów!")
                else:
                    with open(f'duplikaty-nr-{i+1}.txt', "w", encoding="utf-8") as f:
                        f.write(f'Katalog: {path}')
                        for j,duplicate in enumerate(duplicates):
                            f.write(f'\n#{j+1} {"; ".join(duplicate)}')
                    print(f"\nZnaleziono duplikaty! Ścieżki podano w utworzonym pliku tekstowym (duplikaty-nr-{i+1}.txt)!")
            input("\nNaciśnij dowolny klawisz aby kontynuować... ")
        # Move duplicates
        elif choise == "3":
            dirs_num = ''
            while not dirs_num.isdigit():
                dirs_num = input("Podaj liczbę katalogów do sprawdzenia duplikatów: ")
            dirs_num = int(dirs_num)
            dirs = []
            for i in range(1,dirs_num+1):
                dir_path = pg.ask_for_dir(f'Wybierz folder nr {i}')
                dirs.append(dir_path)
            for i,path in enumerate(dirs):
                print(f'Folder nr {i+1}')
                duplicates = ps.find_duplicates(path)
                if len(duplicates) == 0:
                    print("\nBrak duplikatów!")
                else:
                    files_to_move = []
                    for d in duplicates:
                        file_to_save = min(d,key=len)
                        d.remove(file_to_save)
                        files_to_move.append(d)
                    dir_name = f'{path}/duplikaty'
                    if not os.path.exists(dir_name):
                        os.mkdir(dir_name)
                    print("Przenoszenie duplikatów")
                    err_list = ps.move_duplicates(dir_name,files_to_move)
                    if len(err_list) == 0:
                        print("\nWszystkie pliki przeniesiono poprawnie!")
                    else:
                        print(str(len(err_list)) + " plików nie zostało pomyślnie przeniesionych!")
                        with open('logs.txt', "w", encoding="utf-8") as f:
                            f.write("Nieprzeniesione pliki:\n")
                            for e in err_list:
                                f.write(e + '\n')
            input("\nNaciśnij dowolny klawisz aby kontynuować... ")

except Exception as e:
    print(str(e))
    print("\nCoś poszło nie tak! Spróbuj ponownie później!")
    input("\nNaciśnij dowolny klawisz aby kontynuować... ")
