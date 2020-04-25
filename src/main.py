"""Main Tkinter script"""
from tkinter import Tk
from modules.App import App

if __name__ == "__main__":
    root = Tk()
    root.geometry('350x250')
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
