from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

img_window = None
current_img = None
iw_w = iw_h = 0

history_data = []
current = -1

def set_img_window(i_w, w_w, w_h):
    global img_window, iw_w, iw_h
    img_window = i_w
    iw_w = w_w
    iw_h = w_h


def change_img(new_img, add_in_history=True):
    # if not img_window: return
    i_w, i_h = new_img.size
    if i_w > 1400:
        new_img = new_img.resize((1400, int(1400*i_h/i_w)))
    w_s = i_w/iw_w
    h_s = i_h/iw_h
    if w_s < h_s:
        n_w = i_w/h_s
        n_h = iw_h
    else:
        n_w = iw_w
        n_h = i_h/w_s

    global current_img, photo, current
    current_img = new_img
    if add_in_history:
        for e in history_data[current+1:]:
            history_data.remove(e)
        history_data.append(current_img)
        current += 1

    photo = ImageTk.PhotoImage(
        current_img.resize((int(n_w) - 20, int(n_h) - 20)))
    img_window.create_image(iw_w/2, iw_h/2, image= photo)


def change_frame(parent, frame):
    pass


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


invert= lambda c: (255-c[0], 255-c[1], 255-c[2])


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
    layer = Toplevel(parent)
    layer.title("Select New Size")
    Label(layer, text="I am in").pack()


def undo():
    global current
    if current - 1 >= 0:
        current -= 1
        change_img(history_data[current], False)


def redo():
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
            title='Select where to save', initialfile='Imagify_img', defaultextension='.png', filetypes=filetypes)

    return filename


def open_img():
    filename = select_path('open')
    if(filename):
        img = Image.open(filename)
        change_img(img)


def save_img():
    if current_img:
        path = select_path('save')
        current_img.save(path)


def not_done_msg():
    messagebox.showinfo(
        title="Sorry !", message="This feature is not done yet.")


def image_does_not_exist_msg():
    messagebox.showerror(title="Image not Found",
                         message="Please add an image first.")
