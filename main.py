from tkinter import *

root= Tk()
root.geometry("300x300")
img_window= LabelFrame(root, border= 1, text= "Image", padx=10, pady= 10)
img_window.pack()
l1= Label(img_window, text="This is in a frame")
l1.pack()
root.mainloop()