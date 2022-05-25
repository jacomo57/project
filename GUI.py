import sys

import tkinter as tk

import tkinter.ttk as ttk

from tkinter.constants import *


def main():
    root = tk.Tk()
    t = Toplevel1(root)
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    root.mainloop()


class Toplevel1:

    def __init__(self, top):
        """This class configures and populates the toplevel window.
        18            top is the toplevel containing window."""

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = 'gray40'  # X11 color: #666666
        _ana1color = '#c3c3c3'  # Closest X11 color: 'gray76'
        _ana2color = 'beige'  # X11 color: #f5f5dc
        _tabfg1 = 'black'
        _tabfg2 = 'black'
        _tabbg1 = 'grey75'
        _tabbg2 = 'grey89'
        _bgmode = 'light'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])
        top.geometry("600x450+420+150")
        top.minsize(72, 15)
        top.maxsize(1440, 855)
        top.resizable(1, 1)
        top.title("Toplevel 0")
        top.configure(background="#d9d9d9")
        self.top = top
        self.header = tk.Label(self.top)
        self.header.place(relx=0.217, rely=0.022, height=84, width=354)
        self.header.configure(anchor='w')
        self.header.configure(background="#d9d9d9")
        self.header.configure(compound='left')
        self.header.configure(cursor="")
        self.header.configure(font="-family {Comic Sans MS} -size 30")
        self.header.configure(foreground="#000000")
        self.header.configure(text='''Welcome to CloudBlocks''')
        self.sign_up_button = ttk.Button(self.top)
        self.sign_up_button.place(relx=0.05, rely=0.4, height=124, width=247)
        self.sign_up_button.configure(takefocus="")
        self.sign_up_button.configure(text='''Sign up''')
        self.sign_up_button.configure(compound='left')
        self.sign_up_button.configure(cursor="")
        self.log_in_button = ttk.Button(self.top)
        self.log_in_button.place(relx=0.533, rely=0.4, height=124, width=247)
        self.log_in_button.configure(takefocus="")
        self.log_in_button.configure(text='''Log in''')
        self.log_in_button.configure(compound='left')
        self.log_in_button.configure(cursor="")


if __name__ == '__main__':
    main()
