from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

img_window = None
current_img = None
i_f_w = i_f_h = 0

history_data = []
current = -1


def set_img_window(i_w, w_w, w_h):
    global img_window, i_f_w, i_f_h
    img_window = i_w
    i_f_w = w_w
    i_f_h = w_h


def change_img(new_img, add_in_history=True):
    # if a very large image is given then resize
    i_w, i_h = new_img.size
    if i_w > 1400:
        new_img = new_img.resize((1400, int(1400*i_h/i_w)))
    elif i_h > 1400:
        new_img = new_img.resize((int(1400*i_w/i_h), 1400))

    i_w, i_h = new_img.size 
    global current_img, photo, current, in_w, in_h
    w_s = i_w/i_f_w
    h_s = i_h/i_f_h
    if w_s < h_s:
        in_w = int(i_w/h_s)
        in_h = i_f_h
    else:
        in_w = i_f_w
        in_h = int(i_h/w_s)

    current_img = new_img
    if add_in_history:
        for e in history_data[current+1:]:
            history_data.remove(e)
        history_data.append(current_img)
        current += 1

    photo = ImageTk.PhotoImage(current_img.resize((in_w, in_h)))
    img_window.create_image(in_w/2, in_h/2, image=photo)
    img_window.configure(width= in_w, height= in_h)

def change_frame(parent, frame):
    pass

p1= None
p2= None      

rect= c1= c2 = None

def finished(event):
    img_window.unbind('<ButtonRelease-1>')
    img_window.unbind('<B1-Motion>')
    img_window.unbind('<Button 1>')
    if rect:
        img_window.delete(rect, c1, c2)
    i_w, i_h= current_img.size

    np1= (int(p1[0]/in_w*i_w), int(p1[1]/in_h*i_h))
    np2= (int(p2[0]/in_w*i_w), int(p2[1]/in_h*i_h))

    i_data = current_img.load()
    width= np2[0] - np1[0]
    height= np2[1] - np1[1]
    dx= 0 if width==0 else int(abs(width)/width)
    dy= 0 if height==0 else int(abs(height)/height)

    cropped_img = Image.new(current_img.mode, (abs(width), abs(height)))

    x = 0
    for i in range(np1[0], np2[0], dx):
        y = 0
        for j in range(np1[1], np2[1], dy):
            x0= x if dx==1 else abs(width)-x-1
            y0= y if dy==1 else abs(height)-y-1
            cropped_img.putpixel((x0, y0), i_data[i, j])
            y += 1
        x += 1
        
    change_img(cropped_img)
    
def move_p2(event):
    global p2, rect, c1, c2
    iw_w = img_window.winfo_width()
    iw_h = img_window.winfo_height()
    p2 = (event.x, event.y)
    if p2[0] < 0: p2[0] = 0
    elif p2[0] > iw_w - 1: p2[0] = iw_w - 1
    if p2[1] < 0: p2[1] = 0
    elif p2[1] > iw_h - 1: p2[1] = iw_h - 1

    x1, y1= p1
    x2, y2= p2
    if rect:
        img_window.delete(rect, c1, c2)
    rect = img_window.create_rectangle(x1, y1, x2, y2, outline= 'white', width= 3)
    c1 = img_window.create_oval(x1 - 5, y1 - 5, x1 + 5, y1 + 5, fill='black')
    c2 = img_window.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill='black')
    img_window.bind('<ButtonRelease-1>', finished)

def start_making(event):
    global p1, p2
    p1 = p2 = (event.x, event.y)
    img_window.bind('<B1-Motion>', move_p2)

def crop_img():
    if current_img:
        messagebox.showinfo(title="Crop Instruction", message="Select area for crop")
        img_window.bind('<Button 1>', start_making)
    else:
        image_does_not_exist_msg()


def rotate_a_img():
    if current_img:
        i_data = current_img.load()
        width, height = current_img.size
        rotated_img = Image.new(current_img.mode, (height, width))
        for i in range(width):
            for j in range(height):
                rotated_img.putpixel((j, width-i-1), i_data[i, j])
        change_img(rotated_img)
    else:
        image_does_not_exist_msg()


def rotate_c_img():
    if current_img:
        i_data = current_img.load()
        width, height = current_img.size
        rotated_img = Image.new(current_img.mode, (height, width))
        for i in range(width):
            for j in range(height):
                rotated_img.putpixel((height-j-1, i), i_data[i, j])
        change_img(rotated_img)
    else:
        image_does_not_exist_msg()


def flip_h_img():
    if current_img:
        i_data = current_img.load()
        width, height = current_img.size
        flipped_img = Image.new(current_img.mode, (width, height))
        for i in range(width):
            for j in range(height):
                flipped_img.putpixel((width-i-1, j), i_data[i, j])
        change_img(flipped_img)
    else:
        image_does_not_exist_msg()


def flip_v_img():
    if current_img:
        i_data = current_img.load()
        width, height = current_img.size
        flipped_img = Image.new(current_img.mode, (width, height))
        for i in range(width):
            for j in range(height):
                flipped_img.putpixel((i, height-j-1), i_data[i, j])
        change_img(flipped_img)
    else:
        image_does_not_exist_msg()


def invert(c): return (255-c[0], 255-c[1], 255-c[2])


def invert_img():
    if current_img:
        i_data = current_img.load()
        width, height = current_img.size
        inverted_img = Image.new(current_img.mode, (width, height))
        for i in range(width):
            for j in range(height):
                inverted_img.putpixel((i, j), invert(i_data[i, j]))
        change_img(inverted_img)
    else:
        image_does_not_exist_msg()


def resize_img(parent):
    not_done_msg()
    # if current_img:
    #     layer= Toplevel(img_window, width=200, height=200)
    #     layer.resizable(0, 0)
    # else:
    #     image_does_not_exist_msg()


def undo(event):
    global current
    if current - 1 >= 0:
        current -= 1
        change_img(history_data[current], False)


def redo(event):
    global current
    if current + 1 < len(history_data):
        current += 1
        change_img(history_data[current], False)


def select_path(type):
    filename = ""
    filetypes = (
        ('All Picture Files', ['*.png', '*.jpg', '*.jpeg', '*.bmp']),
        ('JPEG (*.jpeg)', '*.jpeg'),
        ('JPG (*.jpg)', '*.jpg'),
        ('PNG (*.png)', '*.png'),
        ('BMP (*.bmp)', '*.bmp'),
        ('All Files', '*.*')
    )
    if type == 'open':
        filename = filedialog.askopenfilename(
            title='Select an Image File', initialdir='./', filetypes=filetypes)
    elif type == 'save':
        filename = filedialog.asksaveasfilename(
            title='Select Where to Save', initialfile='Imagify_img', defaultextension='.png', filetypes=filetypes)

    return filename


def open_img(event):
    filename = select_path('open')
    if(filename):
        img = Image.open(filename)
        if img:
            global current
            history_data.clear()
            current= -1
            change_img(img)


def save_img(event):
    if current_img:
        path = select_path('save')
        if path:
            current_img.save(path)

def about():
    messagebox.showinfo(
        title="About", message="<b>Imagify</b>")
def not_done_msg():
    messagebox.showinfo(
        title="Sorry !", message="This feature is not done yet.")


def image_does_not_exist_msg():
    messagebox.showerror(title="Image not Found",
                         message="Please add an image first.")
