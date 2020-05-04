# Get path by using tkinter GUI
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

def ask_for_file(msg):
    root = Tk()
    root.withdraw()
    filename = askopenfilename(title=msg)
    root.destroy()
    return filename

def ask_for_dir(msg):
    root = Tk()
    root.withdraw()
    filename = askdirectory(title=msg)
    root.destroy()
    return filename