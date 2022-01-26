from tkinter import *
from tkinter import messagebox
from PIL import Image

import functions as fns
from resources import Images
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# creating screen

root = Tk()
root.iconbitmap("images/logo.ico")
root.title("Imagify")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
bg_color = "#90A8F4"

root.geometry(f"{width}x{height}")
root.configure(bg=bg_color, bd=10, highlightcolor="#98F", highlightthickness=5)

menu_bar = Menu(root, activeborderwidth=5)
root.configure(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0, activeborderwidth=5)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=fns.open_img, accelerator="Ctrl+O")
root.bind('<Control-o>', fns.open_img)

file_menu.add_command(label="Save", command=fns.save_img, accelerator="Ctrl+S")
root.bind('<Control-s>', fns.save_img)
file_menu.add_separator()
file_menu.add_command(
    label="Exit", command=lambda: fns.quit(root), accelerator="Ctrl+Q")
root.bind('<Control-q>', func=lambda event: fns.quit(root))

edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=fns.undo, accelerator="Ctrl+Z")
root.bind('<Control-z>', fns.undo)
edit_menu.add_command(label="Redo", command=fns.redo, accelerator="Ctrl+Y")
root.bind('<Control-y>', fns.redo)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=fns.about)

i_f_w = height - 140
i_f_h = int(i_f_w*1.55)
c1_width = width - i_f_h - 60

# creating basic layout
img_window_frame = Frame(root, bg="#001", width=i_f_h, height=i_f_w)
img_window_frame.grid(row=0, column=0, rowspan=3)
img_window_frame.pack_propagate(0)

img_window = Canvas(img_window_frame, width=i_f_h,
                    height=i_f_w, bg='black', highlightthickness=0)
img_window.pack(expand=1)
fns.set_img_window(img_window, i_f_h, i_f_w)
fns.change_img(Image.open("images/default.jpg"))

imagify_frame = Frame(root, border=3, borderwidth=5, padx=10, pady=10,
                      width=c1_width, height=125, cursor="heart", relief=RIDGE)
imagify_frame.grid(row=0, column=1, padx=10, pady=(
    10, 0), ipadx=5, ipady=5, sticky=N)

color_1 = "#041a3d"
color_2 = "#fff3b8"

middle_frame_height = height/6
middle_frame = Frame(root, border=3, borderwidth=5, bg=color_1,
                     pady=10, width=c1_width, height=middle_frame_height, relief=RIDGE)
middle_frame.grid(row=1, column=1, padx=10, pady=(
    10, 0), ipadx=5, ipady=5, sticky=N)

main_frame = Frame(root, border=3, borderwidth=5, bg=color_1,
                   pady=20, width=c1_width, height=height - 340 - middle_frame_height, relief=RIDGE)
main_frame.grid(row=2, column=1, padx=10, pady=(5, 0))

# importing images
my_images = Images()

# adding stuff in frames

imagify_logo = Label(imagify_frame, image=my_images.logo)
imagify_logo.grid(row=0, column=0, rowspan=2)
imagify_logo.bind("<Button 1>", fns.about)

Label(imagify_frame, text="Imagify", font=('Comic Sans MS bold', 20)).grid(
    row=0, column=1, padx=5)
Label(imagify_frame, text="By Jam-Burger", font=('Comic Sans MS', 10)
      ).grid(row=1, column=1, padx=5)

# adding buttons
for i in range(4):
    middle_frame.columnconfigure(i, weight=1)

btn_type1 = []
btn_type2 = []

open_image_btn = Button(
    middle_frame, text="Open Image", command=fns.open_img)
open_image_btn.grid(row=0, column=0, columnspan=2)
btn_type1.append(open_image_btn)

save_image_btn = Button(middle_frame, text="Save Image", command=fns.save_img)
save_image_btn.grid(row=0, column=2, columnspan=2)
btn_type1.append(save_image_btn)
Label(middle_frame, text="-"*50, font=('Consolas')
      ).grid(row=1, column=0, columnspan=4)

# crop_rotate_btn = Button(main_frame, image=my_images.crop_rotate_img,
#                          command=lambda: fns.change_frame(dynamic_frame, crop_rotate_frame))
# crop_rotate_btn.grid(row=2, column=0, pady=(20, 0))
# Label(main_frame, text="Crop&\nRotate").grid(row=5, column=0)
# btn_type2.append(crop_rotate_btn)

crop_btn = Button(middle_frame, image=my_images.crop_rotate_img,
                  command=fns.crop_img)
crop_btn.grid(row=2, column=0, pady=(10, 0))
Label(middle_frame, text="Crop").grid(row=3, column=0)
btn_type2.append(crop_btn)

undo_btn = Button(middle_frame, image=my_images.undo_img, command=fns.undo)
undo_btn.grid(row=2, column=1, pady=(10, 0))
Label(middle_frame, text="Undo").grid(row=3, column=1)
btn_type2.append(undo_btn)

redo_btn = Button(middle_frame, image=my_images.redo_img, command=fns.redo)
redo_btn.grid(row=2, column=2, pady=(10, 0))
Label(middle_frame, text="Redo").grid(row=3, column=2)
btn_type2.append(redo_btn)

# adjust_btn = Button(main_frame, image=my_images.adjust_img,
#                     command=lambda: fns.change_frame(dynamic_frame, adjust_frame))
# adjust_btn.grid(row=2, column=3, pady=(20, 0))
# Label(main_frame, text="Adjust").grid(row=5, column=3)
# btn_type2.append(adjust_btn)

resize_btn = Button(middle_frame, image=my_images.resize_img,
                    command=fns.resize_img)
resize_btn.grid(row=2, column=3, pady=(10, 0))
Label(middle_frame, text="Resize").grid(row=3, column=3)
btn_type2.append(resize_btn)

for w in btn_type2:
    w.configure(width=42, height=42, anchor='nw')
for w in btn_type1 + btn_type2:
    w.configure(cursor="circle")
for w in middle_frame.winfo_children():
    w.configure(font=('Consolas', 11), border=0,
                background=color_1, fg=color_2)
for w in btn_type1:
    w.configure(font=('Consolas bold', 13), width=13)

for i in range(4):
    main_frame.columnconfigure(i, weight=1)

rotate_a_btn = Button(
    main_frame, image=my_images.rotate_a_img, command=fns.rotate_a_img)
rotate_a_btn.grid(row=2, column=0)

rotate_c_btn = Button(
    main_frame, image=my_images.rotate_c_img, command=fns.rotate_c_img)
rotate_c_btn.grid(row=2, column=1)

Label(main_frame, text="Rotate").grid(row=3, column=0, columnspan=2)

flip_h_btn = Button(main_frame, image=my_images.flip_h_img,
                    command=fns.flip_h_img)
flip_h_btn.grid(row=2, column=2)

flip_v_btn = Button(main_frame, image=my_images.flip_v_img,
                    command=fns.flip_v_img)
flip_v_btn.grid(row=2, column=3)

Label(main_frame, text="Flip").grid(row=3, column=2, columnspan=2)

Label(main_frame, text="-"*50, font=('Consolas')
      ).grid(row=4, column=0, columnspan=4)

invert_btn = Button(main_frame, image=my_images.invert_img,
                    command=fns.invert_img)
invert_btn.grid(row=5, column=0, pady=(20, 0))
Label(main_frame, text="Invert\nColor").grid(row=6, column=0)


for w in main_frame.winfo_children():
    w.configure(font=('Consolas', 11), border=0,
                background=color_1, fg=color_2)
# setting every frame non-resizable
for w in root.winfo_children():
    w.grid_propagate(0)

root.protocol("WM_DELETE_WINDOW", lambda: fns.quit(root))
root.mainloop()
