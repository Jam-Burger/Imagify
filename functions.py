from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

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
    
def change_img(new_img, img_window):
    global iw_w, iw_h
    iw_w= img_window.winfo_width()
    iw_h= img_window.winfo_height()
    i_w, i_h = new_img.size
    w_s = i_w/iw_w
    h_s = i_h/iw_h
    if w_s < h_s:
        n_w = i_w/h_s
        n_h = iw_h
    else:
        n_w = iw_w
        n_h = i_h/w_s
    
    global img, photo
    img= new_img
    photo = ImageTk.PhotoImage(img.resize((int(n_w) - 25, int(n_h) - 25)))

    for w in img_window.winfo_children():
        w.pack_forget()
    Label(img_window, image= photo).pack(padx= (iw_w-n_w)/2, pady= (iw_h-n_h)/2)

def select_img(img_window):
    filename= select_path('open')
    if(filename):
        img = Image.open(filename)
        change_img(img, img_window)

def save_img(img):
    not_done()
    # if img:
    #     img.save(select_path('save'))

def not_done():
    messagebox.showinfo(title="Sorry !", message="This feature is not done yet.")