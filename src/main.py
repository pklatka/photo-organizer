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
    print("Photo organizer\n(C) Patryk Klatka 2020\n*****************\n\n")
    input("Naciśnij dowolny klawisz aby kontynuować... ")
    choise = 1
    while choise != "0":
        clear_terminal()
        print("\nWybierz opcję:\n[0] - Wyjście\n[1] - Sortowanie zdjęć\n[2] - Usuwanie duplikatów\n")
        choise = input("Twój wybór: ")
        # Sort photos by date
        if choise == "1":
            load_file = ''
            while load_file != 't' and load_file != 'n':
                load_file = input("Czy posiadasz plik z przedziałami dat zdjęć oraz z nazwami folderów? [t/n]: ").lower()
                if load_file == 't':
                    save_unsorted = ''
                    while save_unsorted != 't' and save_unsorted != 'n':
                        save_unsorted = input(
                            "Czy chcesz utworzyć osobny folder ze zdjęciami nieposortowanymi [t/n]: ").lower()
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
        elif choise == "2":
            print("Ta opcja jeszcze nie jest dostępna!")
            input("\nNaciśnij dowolny klawisz aby kontynuować... ")


except:
    print("\nCoś poszło nie tak! Spróbuj ponownie później!")
    input("\nNaciśnij dowolny klawisz aby kontynuować... ")
