import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

# Support code for Balloon Help (also called tooltips).
# derived from http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
from time import time, localtime, strftime


def main():
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)  # Creates a toplevel widget.
    w1 = Toplevel1(root)
    root.mainloop()


class Toplevel1:
    def __init__(self, user, root=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
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
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        root.geometry("942x571+730+263")
        root.minsize(120, 1)
        root.maxsize(4244, 1421)
        root.resizable(1, 1)
        root.title("Toplevel 0")
        root.configure(background="#d9d9d9")

        self.root = root
        self.user = user

        self.login_page = tk.Frame(self.root)
        self.login_page.place(relx=0.0, rely=0.105, relheight=0.904, relwidth=1.015)
        self.login_page.configure(relief='groove')
        self.login_page.configure(borderwidth="2")
        self.login_page.configure(relief="groove")
        self.login_page.configure(background="#d9d9d9")

        self.login_labelframe = tk.LabelFrame(self.login_page)
        self.login_labelframe.place(relx=0.021, rely=0.019, relheight=0.94, relwidth=0.509)
        self.login_labelframe.configure(relief='groove')
        self.login_labelframe.configure(foreground="#000000")
        self.login_labelframe.configure(text='''Login''')
        self.login_labelframe.configure(background="#d9d9d9")
        self.login_labelframe.configure(cursor="")

        self.login_header = tk.Label(self.login_labelframe)
        self.login_header.place(relx=0.064, rely=0.062, height=46, width=330, bordermode='ignore')
        self.login_header.configure(activebackground="#f9f9f9")
        self.login_header.configure(anchor='w')
        self.login_header.configure(background="#d9d9d9")
        self.login_header.configure(compound='left')
        self.login_header.configure(disabledforeground="#a3a3a3")
        self.login_header.configure(font="-family {Times New Roman} -size 24")
        self.login_header.configure(foreground="#000000")
        self.login_header.configure(highlightbackground="#d9d9d9")
        self.login_header.configure(highlightcolor="black")
        self.login_header.configure(text='''Log In''')

        self.username_label = tk.Label(self.login_labelframe)
        self.username_label.place(relx=0.064, rely=0.186, height=37, width=114, bordermode='ignore')
        self.username_label.configure(activebackground="#f9f9f9")
        self.username_label.configure(anchor='w')
        self.username_label.configure(background="#d9d9d9")
        self.username_label.configure(compound='left')
        self.username_label.configure(disabledforeground="#a3a3a3")
        self.username_label.configure(font="-family {Times New Roman} -size 18")
        self.username_label.configure(foreground="#000000")
        self.username_label.configure(highlightbackground="#d9d9d9")
        self.username_label.configure(highlightcolor="black")
        self.username_label.configure(text='''Username''')

        self.username_entry = tk.Entry(self.login_labelframe)
        self.username_entry.place(relx=0.064, rely=0.289, height=60, relwidth=0.809, bordermode='ignore')
        self.username_entry.configure(background="white")
        self.username_entry.configure(disabledforeground="#a3a3a3")
        self.username_entry.configure(font="-family {Times New Roman} -size 16")
        self.username_entry.configure(foreground="#000000")
        self.username_entry.configure(highlightbackground="#d9d9d9")
        self.username_entry.configure(highlightcolor="black")
        self.username_entry.configure(selectbackground="#c4c4c4")
        self.username_entry.configure(selectforeground="black")

        self.block_label = tk.Label(self.login_labelframe)
        self.block_label.place(relx=0.064, rely=0.454, height=38, width=147, bordermode='ignore')
        self.username_entry.configure(insertbackground="black")
        self.block_label.configure(activebackground="#f9f9f9")
        self.block_label.configure(anchor='w')
        self.block_label.configure(background="#d9d9d9")
        self.block_label.configure(compound='left')
        self.block_label.configure(disabledforeground="#a3a3a3")
        self.block_label.configure(font="-family {Times New Roman} -size 18")
        self.block_label.configure(foreground="#000000")
        self.block_label.configure(highlightbackground="#d9d9d9")
        self.block_label.configure(highlightcolor="black")
        self.block_label.configure(text='''Genesis Block''')
        self.choose_file_button = ttk.Button(self.login_labelframe)
        self.choose_file_button.place(relx=0.064, rely=0.536, height=55, width=416, bordermode='ignore')
        self.choose_file_button.configure(takefocus="")
        self.choose_file_button.configure(text='''Choose file''')
        self.choose_file_button.configure(compound='left')
        self.tooltip_font = "TkDefaultFont"
        self.choose_file_button_tooltip = ToolTip(self.choose_file_button, self.tooltip_font, '''Opens file explorer''')
        self.login_button = ttk.Button(self.login_labelframe)
        self.login_button.place(relx=0.064, rely=0.68, height=85, width=416, bordermode='ignore')
        self.login_button.configure(takefocus="")
        self.login_button.configure(text='''Log in''')
        self.login_button.configure(compound='left')

        self.signup_labelframe = tk.LabelFrame(self.login_page)
        self.signup_labelframe.place(relx=0.554, rely=0.019, relheight=0.94, relwidth=0.417)
        self.signup_labelframe.configure(relief='groove')
        self.signup_labelframe.configure(foreground="#000000")
        self.signup_labelframe.configure(text='''Signup''')
        self.signup_labelframe.configure(background="#d9d9d9")

        self.username_label_signup = tk.Label(self.signup_labelframe)
        self.username_label_signup.place(relx=0.05, rely=0.186, height=37, width=114, bordermode='ignore')
        self.username_label_signup.configure(activebackground="#f9f9f9")
        self.username_label_signup.configure(anchor='w')
        self.username_label_signup.configure(background="#d9d9d9")
        self.username_label_signup.configure(compound='left')
        self.username_label_signup.configure(disabledforeground="#a3a3a3")
        self.username_label_signup.configure(font="-family {Times New Roman} -size 18")
        self.username_label_signup.configure(foreground="#000000")
        self.username_label_signup.configure(highlightbackground="#d9d9d9")
        self.username_label_signup.configure(highlightcolor="black")
        self.username_label_signup.configure(text='''Username''')

        self.username_entry_signup = tk.Entry(self.signup_labelframe)
        self.username_entry_signup.place(relx=0.05, rely=0.289, height=60, relwidth=0.887, bordermode='ignore')
        self.username_entry_signup.configure(background="white")
        self.username_entry_signup.configure(disabledforeground="#a3a3a3")
        self.username_entry_signup.configure(font="-family {Times New Roman} -size 16")
        self.username_entry_signup.configure(foreground="#000000")
        self.username_entry_signup.configure(highlightbackground="#d9d9d9")
        self.username_entry_signup.configure(highlightcolor="black")
        self.username_entry_signup.configure(insertbackground="black")
        self.username_entry_signup.configure(selectbackground="#c4c4c4")
        self.username_entry_signup.configure(selectforeground="black")

        self.sign_up_button = ttk.Button(self.signup_labelframe)
        self.sign_up_button.place(relx=0.064, rely=0.536, height=85, width=356, bordermode='ignore')
        self.sign_up_button.configure(takefocus="")
        self.sign_up_button.configure(text='''Sign up''')
        self.sign_up_button.configure(compound='left')
        self.sign_up_button.configure(command=self.sign_up_clicked)

        self.header = tk.Label(self.root)
        self.header.place(relx=0.0, rely=-0.018, height=65, width=941)
        self.header.configure(activebackground="#f9f9f9")
        self.header.configure(background="#7bbfac")
        self.header.configure(compound='left')
        self.header.configure(disabledforeground="#a3a3a3")
        self.header.configure(font="-family {Times New Roman} -size 30 -weight bold")
        self.header.configure(foreground="#ffffff")
        self.header.configure(highlightbackground="#d9d9d9")
        self.header.configure(highlightcolor="black")
        self.header.configure(text='''CloudBlocks''')

        self.homepage = tk.Frame(self.root)
        self.homepage.place(relx=0.0, rely=0.105, relheight=0.902, relwidth=1.006)
        self.homepage.configure(relief='groove')
        self.homepage.configure(borderwidth="2")
        self.homepage.configure(relief="groove")
        self.homepage.configure(background="#d9d9d9")

        self.login_page.tkraise()

    def sign_up_clicked(self):
        name = self.username_entry_signup.get()
        return name

    def login_clicked(self):  # Needs to get file for block and stuff
        name = self.username_entry.get()
        block = None
        return [name, block]


class ToolTip(tk.Toplevel):
    """ Provides a ToolTip widget for Tkinter. """

    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None, delay=0.5, follow=True):
        self.wdgt = wdgt
        self.parent = self.wdgt.master
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        self.withdraw()
        self.overrideredirect(True)
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                   font=tooltip_font,
                   aspect=1000).grid()
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        self.visible = 1
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        self.lastMotion = time()
        if self.follow is False:
            self.withdraw()
            self.visible = 1
        self.geometry('+%i+%i' % (event.x_root + 20, event.y_root - 10))
        try:
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        self.visible = 0
        self.withdraw()

    def update(self, msg):
        self.msgVar.set(msg)


if __name__ == "__main__":
    main()
