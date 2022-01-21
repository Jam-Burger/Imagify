from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog

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

frame1 = LabelFrame(root, border=3, padx=10, pady=10, width=c1_width, height=120)
frame1.grid(row=0, column=2, padx=10, pady=(10, 0), ipadx=5, ipady=5, sticky=N)

frame2= LabelFrame(root, border=3, padx=10, pady=10, width=c1_width, height=height/2 - 50)
frame2.grid(row=2, column=2, padx=10, pady=(0, 10), ipadx=5, ipady=5, sticky=N)

# adding stuff in frames

img1 = Image.open("images/Imagify-logo.jpeg")
img1 = ImageTk.PhotoImage(img1.resize((100, 100)))
Label(frame1, image=img1).grid(row=1, column=0, rowspan=2)

Label(frame1, text="Imagify", font=('Comic Sans MS bold', 20)).grid(row=1, column=1, padx=5, pady=5, sticky=W)
Label(frame1, text="By Jam-Burger", font=('Comic Sans MS', 10)).grid(row=2, column=1, padx=5, pady=5)

# adding buttons
frame2.columnconfigure(0, weight=1);
frame2.columnconfigure(1, weight=1);

select_image_btn= Button(frame2, text="Select Image", font=('bold'), bg=bg_color)
select_image_btn.grid(row=0, column=0)

save_image_btn= Button(frame2, text="Save Image", font=('bold'), bg=bg_color)
save_image_btn.grid(row=0, column=1)

# setting every frame non-resizable

for w in root.winfo_children():
    w.grid_propagate(0)

def select_path(type):
    filename= ""
    if type=='open':
        filetypes = (
            ('All Picture Files', ['*.png', '*.jpg', '*.jpeg', '*.ico']),
            ('JPEG (*.jpg, *.jpeg)', ['*.jpg', '*.jpeg']),
            ('PNG (*.png)', '*.png'),
            ('All Files', '*.*')
        )
        filename = filedialog.askopenfilename(title='Select an Image File', filetypes=filetypes)
    elif type=='save':
        filename = filedialog.asksaveasfilename(title='Select where to save', mode='w', defaultextension=".jpg")

    return filename

def change_img(new_img):
    global img_window, iw_w, iw_h
    i_w, i_h = new_img.size
    w_s = i_w/iw_w
    h_s = i_h/iw_h
    if w_s < h_s:
        n_w = i_w/h_s
        n_h = iw_h
    else:
        n_w = iw_w
        n_h = i_h/w_s
    global img
    img = ImageTk.PhotoImage(new_img.resize((int(n_w) - 25, int(n_h) - 25)))
    for w in img_window.winfo_children():
        w.pack_forget()
    Label(img_window, image= img).pack(padx= (iw_w-n_w)/2, pady= (iw_h-n_h)/2)

def select_img():
    filename= select_path('open')
    if(filename):
        img = Image.open(filename)
        change_img(img)

def save_img():
    global img_window
    if len(img_window.winfo_children())==1:
        img= Image.open(img_window.winfo_children()[0])
        img.save(select_path('save'))

select_image_btn.configure(command=select_img)
# save_image_btn.configure(command=save_img)
root.mainloop()
