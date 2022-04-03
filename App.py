from tkinter import *
from tkinter.ttk import *


def main():
    app = App()
    app.run_GUI()
    #app = App('/Users/idan/Desktop/mac_folder_icon.png', '/Users/idan/Desktop/mac_file_default.png')
    #app.setup_buttons(10, 10)


class App:
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, bg="white", height=250, width=300)

    def organize_canvas(self):
        scroll_x = Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        scroll_x.grid(row=1, column=0, sticky="ew")

        scroll_y = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def run_GUI(self):
        self.organize_canvas()
        mainloop()


    #def __init__(self, folder_image, file_image, ):
    #    self.root = Tk(className='File Explorer')
    #    self.root.geometry("500x200")
    #    self.title = Label(self.root, text='File Explorer', font=('Verdana', 15)).pack(side=TOP, pady=10)
    #    self.folder_image = folder_image
    #    self.file_image = file_image
    #    self.folder_button = 0  # Will be setup in setup_buttons.
    #    self.file_button = 0

    #def setup_buttons(self, x, y):
    #    self.folder_image = PhotoImage(file=self.folder_image)  # Creating photoimage object to use image
    #    self.file_image = PhotoImage(file=self.file_image)
    #    self.folder_image = self.folder_image.subsample(x, y)  # Resizing buttons
    #    self.file_image = self.file_image.subsample(x, y)
    #    self.folder_button = Button(self.root, text='Folder', image=self.folder_image, compound=TOP).pack(side=TOP)
    #    self.file_button = Button(self.root, text='File', image=self.file_image, compound=TOP).pack(side=TOP)
    #    mainloop()


if __name__ == '__main__':
    main()
