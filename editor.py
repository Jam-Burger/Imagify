from tkinter import *
from PIL import Image, ImageTk

import functions
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

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
functions.set_img_window(img_window, iw_w, iw_h)
functions.change_img(Image.open("images/default.jpg"))

frame1 = LabelFrame(root, border=3, borderwidth=5, padx=10, pady=10, width=c1_width, height=125, cursor="heart", relief=RIDGE)
frame1.grid(row=0, column=2, padx=10, pady=(10, 0), ipadx=5, ipady=5, sticky=N)

frame2_color= "#041a3d"
frame2_font_color= "#fff3b8"
frame2= LabelFrame(root, border=3, borderwidth=5, padx=10, bg=frame2_color, pady=10, width=c1_width, height=height/2 - 50, relief=RIDGE)
frame2.grid(row=2, column=2, padx=10, pady=(0, 10), ipadx=5, ipady=5, sticky=N)

# importing images
img= None
logo_img = Image.open("images/Imagify-logo.jpeg")
logo_img = ImageTk.PhotoImage(logo_img.resize((100, 100)))

rotate_a_img = Image.open("images/rotate_a.png")
rotate_a_img = ImageTk.PhotoImage(rotate_a_img.resize((40, 40)))
rotate_c_img = Image.open("images/rotate_c.png")
rotate_c_img = ImageTk.PhotoImage(rotate_c_img.resize((40, 40)))

flip_h_img = Image.open("images/flip_h.png")
flip_h_img = ImageTk.PhotoImage(flip_h_img.resize((40, 40)))
flip_v_img = Image.open("images/flip_v.png")
flip_v_img = ImageTk.PhotoImage(flip_v_img.resize((40, 40)))

invert_img = Image.open("images/invert.png")
invert_img = ImageTk.PhotoImage(invert_img.resize((40, 40)))

undo_img = Image.open("images/undo.png")
undo_img = ImageTk.PhotoImage(undo_img.resize((40, 40)))

redo_img = Image.open("images/redo.png")
redo_img = ImageTk.PhotoImage(redo_img.resize((40, 40)))

# adding stuff in frames

Label(frame1, image=logo_img).grid(row=1, column=0, rowspan=2)
Label(frame1, text="Imagify", font=('Comic Sans MS bold', 20)).grid(row=1, column=1, padx=5, pady=5, sticky=W)
Label(frame1, text="By Jam-Burger", font=('Comic Sans MS', 10)).grid(row=2, column=1, padx=5, pady=5)

# adding buttons
frame2.columnconfigure(0, weight=1)
frame2.columnconfigure(1, weight=1)
frame2.columnconfigure(2, weight=1)
frame2.columnconfigure(3, weight=1)


btn_type1=[]
btn_type2=[]
lines=[]

def line(row):
   l= Label(frame2, text= "-"*36)
   l.grid(row=row, column=0, columnspan=4)
   lines.append(l)

select_image_btn= Button(frame2, text="Select Image", command= functions.select_img)
select_image_btn.grid(row=0, column=0, columnspan=2)
btn_type1.append(select_image_btn)

save_image_btn= Button(frame2, text="Save Image", command= functions.save_img)
save_image_btn.grid(row=0, column=2, columnspan=2)
btn_type1.append(save_image_btn)

line(1)

rotate_a_btn= Button(frame2, image= rotate_a_img, command= functions.rotate_a_img)
rotate_a_btn.grid(row=2, column=0)
btn_type2.append(rotate_a_btn)

rotate_c_btn= Button(frame2, image= rotate_c_img, command= functions.rotate_c_img)
rotate_c_btn.grid(row=2, column=1)
btn_type2.append(rotate_c_btn)

Label(frame2, text="Rotate").grid(row=3, column=0, columnspan=2)

flip_h_btn= Button(frame2, image= flip_h_img, command= functions.flip_h_img)
flip_h_btn.grid(row=2, column=2)
btn_type2.append(flip_h_btn)

flip_v_btn= Button(frame2, image= flip_v_img, command= functions.flip_v_img)
flip_v_btn.grid(row=2, column=3)
btn_type2.append(flip_v_btn)

Label(frame2, text="Flip").grid(row=3, column=2, columnspan=2)

invert_btn= Button(frame2, image= invert_img, command= functions.invert_img)
invert_btn.grid(row=4, column=3, pady=(20, 0))
Label(frame2, text="Invert\nColor").grid(row=5, column=3)
btn_type2.append(invert_btn)

undo_btn= Button(frame2, image= undo_img, command= functions.undo)
undo_btn.grid(row=4, column=1, pady=(20, 0))
Label(frame2, text="Undo").grid(row=5, column=1)
btn_type2.append(undo_btn)

redo_btn= Button(frame2, image= redo_img, command= functions.redo)
redo_btn.grid(row=4, column=2, pady=(20, 0))
Label(frame2, text="Redo").grid(row=5, column=2)
btn_type2.append(redo_btn)

line(6)

for w in btn_type2:
    w.configure(width= 42, height= 42, anchor='nw')
for w in btn_type1 + btn_type2:
    w.configure(cursor="circle")
for w in frame2.winfo_children():
    w.configure(font=('Consolas', 11), border= 0, background= frame2_color, fg=frame2_font_color)
for w in btn_type1:
    w.configure(font=('Consolas', 13), width= 13)
for w in lines:
    w.configure(font=('Consolas'))

# setting every frame non-resizable

for w in root.winfo_children():
    w.grid_propagate(0)

root.mainloop()
