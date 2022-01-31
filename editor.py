from tkinter import *
from PIL import Image

import functions as fns
from resources import Images
import design
from design import LabeledButton, Line, DoubleLabledButton, Slider
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

edit_menu = Menu(menu_bar, tearoff=0, activeborderwidth=5)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=fns.undo, accelerator="Ctrl+Z")
root.bind('<Control-z>', fns.undo)
edit_menu.add_command(label="Redo", command=fns.redo, accelerator="Ctrl+Y")
root.bind('<Control-y>', fns.redo)
edit_menu.add_separator()
edit_menu.add_command(label="Copy", command=fns.copy, accelerator="Ctrl+C")
root.bind('<Control-c>', fns.copy)
edit_menu.add_command(label="Paste", command=fns.paste, accelerator="Ctrl+V")
root.bind('<Control-v>', fns.paste)

help_menu = Menu(menu_bar, tearoff=0, activeborderwidth=5)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=fns.about)

i_f_w = height - 140
i_f_h = int(i_f_w*1.55)
main_frame_width = width - i_f_h - 60

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
                      width=main_frame_width, height=125, cursor="heart", relief=RIDGE)
imagify_frame.grid(row=0, column=1, padx=10, pady=(
    10, 0), ipadx=5, ipady=5, sticky=N)

color_1 = design.color_1
color_2 = design.color_2

middle_frame_height = height*.15
middle_frame = Frame(root, height=middle_frame_height, border=3, borderwidth=5, bg=color_1,
                     pady=10, width=main_frame_width, relief=RIDGE)
middle_frame.grid(row=1, column=1, padx=10, pady=(
    10, 0), ipadx=5, ipady=5, sticky=N)

main_frame = Frame(root, height=height - 340 - middle_frame_height, border=3, borderwidth=5, bg=color_1,
                   pady=10, width=main_frame_width, relief=RIDGE)
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

# adding stuff in middle_frame
for i in range(4):
    middle_frame.columnconfigure(i, weight=1)
open_image_btn = Label(middle_frame, text="Open Image")
open_image_btn.grid(row=0, column=0, columnspan=2)
open_image_btn.bind('<Button 1>', fns.open_img)

save_image_btn = Label(middle_frame, text="Save Image")
save_image_btn.grid(row=0, column=2, columnspan=2)
save_image_btn.bind('<Button 1>', fns.save_img)

for w in middle_frame.winfo_children():
    w.configure(bg=color_1, fg=color_2, width=13,
                font=('Consolas bold', 13), cursor='circle')

Line(middle_frame, 1)

LabeledButton(middle_frame, 2, 0, my_images.crop_img, 'Crop', fns.crop_img)
LabeledButton(middle_frame, 2, 1, my_images.undo_img, 'Undo', fns.undo)
LabeledButton(middle_frame, 2, 2, my_images.redo_img, 'Redo', fns.redo)
LabeledButton(middle_frame, 2, 3, my_images.resize_img,
              'Resize', fns.resize_img)

for i in range(4):
    main_frame.columnconfigure(i, weight=1)

DoubleLabledButton(main_frame, 0, 0, 'Rotate',  (my_images.rotate_a_img,
                   fns.rotate_a_img), (my_images.rotate_c_img, fns.rotate_c_img))
DoubleLabledButton(main_frame, 0, 2, 'Flip',  (my_images.flip_h_img,
                   fns.flip_h_img), (my_images.flip_v_img, fns.flip_v_img))

Line(main_frame, 1)

LabeledButton(main_frame, 2, 0, my_images.copy_img, 'Copy', fns.copy)
LabeledButton(main_frame, 2, 1, my_images.paste_img, 'Paste', fns.paste)
LabeledButton(main_frame, 2, 2, my_images.effects_img, 'Effects', fns.effects)
LabeledButton(main_frame, 2, 3, my_images.add_img, 'Add Image', fns.add_img)

Line(main_frame, 3, pady=(0, 10))

brightness_slider = Slider(main_frame, 4, main_frame_width*.7,
                           'Brightness', fns.update_brightness, fns.apply_enhance)
contrast_slider = Slider(main_frame, 5, main_frame_width*.7,
                         'Contrast', fns.update_contrast, fns.apply_enhance)
sharpness_slider = Slider(main_frame, 6, main_frame_width*.7,
                          'Sharpness', fns.update_sharpness, fns.apply_enhance)
color_slider = Slider(main_frame, 7, main_frame_width*.7,
                      'Color', fns.update_color, fns.apply_enhance)

Line(main_frame, 8)

status = Label(main_frame, bg=color_1, text='----Status----',
               fg=color_2, font=('Consolas bold', 10))
status.grid(row=9, column=0, columnspan=4)
if fns.current_img is None:
    status.configure(text="Open a new image")

fns.set_status(status)
# setting every frame non-resizable
for w in root.winfo_children():
    w.grid_propagate(0)

root.protocol("WM_DELETE_WINDOW", lambda: fns.quit(root))
root.mainloop()
