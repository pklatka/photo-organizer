"""Main App class"""

from modules.PhotoSegregator import *
from tkinter import Frame

class App(Frame):
    def __init__(self,window, *args, **kwargs):
        Frame.__init__(self, window, *args, **kwargs)
        self.window = window
