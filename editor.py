from tkinter import *
from PIL import Image, ImageTk

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

root= Tk()
width= 800
height= 600
# root.geometry(f"{width}x{height}")
root.iconbitmap("images/logo.ico")
root.title("Imagify - Jam-burger")
# root.resizable(False, False)

img_w = width*.6
img_window= LabelFrame(root, border= 4, padx=10, pady= 10, width=img_w - 20, height=img_w - 20)
img_window.grid(row=0, column=0, padx= 10, pady=10, ipadx=5, ipady=5, rowspan=3)
img_window.grid_propagate(0)

frame1= LabelFrame(root, border=3, padx= 10, pady= 10, width= width - img_w - 20, height= 120)
frame1.grid(row=0, column=1, padx= 10, pady=10, ipadx=5, ipady=5)
frame1.grid_propagate(0)

img1= Image.open("images/Imagify-logo.jpeg")
img1= ImageTk.PhotoImage(img1.resize((100, 100)))
logo= Label(frame1, image= img1)
logo.grid(row= 0, column=0, rowspan=2)

Label(frame1, text="Imagify", font=('Comic Sans MS bold', 20)).grid(row= 0, column=1, padx= 5, pady=5, sticky=W)
Label(frame1, text="By Jam-Burger", font=('Comic Sans MS', 10)).grid(row= 1, column=1, padx= 5, pady=5)

root.mainloop()