from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import os
import re
import time

win = Tk()
win.title('exeMaker')
win.resizable(0,0)

stat = StringVar()

def filePath():
    fp = filedialog.askopenfilename()
    path.delete(1.0,"end")
    path.insert(1.0, fp)

def generate():
    filePath=path.get("1.0","end-1c")
    exename=outputName.get("1.0","end-1c")
    outType = ot.get()
    stat.set('checking details entered..')
    if len(filePath) == 0 or len(exename) == 0:
        stat.set('Please enter the above details to continue the Build')
    else:
        stat.set('Downloading modules..')
        win.update()
        os.system('pip install pyinstaller')
        stat.set('Bulding...')
        win.update()
        try:
            directory = re.findall(r"^[A-Z]:/.*/", filePath)[0]
            filename = re.sub(r"^[A-Z]:/.*/", "", filePath)
            os.chdir(directory)
            if outType == 'Hidden':
                var = os.system('pyinstaller '+ filename +' -n'+ exename+' --onefile --noconsole')                
            else:
                var = os.system('pyinstaller '+ filename +' -n'+ exename+' --onefile')
            stat.set('Done!!')
        except Exception as e:
            print(e)
            stat.set('Build Fail!!')
            makeBtn.bg = "Red"
    

Heading = Label(win, text='ExeMaker', fg='Black', font=8).grid(row=0,column=1)

la1= Label(win, text='Path:', fg='Blue', font=8)
la1.grid(row=2,column=0,pady=5)
path = Text(win, height=1, width=40)
path.grid(row=2,column=1,pady=5, padx=10)
selectFileBtn = Button(win, text= "Select File", command=filePath).grid(row=2,column=2, padx=5)

ol = Label(win, text='EXE Name:', fg='Blue', font=8)
ol.grid(row=3,column=0,pady=5)
outputName = Text(win, height=1, width=40)
outputName.grid(row=3,column=1,pady=5, padx=10)

otl = Label(win, text='Console:', fg='Blue', font=8).grid(row=4, column=0)
ot = Combobox(win, values=['Visible', 'Hidden'])
ot.grid(row=4,column=1)

status= Label(win, textvariable=stat, fg='Green', font=8)
status.grid(row=5,column=1,pady=5)

makeBtn = Button(win, text= "Generate EXE", bg='lightgreen',font=7, command= generate).grid(row=6,column=1, padx=5, pady=2)

win.mainloop()
