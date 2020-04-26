"""Main App class"""

from modules.PhotoSegregator import *
import tkinter as tk
from os import path

class App:
    def __init__(self,width,height):
        self.w = width
        self.h = height
        # self.font = tk.
        self.generate_window()

    def generate_window(self):
        self.root = tk.Tk()
        self.root.minsize(self.w,self.h)
        self.root.iconbitmap(path.abspath("../resources/icon.ico"))
        self.root.title('Photo organizer')
        self.root.tk.call('tk', 'scaling', 3.0)
        # Wrapper frame
        self.wrapper = tk.Frame(self.root)
        self.wrapper.place(relx=0,rely=0,relwidth=1,relheight=1)
        # Initialize components
        self.header_component()
        self.navigation_component()
        self.main_component()
        # Main loop
        self.root.mainloop()

    def header_component(self):
        self.header = tk.Frame(self.wrapper,height=75,bg='darkgray')
        self.header.place(relx=0,rely=0,relwidth=1)
        # Logo
        self.header_logo = tk.Canvas(self.header,bg='darkgray',bd=0,highlightthickness=0, width=60, height=60)
        self.header_logo_img = tk.PhotoImage(file=path.abspath("../resources/logo.png"))
        self.header_logo.create_image(0, 0, anchor='nw', image=self.header_logo_img)
        self.header_logo.place(x=7.5,y=7.5)
        # Title
        self.header_label = tk.Label(self.header,font=('Ariel Bold',10),text='Photo organizer',bg='darkgray')
        self.header_label.place(x=75,y=8)
        self.header_version = tk.Label(self.header,font=('Ariel Bold',4),text='Version 0.1 (C) Patryk Klatka 2020',bg='darkgray')
        self.header_version.place(x=75,y=45)

    def navigation_component(self):
        self.nav = tk.Frame(self.wrapper,bg='gray')
        self.nav.place(x=0,y=75,width=200,relheight=1)
        self.nav_link_1 = tk.Button(self.nav,text='Organize files',font=('Ariel Bold',7),highlightthickness = 0, bd = 0)
        self.nav_link_1.place(relwidth=1,y=0,height=100)
        self.nav_link_2 = tk.Button(self.nav,text='Remove duplicates',font=('Ariel Bold',7),bg='black',highlightthickness=0, bd=0)
        self.nav_link_2.place(relwidth=1,y=100,height=100)

    def main_component(self):
        self.main = tk.Frame(self.wrapper,bg='white')
        self.main.place(x=200,y=75,relwidth=1,relheight=1)
