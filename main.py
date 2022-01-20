from tkinter import *

root= Tk()
width= 800
height= 600
root.geometry(f"{width}x{height}")

w = 500
img_window= LabelFrame(root, border= 1, text= "Image", padx=10, pady= 10, width=w, height=w)
img_window.grid(row=0, column=0, padx= 10, pady=10, rowspan=3)

frame1= LabelFrame(root, border=1, padx= 10, pady= 10, width= width-w-20 , height= height/3)
frame1.grid(row=0, column=1, padx= 5, pady=10)

logo= Label(frame1, text="This is\na logo", width=(int)frame1.winfo_width)
logo.grid(row= 0, column=0)
root.mainloop()