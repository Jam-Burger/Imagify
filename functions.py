from dbm import ndbm
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import numpy as np

img_window= None
current_img= None
iw_w = iw_h= 0

undo_data= []
current= -1

def set_img_window(i_w, w_w, w_h):
    global img_window, iw_w, iw_h
    img_window= i_w
    iw_w= w_w
    iw_h= w_h

def change_img(new_img, add_in_history= True):
    # if not img_window: return
    i_w, i_h = new_img.size
    if i_w > 1400:
        new_img= new_img.resize((1400, int(1400*i_h/i_w)))
    w_s = i_w/iw_w
    h_s = i_h/iw_h
    if w_s < h_s:
        n_w = i_w/h_s
        n_h = iw_h
    else:
        n_w = iw_w
        n_h = i_h/w_s
    
    global current_img, photo, current
    current_img= new_img
    if add_in_history:
        for e in undo_data[current+1:]:
            undo_data.remove(e)
        undo_data.append(current_img)
        current+=1

    photo = ImageTk.PhotoImage(current_img.resize((int(n_w) - 25, int(n_h) - 25)))
    for w in img_window.winfo_children():
        w.pack_forget()
    Label(img_window, image= photo).pack(padx= (iw_w-n_w)//2, pady= (iw_h-n_h)//2)
     
def rotate_a_img():
    if current_img:
        i_data= current_img.load()
        width, height= current_img.size
        rotated_img= Image.new(current_img.mode, (height, width))
        for i in range(width):
            for j in range(height):
                rotated_img.putpixel((j, width-i-1), i_data[i, j])
        change_img(rotated_img)
    else:
        image_does_not_exist_msg()
def rotate_c_img():
    if current_img:
        i_data= current_img.load()
        width, height= current_img.size
        rotated_img= Image.new(current_img.mode, (height, width))
        for i in range(width):
            for j in range(height):
                rotated_img.putpixel((height-j-1, i), i_data[i, j])
        change_img(rotated_img)
    else:
        image_does_not_exist_msg()

def flip_h_img():
    if current_img:
        i_data= current_img.load()
        width, height= current_img.size
        flipped_img= Image.new(current_img.mode, (width, height))
        for i in range(width):
            for j in range(height):
                flipped_img.putpixel((width-i-1, j), i_data[i, j])
        change_img(flipped_img)
    else:
        image_does_not_exist_msg()
def flip_v_img():
    if current_img:
        i_data= current_img.load()
        width, height= current_img.size
        flipped_img= Image.new(current_img.mode, (width, height))
        for i in range(width):
            for j in range(height):
                flipped_img.putpixel((i, height-j-1), i_data[i, j])
        change_img(flipped_img)
    else:
        image_does_not_exist_msg()
invert= lambda c: (255-c[0], 255-c[1], 255-c[2])
def invert_img():
    if current_img:
        i_data= current_img.load()
        width, height= current_img.size
        inverted_img= Image.new(current_img.mode, (width, height))
        for i in range(width):
            for j in range(height):
                inverted_img.putpixel((i, j), invert(i_data[i, j]))
        change_img(inverted_img)
    else:
        image_does_not_exist_msg()   
def undo():
    global current
    if current - 1>= 0:
        change_img(undo_data[current-1], False)
        current-=1

def redo():
    global current
    if current + 1 < len(undo_data):
        change_img(undo_data[current+1], False)
        current+=1


def select_path(type):
    filename= ""
    filetypes = (
            ('All Picture Files', ['*.png', '*.jpg', '*.jpeg', '*.bmp']),
            ('JPEG (*.jpeg)','*.jpeg'),
            ('JPG (*.jpg)', '*.jpg'),
            ('PNG (*.png)', '*.png'),
            ('BMP (*.bmp)', '*.bmp'),
            ('All Files', '*.*')
        )
    if type=='open':
        filename = filedialog.askopenfilename(title='Select an Image File', filetypes=filetypes)
    elif type=='save':
        filename = filedialog.asksaveasfilename(title='Select where to save', filetypes=filetypes, defaultextension=filetypes)

    return filename

def select_img():
    filename= select_path('open')
    if(filename):
        img = Image.open(filename)
        change_img(img)

def save_img():
    if current_img:
        path= select_path('save')
        current_img.save(path)

def not_done_msg():
    messagebox.showinfo(title="Sorry !", message="This feature is not done yet.")

def image_does_not_exist_msg():
    messagebox.showerror(title="Image not Found", message="Please add an image first.")