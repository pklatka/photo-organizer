# Get path by using tkinter GUI
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

def ask_for_file(msg):
    print(msg)
    root = Tk()
    root.withdraw()
    filename = ''
    while filename == '':
        filename = askopenfilename(title=msg)
    root.destroy()
    return filename

def ask_for_dir(msg):
    print(msg)
    root = Tk()
    root.withdraw()
    filename = ''
    while filename == '':
        filename = askdirectory(title=msg)
    root.destroy()
    return filename
