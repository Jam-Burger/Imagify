from tkinter import *
from PIL import *

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

root= Tk()
width= 800
height= 600
root.geometry(f"{width}x{height}")
root.iconbitmap("images/logo.ico")
root.title("Imagify - Jam-burger")
# root.resizable(False, False)

img_w = width*.6
img_window= LabelFrame(root, border= 4, padx=10, pady= 10, width=img_w - 20, height=img_w - 20)
img_window.grid(row=0, column=0, padx= 10, pady=10, rowspan=3)

frame1= LabelFrame(root, border=3, padx= 10, pady= 10, width= width - img_w - 20, height= img_w / 3 - 20)
frame1.grid(row=0, column=1, padx= 10, pady=10)
frame1.grid_propagate(0)

logo= Label(frame1, text= "This is\na logo", image=None)
logo.grid(row= 0, column=0, padx= 5, pady=5)


name= Label(frame1, text="Jam-Burger")
name.grid(row= 0, column=1, padx= 5, pady=5)

root.mainloop()