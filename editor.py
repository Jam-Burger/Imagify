from tkinter import *
from PIL import Image

import functions as fns
from resources import Images
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# creating screen

root = Tk()
root.iconbitmap("images/logo.ico")
root.title("Imagify - Jam-burger")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
bg_color = "#90A8F4"

root.geometry(f"{width}x{height}")
root.configure(bg=bg_color, bd=10, highlightcolor="#98F", highlightthickness=5)

menu_bar = Menu(root)
root.configure(menu=menu_bar)

file_menu = Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open")

i_f_w = height - 140
i_f_h = int(i_f_w*1.55)
c1_width = width - i_f_h - 60

# creating basic layout
img_window_frame= Frame(root, bg="#001", width=i_f_h, height=i_f_w)
img_window_frame.grid(row=0, column=0, rowspan=3)
img_window_frame.pack_propagate(0)
img_window = Canvas(img_window_frame, bg='black', highlightthickness=0)
img_window.pack(expand=1)
fns.set_img_window(img_window, i_f_h, i_f_w)
fns.change_img(Image.open("images/default.jpg"))

imagify_frame = Frame(root, border=3, borderwidth=5, padx=10, pady=10,
                      width=c1_width, height=125, cursor="heart", relief=RIDGE)
imagify_frame.grid(row=0, column=1, padx=10, pady=(
    10, 0), ipadx=5, ipady=5, sticky=N)

color_1 = "#041a3d"
color_2 = "#fff3b8"

main_frame_height = height/5
main_frame = Frame(root, border=3, borderwidth=5, bg=color_1,
                   pady=10, width=c1_width, height=main_frame_height, relief=RIDGE)
main_frame.grid(row=1, column=1, padx=10, pady=(
    10, 0), ipadx=5, ipady=5, sticky=N)

dynamic_frame = Frame(root, border=3, borderwidth=5, bg=color_1,
                      pady=10, width=c1_width, height=height - 350 - main_frame_height, relief=RIDGE)
dynamic_frame.grid(row=2, column=1, padx=10, pady=(5, 0), sticky=N)

crop_rotate_frame = Frame(dynamic_frame, bg=color_1,
                          width=c1_width, height=height - 350 - main_frame_height, pady=20)
crop_rotate_frame.pack()

adjust_frame = Frame(dynamic_frame, bg='black',
                         width=c1_width, height=height - 350 - main_frame_height)

# importing images
img = None
my_images= Images()
logo_img = my_images.logo

# adding stuff in frames

Label(imagify_frame, image=logo_img).grid(row=0, column=0, rowspan=2)
Label(imagify_frame, text="Imagify", font=('Comic Sans MS bold', 20)).grid(
    row=0, column=1, padx=5)
Label(imagify_frame, text="By Jam-Burger", font=('Comic Sans MS', 10)
      ).grid(row=1, column=1, padx=5)

# adding buttons
for i in range(4):
    main_frame.columnconfigure(i, weight=1)


btn_type1 = []
btn_type2 = []

open_image_btn = Button(
    main_frame, text="Open Image", command=fns.open_img)
open_image_btn.grid(row=0, column=0, columnspan=2)
btn_type1.append(open_image_btn)

save_image_btn = Button(main_frame, text="Save Image", command=fns.save_img)
save_image_btn.grid(row=0, column=2, columnspan=2)
btn_type1.append(save_image_btn)

Label(main_frame, text="-"*50, font=('Consolas')).grid(row=1, column=0, columnspan=4)

# crop_rotate_btn = Button(main_frame, image=my_images.crop_rotate_img,
#                          command=lambda: fns.change_frame(dynamic_frame, crop_rotate_frame))
# crop_rotate_btn.grid(row=2, column=0, pady=(20, 0))
# Label(main_frame, text="Crop&\nRotate").grid(row=5, column=0)
# btn_type2.append(crop_rotate_btn)

undo_btn = Button(main_frame, image=my_images.undo_img, command=fns.undo)
undo_btn.grid(row=2, column=1, pady=(20, 0))
Label(main_frame, text="Undo").grid(row=3, column=1)
btn_type2.append(undo_btn)

redo_btn = Button(main_frame, image=my_images.redo_img, command=fns.redo)
redo_btn.grid(row=2, column=2, pady=(20, 0))
Label(main_frame, text="Redo").grid(row=3, column=2)
btn_type2.append(redo_btn)

# adjust_btn = Button(main_frame, image=my_images.adjust_img,
#                     command=lambda: fns.change_frame(dynamic_frame, adjust_frame))
# adjust_btn.grid(row=2, column=3, pady=(20, 0))
# Label(main_frame, text="Adjust").grid(row=5, column=3)
# btn_type2.append(adjust_btn)

resize_btn = Button(main_frame, image=my_images.resize_img,
                    command=lambda: fns.resize_img(root))
resize_btn.grid(row=2, column=0, pady=(20, 0))
Label(main_frame, text="Resize").grid(row=3, column=0)
btn_type2.append(resize_btn)

invert_btn = Button(main_frame, image=my_images.invert_img, command=fns.invert_img)
invert_btn.grid(row=2, column=3, pady=(20, 0))
Label(main_frame, text="Invert\nColor").grid(row=3, column=3)
btn_type2.append(invert_btn)

for w in btn_type2:
    w.configure(width=42, height=42, anchor='nw')
for w in btn_type1 + btn_type2:
    w.configure(cursor="circle")
for w in main_frame.winfo_children():
    w.configure(font=('Consolas', 11), border=0,
                background=color_1, fg=color_2)
for w in btn_type1:
    w.configure(font=('Consolas bold', 13), width=13)

for i in range(4):
    crop_rotate_frame.columnconfigure(i, weight=1)

rotate_a_btn = Button(crop_rotate_frame, image=my_images.rotate_a_img, command=fns.rotate_a_img)
rotate_a_btn.grid(row=2, column=0)

rotate_c_btn = Button(crop_rotate_frame, image=my_images.rotate_c_img, command=fns.rotate_c_img)
rotate_c_btn.grid(row=2, column=1)

Label(crop_rotate_frame, text="Rotate").grid(row=3, column=0, columnspan=2)

flip_h_btn = Button(crop_rotate_frame, image=my_images.flip_h_img, command=fns.flip_h_img)
flip_h_btn.grid(row=2, column=2)

flip_v_btn = Button(crop_rotate_frame, image=my_images.flip_v_img, command=fns.flip_v_img)
flip_v_btn.grid(row=2, column=3)

Label(crop_rotate_frame, text="Flip").grid(row=3, column=2, columnspan=2)

crop_btn = Button(crop_rotate_frame, image=my_images.crop_rotate_img,
                         command= fns.crop_img)
crop_btn.grid(row=4, column=0, pady=(20, 0))
Label(crop_rotate_frame, text="Crop").grid(row=5, column=0)

for w in crop_rotate_frame.winfo_children():
    w.configure(font=('Consolas', 11), border=0,
                background=color_1, fg=color_2)

# setting every frame non-resizable
dynamic_frame.pack_propagate(0)
for w in root.winfo_children() + dynamic_frame.winfo_children():
    w.grid_propagate(0)

root.mainloop()
