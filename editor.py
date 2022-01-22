from tkinter import *
from PIL import Image, ImageTk

import functions
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

#creating screen

root = Tk()
root.iconbitmap("images/logo.ico")
root.title("Imagify - Jam-burger")

width= root.winfo_screenwidth()
height= root.winfo_screenheight()
bg_color= "#90A8F4"

root.geometry(f"{width}x{height}")
root.configure(bg=bg_color, bd= 10, highlightcolor="#98F", highlightthickness=5)

iw_h = height - 125
iw_w = iw_h*3/2
c1_width= width - iw_w - 80


# creating basic layout

img_window = LabelFrame(root, border=1, padx=10, pady=10, bg="#001", width=iw_w, height=iw_h)
img_window.grid(row=0, column=0, padx=10, pady=10, rowspan=3)

frame1 = LabelFrame(root, border=3, borderwidth=5, padx=10, pady=10, width=c1_width, height=125, cursor="heart", relief=RIDGE)
frame1.grid(row=0, column=2, padx=10, pady=(10, 0), ipadx=5, ipady=5, sticky=N)

frame2_color= "#041a3d"
frame2= LabelFrame(root, border=3, borderwidth=5, padx=10, bg=frame2_color, pady=10, width=c1_width, height=height/2 - 50, relief=RIDGE)
frame2.grid(row=2, column=2, padx=10, pady=(0, 10), ipadx=5, ipady=5, sticky=N)

# importing images
img= None
logo_img = Image.open("images/Imagify-logo.jpeg")
logo_img = ImageTk.PhotoImage(logo_img.resize((100, 100)))

rotate_img = Image.open("images/rotate.png")
rotate_img = ImageTk.PhotoImage(rotate_img.resize((40, 40)))

undo_img = Image.open("images/undo.png")
undo_img = ImageTk.PhotoImage(undo_img.resize((40, 40)))

redo_img = Image.open("images/redo.png")
redo_img = ImageTk.PhotoImage(redo_img.resize((40, 40)))

flip_img = Image.open("images/flip.png")
flip_img = ImageTk.PhotoImage(flip_img.resize((40, 40)))

# adding stuff in frames

Label(frame1, image=logo_img).grid(row=1, column=0, rowspan=2)
Label(frame1, text="Imagify", font=('Comic Sans MS bold', 20)).grid(row=1, column=1, padx=5, pady=5, sticky=W)
Label(frame1, text="By Jam-Burger", font=('Comic Sans MS', 10)).grid(row=2, column=1, padx=5, pady=5)

# adding buttons
frame2.columnconfigure(0, weight=1)
frame2.columnconfigure(1, weight=1)
frame2.columnconfigure(2, weight=1)
frame2.columnconfigure(3, weight=1)


select_image_btn= Button(frame2, cursor="circle", text="Select Image", width=13, command= lambda : functions.select_img(img_window))
select_image_btn.grid(row=0, column=0, columnspan=2)

save_image_btn= Button(frame2, cursor="circle", text="Save Image", width=13, command= lambda : functions.save_img(img))
save_image_btn.grid(row=0, column=2, columnspan=2)

rotate_btn= Button(frame2, image= rotate_img, cursor="circle", width= 42, height= 42, anchor='nw', command= lambda : functions.rotate_img(img))
rotate_btn.grid(row=2, column=0)
Label(frame2, text="Rotate").grid(row=3, column=0)

undo_btn= Button(frame2, image= undo_img, cursor="circle", width= 42, height= 42, anchor='nw')
undo_btn.grid(row=2, column=1)
Label(frame2, text="Undo").grid(row=3, column=1)

redo_btn= Button(frame2, image= redo_img, cursor="circle", width= 42, height= 42, anchor='nw')
redo_btn.grid(row=2, column=2)
Label(frame2, text="Redo").grid(row=3, column=2)

flip_btn= Button(frame2, image= flip_img, cursor="circle", width= 42, height= 42, anchor='nw')
flip_btn.grid(row=2, column=3)
Label(frame2, text="Flip").grid(row=3, column=3)

for w in frame2.winfo_children():
    w.configure(font=('Consolas'), border= 0, relief= RIDGE)
    w.configure(background= frame2_color, fg="#fff3b8")

Label(frame2, text= "-"*36, font=('Consolas'), background= frame2_color, fg="#fff3b8").grid(row=1, column=0, columnspan=4)
Label(frame2, text= "-"*36, font=('Consolas'), background= frame2_color, fg="#fff3b8").grid(row=4, column=0, columnspan=4)

# setting every frame non-resizable

for w in root.winfo_children():
    w.grid_propagate(0)

root.mainloop()
