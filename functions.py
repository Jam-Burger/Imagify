from dbm import ndbm
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import numpy as np

img_window= None
current_img= None
iw_w = iw_h= 0

def set_img_window(i_w, w_w, w_h):
    global img_window, iw_w, iw_h
    img_window= i_w
    iw_w= w_w
    iw_h= w_h

def change_img(new_img):
    # if not img_window: return
    i_w, i_h = new_img.size
    w_s = i_w/iw_w
    h_s = i_h/iw_h
    if w_s < h_s:
        n_w = i_w/h_s
        n_h = iw_h
    else:
        n_w = iw_w
        n_h = i_h/w_s
    
    global current_img, photo
    current_img= new_img
    photo = ImageTk.PhotoImage(current_img.resize((int(n_w) - 25, int(n_h) - 25)))

    for w in img_window.winfo_children():
        w.pack_forget()
    Label(img_window, image= photo).pack(padx= (iw_w-n_w)//2, pady= (iw_h-n_h)//2)

def new_2d_array(width, height):
    arr= []
    for i in range(height):
        row=[]
        for j in range(width):
            row.append(None)
        arr.append(row)
    return arr
        
def rotate_a_img():
    if current_img:
        i_data= np.array(current_img)
        width, height= current_img.size
        n_data= new_2d_array(height, width)
        for i in range(height):
            for j in range(width):
                n_data[width-j-1][i]= i_data[i, j]
        rotate_img= Image.fromarray(np.array(n_data))
        change_img(rotate_img)
    else:
        image_does_not_exist_msg()
def rotate_c_img():
    if current_img:
        i_data= np.array(current_img)
        width, height= current_img.size
        n_data= new_2d_array(height, width)
        for i in range(height):
            for j in range(width):
                n_data[j][height-i-1]= i_data[i, j]
        rotate_img= Image.fromarray(np.array(n_data))
        change_img(rotate_img)
    else:
        image_does_not_exist_msg()

def flip_h_img():
    if current_img:
        i_data= np.array(current_img)
        width, height= current_img.size
        n_data= new_2d_array(width, height)
        for i in range(height):
            for j in range(width):
                n_data[i][width-1-j]= i_data[i, j]
        rotate_img= Image.fromarray(np.array(n_data))
        change_img(rotate_img)
    else:
        image_does_not_exist_msg()
def flip_v_img():
    if current_img:
        i_data= np.array(current_img)
        width, height= current_img.size
        n_data= new_2d_array(width, height)
        for i in range(height):
            for j in range(width):
                n_data[height-i-1][j]= i_data[i, j]
        rotate_img= Image.fromarray(np.array(n_data))
        change_img(rotate_img)
    else:
        image_does_not_exist_msg()

        
def undo():
    not_done_msg()

def redo():
    not_done_msg()


def select_path(type):
    filename= ""
    filetypes = (
            ('All Picture Files', ['*.png', '*.jpg', '*.jpeg']),
            ('JPEG (*.jpg, *.jpeg)', ['*.jpg', '*.jpeg']),
            ('PNG (*.png)', '*.png'),
            ('All Files', '*.*')
        )
    if type=='open':
        filename = filedialog.askopenfilename(title='Select an Image File', filetypes=filetypes)
    elif type=='save':
        filename = filedialog.asksaveasfile(title='Select where to save', mode='w', filetypes=filetypes, defaultextension=".png")

    return filename

def select_img():
    filename= select_path('open')
    if(filename):
        img = Image.open(filename)
        change_img(img)

def save_img():
    not_done_msg()
    # if img:
    #     img.save(select_path('save'))

def not_done_msg():
    messagebox.showinfo(title="Sorry !", message="This feature is not done yet.")

def image_does_not_exist_msg():
    messagebox.showerror(title="Image not Found", message="Please add an image first.")