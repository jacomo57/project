import pickle
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, simpledialog
from tkinter.constants import *

# Support code for Balloon Help (also called tooltips).
# derived from http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
from time import time, localtime, strftime

from BlockFolder import BlockFolder
from BlockFile import BlockFile
from Networker import Networker


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
        self.networker = Networker()
        self.next_networker = Networker()

        self.header = tk.Label(self.root)
        self.header.place(relx=0.0, rely=-0.018, height=65, width=810)
        self.header.configure(activebackground="#f9f9f9")
        self.header.configure(background="#7bbfac")
        self.header.configure(compound='left')
        self.header.configure(disabledforeground="#a3a3a3")
        self.header.configure(font="-family {Times New Roman} -size 30 -weight bold")
        self.header.configure(foreground="#ffffff")
        self.header.configure(highlightbackground="#d9d9d9")
        self.header.configure(highlightcolor="black")
        self.header.configure(text='''CloudBlocks''')

        self.exit_button = ttk.Button(self.root)
        self.exit_button.place(relx=0.849, rely=0.0, height=65, width=146)
        self.exit_button.configure(takefocus="")
        self.exit_button.configure(text='''Exit Program''')
        self.exit_button.configure(compound='left')
        self.exit_button.configure(command=self.exit_program)

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

        self.login_button = ttk.Button(self.login_labelframe)
        self.login_button.place(relx=0.064, rely=0.536, height=85, width=416, bordermode='ignore')
        self.login_button.configure(takefocus="")
        self.login_button.configure(text='''Log in''')
        self.login_button.configure(compound='left')
        self.login_button.configure(command=self.login_clicked)

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

        self.login_page.tkraise()

        self.root.mainloop()

    def make_homepage(self):
        self.homepage = tk.Frame(self.root)
        self.homepage.place(relx=0.0, rely=0.105, relheight=0.902, relwidth=1.006)
        self.homepage.configure(relief='groove')
        self.homepage.configure(borderwidth="2")
        self.homepage.configure(relief="groove")
        self.homepage.configure(background="#d9d9d9")

        self.welcome_label = tk.Label(self.homepage)
        self.welcome_label.place(relx=0.042, rely=0.001, height=71, width=500)
        self.welcome_label.configure(anchor='w')
        self.welcome_label.configure(background="#d9d9d9")
        self.welcome_label.configure(compound='left')
        self.welcome_label.configure(disabledforeground="#a3a3a3")
        self.welcome_label.configure(font="-family {Times New Roman} -size 24")
        self.welcome_label.configure(foreground="#000000")
        self.welcome_label.configure(text="Welcome " + self.user.user_name)

        self.user_actions_labelframe = tk.LabelFrame(self.homepage)
        self.user_actions_labelframe.place(relx=0.021, rely=0.117, relheight=0.845, relwidth=0.37)
        self.user_actions_labelframe.configure(relief='groove')
        self.user_actions_labelframe.configure(foreground="#000000")
        self.user_actions_labelframe.configure(text='''User Actions''')
        self.user_actions_labelframe.configure(background="#d9d9d9")

        self.make_folder_button = ttk.Button(self.user_actions_labelframe)
        self.make_folder_button.place(relx=0.058, rely=0.046, height=55, width=300, bordermode='ignore')
        self.make_folder_button.configure(takefocus="")
        self.make_folder_button.configure(text='''Save Folder''')
        self.make_folder_button.configure(compound='left')
        self.make_folder_button.configure(command=self.make_folder_clicked)

        self.make_file_button = ttk.Button(self.user_actions_labelframe)
        self.make_file_button.place(relx=0.058, rely=0.207, height=55, width=300, bordermode='ignore')
        self.make_file_button.configure(takefocus="")
        self.make_file_button.configure(text='''Save Files''')
        self.make_file_button.configure(compound='left')
        self.make_file_button.configure(command=self.make_file_clicked)

        self.load_button = ttk.Button(self.user_actions_labelframe)
        self.load_button.place(relx=0.058, rely=0.368, height=55, width=300, bordermode='ignore')
        self.load_button.configure(takefocus="")
        self.load_button.configure(text='''Block Info''')
        self.load_button.configure(compound='left')
        self.load_button.configure(command=self.load_button_clicked)

        self.traverse_button = ttk.Button(self.user_actions_labelframe)
        self.traverse_button.place(relx=0.058, rely=0.529, height=55, width=300, bordermode='ignore')
        self.traverse_button.configure(takefocus="")
        self.traverse_button.configure(text='''Traverse''')
        self.traverse_button.configure(compound='left')
        self.traverse_button.configure(command=self.traverse_button_clicked)

        self.delete_button = ttk.Button(self.user_actions_labelframe)
        self.delete_button.place(relx=0.058, rely=0.69, height=55, width=300, bordermode='ignore')
        self.delete_button.configure(takefocus="")
        self.delete_button.configure(text='''Delete Block''')
        self.delete_button.configure(compound='left')

        self.get_file_button = ttk.Button(self.user_actions_labelframe)
        self.get_file_button.place(relx=0.058, rely=0.851, height=55, width=300, bordermode='ignore')
        self.get_file_button.configure(takefocus="")
        self.get_file_button.configure(text='''Get File''')
        self.get_file_button.configure(compound='left')
        self.get_file_button.configure(command=self.get_file_clicked)

        self.treeview_labelframe = tk.LabelFrame(self.homepage)
        self.treeview_labelframe.place(relx=0.423, rely=0.117, relheight=0.845, relwidth=0.527)
        self.treeview_labelframe.configure(relief='groove')
        self.treeview_labelframe.configure(foreground="#000000")
        self.treeview_labelframe.configure(text='''TreeView''')
        self.treeview_labelframe.configure(background="#d9d9d9")

        self.treeview = ttk.Treeview(self.treeview_labelframe)
        self.treeview.place(relx=0.04, rely=0.046, height=391, width=435, bordermode='ignore')
        self.treeview['columns'] = ('Block Name', 'Father Name', 'Children')

        self.treeview.column('#0', width=120, minwidth=25)
        self.treeview.column('Block Name', anchor=CENTER, width=120)
        self.treeview.column('Father Name', anchor=CENTER, width=120)
        self.treeview.column('Children', anchor=CENTER, width=75)

        self.treeview.heading('#0', text='Type', anchor=CENTER)
        self.treeview.heading('Block Name', text='Block Name', anchor=CENTER)
        self.treeview.heading('Father Name', text='Father Name', anchor=CENTER)
        self.treeview.heading('Children', text='Children', anchor=CENTER)

        self.counter = 0
        self.on_tv = []
        self.show_in_tv("gen_" + self.user.user_name)

        self.homepage.tkraise()

    def show_in_tv(self):  # use networker answers
        block = self.next_networker.answer
        if not dad_name == 0:
            for block_shown in self.on_tv[0]:  # Block name shown
                if block.block_name == block_shown:
                    return
        to_show = [block.block_name, dad_name, len(block.children)]  # Supposed to be dad children
        if isinstance(block, BlockFolder):
            self.treeview.insert(parent='', index='end', iid=self.counter, text='Folder', values=to_show)
        elif isinstance(block, BlockFile):
            self.treeview.insert(parent='', index='end', iid=self.counter, text='File', values=to_show)
        counter = 0
        if not dad_name == 0:
            for block_shown in self.on_tv[0]:  # Block name shown
                if dad_name == block_shown:  # If true needs update
                    self.on_tv[counter][-1] = self.on_tv[counter][-1] + 1
                    self.update_record(counter, values=self.on_tv[counter])
                    print("Treeview record updated")
                counter += 1
        self.on_tv.append(to_show)
        self.counter += 1

    def make_folder_clicked(self):
        new_name = simpledialog.askstring(title="New Folder Name", prompt="Enter the new folder's name:")
        dad_name = simpledialog.askstring(title="Father Name", prompt="Enter the father's name:")
        dad_block = self.user.load_block(dad_name)
        new_block = self.user.create_folder(dad_block, new_name)
        self.show_in_tv(new_block, dad_name)

    def update_record(self, id, values):
        self.treeview.item(id, text="Folder", values=values)

    def make_folder_clicked(self):
        new_name = simpledialog.askstring(title="New Folder Name", prompt="Enter the new folder's name:")
        dad_name = simpledialog.askstring(title="Father Name", prompt="Enter the father's name:")
        self.begin_create_load_block(dad_name, new_name, address)
        # dad_block = self.user.load_block(dad_name)
        # new_block = self.user.create_folder(dad_block, new_name)
        self.root.after(2400, lambda: self.show_in_tv())  # blocks will be in networker and next_networker??

    def begin_create_load_block(self, block_name, new_name, address=0):
        self.user.load_block(block_name, self.networker, address)  # Will give networker work
        self.root.after(1200, self.end_load_block_and_begin_create_folder)  #
        pass

    def end_load_block_and_begin_create_folder(self):
        if self.networker.answer is not None:
             self.user.create_folder(self.networker.answer, new_name, self.next_networker)

    def check_answer(self):

    def get_file_clicked(self):
        file_name = simpledialog.askstring(title="Block File name", prompt="Enter the block-file's name:")
        self.user.dump_block(file_name)

    def make_file_clicked(self):
        file_name = filedialog.askopenfilename()
        file = open(file_name, 'rb')
        pickled_file = pickle.load(file)
        file.close()
        dad_name = simpledialog.askstring(title="Father name", prompt="Enter the father's name:")
        dad_block = self.user.load_block(dad_name)
        file_name = file_name.split("/")[-1]
        new_block = self.user.create_file(dad_block, file_name, pickled_file)
        self.show_in_tv(new_block, dad_name)

    def traverse_button_clicked(self):
        user_inp = simpledialog.askstring(title="Block to Traverse", prompt="Enter what block to traverse:")
        self.user.traverse(user_inp)

    def load_button_clicked(self):
        user_inp = simpledialog.askstring(title="Block to Load", prompt="Enter what block to load:")
        block = self.user.load_block(user_inp)
        print(block)

    def sign_up_clicked(self):
        name = self.username_entry_signup.get()
        pos = self.user.create_user(name)
        if pos:
            self.make_homepage() ##
            self.user.make_userserver() ##
        else:
            pass  # Show on gui wrong username

    def login_clicked(self):  # Needs to get file for block and stuff
        name = self.username_entry.get()
        pos = self.user.log_in(name)
        if pos:
            self.make_homepage()
            self.user.make_userserver()
        else:  # Shown on gui something aint right
            pass

    def exit_program(self):
        if self.user.exit_program():
            self.root.destroy()
            return
        print("An error occurred while exiting")


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
