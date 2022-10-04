import tkinter
from tkinter import *
import tkinter.messagebox
import customtkinter
from tkinter import filedialog
import os
import re
import time
from threading import *
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.files = []

        self.title("Exe Maker")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="ExeMaker",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Add Files",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.add_file_button_pressed)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Console Mode")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Hidden", "Visible"],
                                                        )
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=1)
        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=4, rowspan=4, pady=20, padx=20, sticky="nsew")

        self.selected_file = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="Selected Files",
                                                    text_font=("Roboto Medium", -16))
        self.selected_file.grid(row=0, column=0, pady=10, padx=10)


        self.canvas = customtkinter.CTkCanvas(master=self.frame_info,width=App.WIDTH-300, height=App.HEIGHT-300,bd=0, highlightthickness=0,bg="#222222")
        self.canvas.grid(row=1, column=0, columnspan=4, rowspan=1, sticky="nsew",padx=10)
        self.file_holder = customtkinter.CTkFrame(master=self.canvas,width=600,height=1000,corner_radius=0)
        self.file_holder.grid(row=1, column=0, columnspan=4, rowspan=4, pady=20, padx=20, sticky="nsew")
        self.canvas.create_window((0,0),window=self.file_holder,anchor="nw")

        

        self.scrollbar = customtkinter.CTkScrollbar(master=self.frame_right, command=self.canvas.yview,width=20,height=App.HEIGHT-300)
        self.scrollbar.grid(row=2, column=3, rowspan=4, sticky="ns", pady=30, padx=20)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


        # ============ frame_bottom ============

        self.stat = StringVar()
        self.status = customtkinter.CTkLabel(master=self.frame_right,
                                                textvariable=self.stat,
                                                text_font=("Roboto Medium", -16))
        self.status.grid(row=7, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")
    


        self.entry = customtkinter.CTkEntry(master=self.frame_right, placeholder_text="Output file name (Seperate with comma)",width=App.WIDTH-300)

        self.entry.grid(row=8, column=0, rowspan=3, columnspan=2, pady=20, padx=20, sticky="w")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Make!",
                                                
                                                command=self.buildThread)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="e")




    def add_file_button_pressed(self):
        # select multiple python files

        files = filedialog.askopenfilenames(initialdir=os.getcwd(),
                                            title="Select Python Files",
                                            filetypes=(("Python Files", "*.py"), ("Python Files", "*.pyw")))
        if files:
            self.files = list(files)
            self.update_files()

            # update entry text
            self.entry.delete(0, END)
            self.entry.insert(0, ", ".join([os.path.basename(file).split(".")[0] for file in self.files]))


    def remove_file(self,file):
        print("Remove File Button pressed")
        self.files.remove(file)
        self.update_files()

    def update_files(self):
        print(self.files)
        for child in self.file_holder.winfo_children():
            child.destroy()
        for file in self.files:
            
            file_display = customtkinter.CTkFrame(master=self.file_holder)
            file_display.grid(column=0, row= self.files.index(file), pady=10, padx=10, sticky="nwew")
            file_name = customtkinter.CTkLabel(master=file_display, text=file)
            file_name.grid(row=0, column=0, pady=10, padx=10)
            file_remove = customtkinter.CTkButton(master=file_display, text="Remove", command=lambda: self.remove_file(file))
            file_remove.grid(row=0, column=2, pady=10, padx=10, sticky="e")

        
        file_display = customtkinter.CTkButton(master=self.file_holder, text="Add Other Files",width=self.WIDTH-320, command=self.add_file_button_pressed)
        file_display.grid(column=0, row= len(self.files), pady=10, padx=10, sticky="nwew")



    def on_closing(self, event=0):
        self.destroy()

    def generate(self):
        if len(self.files) <=0: 
            self.stat.set("No files selected")
            self.update()
            return
        self.stat.set('Downloading modules...')
        self.update()
        os.system('pip install pyinstaller')
        self.stat.set('Bulding...')
        self.update()
        exenames = self.entry.get().split(",")
        for file in self.files:
            
            filePath=file
            exename= exenames[self.files.index(file)]
            outType = self.optionmenu_1.get()
            self.stat.set('Bulding '+ file+' ...')
            self.update()
            if len(exename) == 0:
                self.stat.set('Please enter the output file name')
            else:
                try:

                    directory = re.findall(r"^[A-Z]:/.*/", filePath)[0]
                    filename = re.sub(r"^[A-Z]:/.*/", "", filePath)
                    os.chdir(directory)
                    if outType == 'Hidden':
                        var = os.system('pyinstaller '+ filename +' -n'+ exename+' --onefile --noconsole')                
                    else:
                        var = os.system('pyinstaller '+ filename +' -n'+ exename+' --onefile')
                    self.stat.set('Done!!')
                except Exception as e:
                    print(e)
                    self.stat.set('Build Fail!!')
    
    def buildThread(self):
        t1=Thread(target=self.generate)
        t1.start()

if __name__ == "__main__":
    app = App()
    app.mainloop()