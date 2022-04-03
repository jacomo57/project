import tkinter as tk
from os import listdir
from os.path import isdir
from tkinter import messagebox

from PIL import ImageTk, Image

# globals
h = []
value = 0
m = 0
b, a, f, q, type, r= "", "", "", "", "", ""
g = 1
l = 1
photo = ""
new_name = 0
row = ""
image = ""
text = ""
# modifying button for files and folders
class modified_button(tk.Button):
    def __init__(self, root, type=None, *args, **kw):
        global h, value, m, b
        tk.Button.__init__(self, root, *args, **kw)
        self.type = type
        self.root = root  # root of the given button widget
        if value == 0:
            for i in range(len(exp.lst)):
                h.append(tk.Button(bg="#ffffff"))  # creating a list of buttons when the first button is created
        h.insert(value, self)  # updating the list with newly created buttons
        value += 1  # increasing the value so that list is not created again
        self.file_path = ""
        self.bind("<Enter>", lambda event, a="enter": self.changebg(a,
                                                                    event))  # changing the color of the button when it is under cursor
        self.bind("<Leave>", lambda event, a="leave": self.changebg(a,
                                                                    event))  # changing the color of the button when the cursor leaves it
        if type == "folder" or type == "file":  # if the button is of a file or a folder
            self.bind("<Button 1>",
                      lambda event, a="click": self.changebg(a, event))  # binding the click and rightclick
            self.bind("<Button-3>", lambda event, a="right-click": self.changebg(a, event))

    def changebg(self, a, event):
        global g, l, q,type
        if self["bg"] != "#80bfff" and a == "leave" and l != 0:  # if the bg of the color is not dark blue change the bg to white
            self.config(bg="#ffffff")
        if self["bg"] != "#80bfff" and a == "enter" and g != 0 and l != 0:  # same as above
            self.config(bg="#cce6ff")
        if self["bg"] != "#80bfff" and a == "click" and l != 0:  # if the user has clicked then changing the bg
            for ech in h:
                if type == "renaming":
                    self.rename()
                if ech["bg"] == "#80bfff":  # checking if any other button has dark blue bg
                    ech.config(bg="#ffffff")  # if it has then change it to light blue
            self.config(bg="#80bfff")  # lastly changing the bg to dark blue
        if self.type != "other":
            if self["bg"] == "#80bfff" and a == "right-click" and l != 0:
                # checking if the button is clicked before or not
                # creating menu for rightclick
                self.m = tk.Menu(self.root, tearoff=0)
                self.m.add_command(label="Cut  ", command=lambda a=self, b="cut": self.copy_paste(b, a))
                self.m.add_command(label="Copy ", command=lambda a=self, b="copy": self.copy_paste(b, a))
                if self.type == "folder":  # if the button is of a folder then only add the option to paste in it
                    self.m.add_command(label="Paste ", command=lambda a=self, b="paste": self.copy_paste(b, a))
                else:
                    pass
                self.m.add_separator()
                self.m.add_command(label="Delete")
                self.m.add_command(label="Rename", command=lambda a=self, b="rename": self.copy_paste(b, a))
                try:
                    self.m.tk_popup(event.x_root, event.y_root)
                finally:
                    self.m.grab_release()

    def copy_paste(self, command, file):
        global b, a, g, l, q,type,r,photo,row,image,text,new_name
        if self.type != "other":
            if command == "cut":  # if the user has selected to cut the file
                self.u = "{0}/{1}".format(exp.z, file["text"])
                a = "cut"
                b = self.u

            if command == "copy":  # if the user has selected to copy the file
                self.u = "{0}/{1}".format(exp.z, file["text"])
                a = "copy"
                b = self.u
            if command == "paste":  # if the user has selected to paste the file
                try:
                    file[0].isalpha()
                    if file == exp.z:
                        self.file_path = file
                    else:
                        self.file_path = "{0}/{1}".format(exp.z, file)  # creating the path to paste
                except:
                    self.file_path = "{0}/{1}".format(exp.z, file["text"])
                if a == "copy":
                    # sh.copy(b,self.file_path)
                    pass
                if a == "cut":
                    # sh.move(b,self.file_path)
                    pass
            if command == "rename":  # renaming file
                row = self.grid_info()["row"]
                image = self["image"]
                text = self["text"]
                type = "renaming"
                self.grid_forget()
                r = tk.Frame(master=self.root, width=1750, height=10, bg="#ffffff")
                photo = tk.Label(master=r, image=exp.p1)
                photo.grid(row=0, column=0)
                new_name = tk.Entry(master=r, width=50)
                new_name.grid(row=0, column=1)
                r.grid(column=0, row=row, sticky="w")
                new_name.bind("<Return>", lambda event: self.rename())
            if command == "delete":
                # remove(b)
                pass

    def rename(self):
        # exact renaming method is not here
        global r,new_name,text,row,type
        print(r,2,new_name,3,text,4,row)
        r.grid_forget()
        button = modified_button(self.root, type=type, image=image, bg="#ffffff", text=new_name.get(), width=750,
                                 height=13,
                                 compound="left",
                                 anchor="w",
                                 borderwidth=0)
        button.bind("<Double 1>", lambda event, a=text: exp.create_dirlst(a))
        if button["text"] == "":
            button["text"] = text
        button.grid(column=0, row=row)
        type = ""


class explorer(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        global f
        tk.Frame.__init__(self, *args, **kwargs)
        # creating the basics and handlers
        self.window = root
        self.lst = []
        self.starting_path = "/Users/idan"
        self.z = " "
        self.last_search = ""
        self.val = [0, 0, 0, 1, 0, 1, 0, 0, 1, 0]
        self.p1 = ImageTk.PhotoImage(Image.open("Folder.png").resize((15, 15), Image.ANTIALIAS))
        self.p2 = ImageTk.PhotoImage(Image.open("file.png").resize((15, 15), Image.ANTIALIAS))
        self.p3 = ImageTk.PhotoImage(Image.open("Untitled-1.png").resize((20, 20), Image.ANTIALIAS))
        self.p4 = ImageTk.PhotoImage(Image.open("Untitled-2.png").resize((20, 20), Image.ANTIALIAS))
        self.no_of_files = 0
        self.no_of_folders = 0
        self.last_opened_folder = ""

    def create_basics(self, a):
        if self.val[0] == 0:  # if this is first time then pass
            pass
        else:  # if this not the first time then delete all the old widgets
            self.left.pack_forget()
            self.up.pack_forget()
            self.parent_frame.pack_forget()
            self.down.pack_forget()
        # after deleting the old widgets creating new one
        self.left = tk.Frame(self.window, bg="#ffffff", width=10)
        self.left.pack(side="left", fill="y")
        self.up = tk.Frame(master=self.window, height=10, width=10)
        self.navigation_buttons = tk.Frame(self.up)
        self.back_button = modified_button(self.navigation_buttons, type="other", image=self.p3, borderwidth=0,
                                           bg="#ffffff")
        self.forward_button = modified_button(self.navigation_buttons, type="other", image=self.p4, borderwidth=0,
                                              bg="#ffffff")
        self.back_button.grid(row=0, column=0)
        self.back_button.bind("<Button-1>", lambda event, command="back": self.navigation(event, command))
        self.forward_button.grid(row=0, column=1)
        self.forward_button.bind("<Button-1>", lambda event, command="next": self.navigation(event, command))
        self.navigation_buttons.pack(side="left", fill="y")
        self.search = tk.Entry(master=self.up)
        if self.last_search == "":
            self.search.insert(tk.END, "Search")
        else:
            self.search.insert(tk.END, self.last_search)
        self.search.bind("<Button-1>", lambda event, a="click": explorer.modify_search(self, a, event))
        self.search.bind("<Leave>", lambda event, a="leave": explorer.modify_search(self, a, event))
        self.search.bind("<Return>", lambda event, a="enter": explorer.modify_search(self, a, event))
        self.search.bind("<BackSpace>", lambda event, a="Backspace": explorer.modify_search(self, a, event))
        self.search.pack(side="right", fill="y")
        self.path = tk.Frame(self.up, bg="#ffffff")
        self.path.pack(fill="both", expand=1)
        self.up.pack(fill="x")
        self.parent_frame = tk.Frame(self.window)
        self.canvas = tk.Canvas(self.parent_frame, bg="#ffffff")
        self.canvas.pack(side="left", fill="both", expand=1)
        self.scrollbar = tk.Scrollbar(self.parent_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame)
        self.parent_frame.pack(fill="both", expand=1)
        self.down = tk.Frame(self.window, width=100, borderwidth=1, bg="#444444")
        self.down.pack(anchor="w")
        self.canvas.bind("<Button-3>", lambda event: self.mod_canvas(event))
        if a == "R":
            self.val[5] = 0
            explorer.create_folder(self)

    def modify_search(self, a, event):  # modifying the search widget
        if self.search.get() == "" and a == "leave" and self.val[3] != 0 and self.val[
            6] == 0:  # if the method is called for first time or after changing the directory
            self.search.insert(tk.END, "Search")

        if a == "click" and self.search.get() == "Search" and self.val[
            3] != 0:  # if the user has clicked the widget to type
            self.search.delete(0, tk.END)
            self.val[6] = 1
        if a == "enter" and self.search.get() != "" and self.search.get() != "Search":  # if the user has pressed enter to search
            m = self.lst  # first saving the list
            self.lst = []  # emptying the list
            for x in m:
                if self.search.get().lower() == x[0:len(
                        self.search.get())].lower():  # sortin all the matches of the search

                    self.lst.append(x)  # updating self.lst
                    self.val[4] += 1  # updating self.val[4] to identify is any file matches or not
            print(self.val[4])
            if self.val[4] == 0:  # if no file matches raise error
                messagebox.showwarning('Error', "Can't find the specified file.")
            else:  # if the files are found creating the new sest of buttons with modified self.lst
                self.last_search = self.search.get()
                self.no_of_files = 0
                self.no_of_folders = 0
                self.create_basics("")
                self.create_folder()
                self.val[4] = 0

        if a == "Backspace":
            if self.search.get() == "Search":
                self.search.delete(0, tk.END)
                self.val[3] = 0
            else:
                pass

    def navigation(self, event, command):
        global f
        if command == "back":  # if the user has pressed back
            try:
                self.last_opened_folder = f  # updating the last_opened_folder for later use
                f = self.z[:len(f) - f[::-1].index("/") - 1]  # obtaining the upper directory
            except:
                pass
            # doing basic things as before to create new
            self.lst = list(f for f in listdir(f) if f[0].isalpha())
            self.starting_path = f
            self.no_of_files = 0
            self.no_of_folders = 0
            self.create_basics("")
            self.create_folder()
        if command == "next":
            try:  # if the user has clicked next button
                self.lst = list(f for f in listdir(self.last_opened_folder) if
                                f[0].isalpha())  # using the last_opened_folder from before
            except:
                pass
            f = self.last_opened_folder
            self.starting_path = self.last_opened_folder
            self.no_of_files = 0
            self.no_of_folders = 0
            self.create_basics("")
            self.create_folder()

    def show_no_of_files(self):
        # creating widgets to show no. of files and folders
        self.files = tk.Label(master=self.down,
                              text=f"No. of files: {self.no_of_files}, No. of folders: {self.no_of_folders}",
                              borderwidth=1)
        self.files.pack(fill="x", expand=1)

    def create_dirlst(self, a):
        global f
        self.lst = []
        # here self.z is the clicked icon or the file/folder user wants to open
        if self.val[0] == 0:  # if this method is called first time then initialise self.z
            self.z = self.starting_path
            self.val[2] += 1
        if self.val[0] != 0 and self.val[
            2] == 1:  # if this method is not called for the first time then modifying self.z
            self.z = "{0}/{1}".format(self.starting_path, a)
        if isdir(self.z) == False and self.val[0] != 0:  # if self.z is not a folder then raise error
            #exact opening file method is not here
            messagebox.showwarning('Open Error', "Can't open this file.")
            self.val[1] += 1
        if self.val[0] != 0 and isdir(self.z):  # if the clicked icon is folder
            self.starting_path = "{0}/{1}".format(self.starting_path, a)
            self.lst = list(f for f in listdir(self.starting_path) if f[0].isalpha())
            self.no_of_files = 0
            self.no_of_folders = 0
            self.create_basics("")
            self.create_folder()
            self.val[5] = 1

            if self.val[1] != 0:  # setting val[1] to zero so that the show_no_of_files method can be called later
                self.val[1] = 0
        f = self.z
        if self.val[0] == 0:  # creating the list if the method is called for first time
            self.lst = list(f for f in listdir(self.starting_path) if f[0].isalpha() and f[0] != "$")

    def create_folder(self):
        for ech in self.lst:  # iterating through the list of dir and files
            if isdir("{0}/{1}".format(self.starting_path, ech)):  # if ech is a folder
                button = modified_button(self.frame, type="folder", image=self.p1, bg="#ffffff", text=ech, width=750,
                                         height=13,
                                         compound="left",
                                         anchor="w",
                                         borderwidth=0)
                button.bind("<Double 1>", lambda event, a=ech: self.create_dirlst(a))
                button.grid(column=0, row=self.lst.index(ech))
                if self.val[5] != 0:
                    self.no_of_folders += 1  # incrementing self.no_of_folders

            else:
                button = modified_button(self.frame, type="file", image=self.p2, bg="#ffffff", text=ech, width=750,
                                         height=13,
                                         compound="left",
                                         anchor="w",
                                         borderwidth=0)
                button.bind("<Double 1>", lambda event, a=ech: self.create_dirlst(a))
                button.grid(column=0, row=self.lst.index(ech))
                if self.val[5] != 0:
                    self.no_of_files += 1
        self.val[0] += 1
        if self.val[8] != 0:
            q = self.starting_path.split("/")
            for g in q:
                self.path_buttons = modified_button(self.path, type="other", text=g, bg="#ffffff", borderwidth=0)
                self.path_buttons.grid(row=0, column=q.index(g), padx=4)
                self.path_buttons.bind("<Button-1>", lambda event, r=g: self.updating_path(r))
        if self.val[1] == 0:
            self.show_no_of_files()

    def updating_path(self, k):
        if self.starting_path == k:
            pass
        else:
            self.starting_path = self.starting_path[:self.starting_path.index(k) + len(k)]
        self.lst = list(f for f in listdir(self.starting_path) if f[0].isalpha())
        self.create_basics("")
        self.create_folder()

    def mod_canvas(self,
                   event):  # modifying the canvas at the right side to paste in the current directory and also for refreshing
        self.menu = tk.Menu(self.canvas, tearoff=0)
        self.menu.add_command(label="Refresh            ", command=lambda a="R": explorer.create_basics(self, a))
        self.menu.add_command(label="Paste                ",
                              command=lambda a="paste", b=self.z: modified_button.copy_paste(self, a, b))
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()


if __name__ == "__main__":  # creating basic window
    window = tk.Tk()
    window.geometry("900x600")
    window.title("Door Explorer 1.0")
    #window.iconbitmap("icon1.ico")
    exp = explorer(window)
    exp.create_basics("")
    exp.create_dirlst(exp.starting_path)
    exp.create_folder()
    window.mainloop()