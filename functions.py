from msilib.schema import CheckBox
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
    img_window.configure(width=in_w, height=in_h)

p1 = None
p2 = None
rect = c1 = c2 = None

def finished(event):
    img_window.unbind('<ButtonRelease-1>')
    img_window.unbind('<B1-Motion>')
    img_window.unbind('<Button 1>')
    if rect:
        img_window.delete(rect, c1, c2)
    i_w, i_h = current_img.size

    np1 = (int(p1[0]/in_w*i_w), int(p1[1]/in_h*i_h))
    np2 = (int(p2[0]/in_w*i_w), int(p2[1]/in_h*i_h))

    cropped_img = current_img.crop(np1+np2)
    change_img(cropped_img)

def move_p2(event):
    global p2, rect, c1, c2
    iw_w = img_window.winfo_width()
    iw_h = img_window.winfo_height()
    p2 = (event.x, event.y)
    if p2[0] < 0:
        p2[0] = 0
    elif p2[0] > iw_w - 1:
        p2[0] = iw_w - 1
    if p2[1] < 0:
        p2[1] = 0
    elif p2[1] > iw_h - 1:
        p2[1] = iw_h - 1

    x1, y1 = p1
    x2, y2 = p2
    if rect:
        img_window.delete(rect, c1, c2)
    rect = img_window.create_rectangle(
        x1, y1, x2, y2, outline='white', width=3)
    c1 = img_window.create_oval(x1 - 5, y1 - 5, x1 + 5, y1 + 5, fill='black')
    c2 = img_window.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill='black')
    img_window.bind('<ButtonRelease-1>', finished)


def start_making(event):
    global p1, p2
    p1 = p2 = (event.x, event.y)
    img_window.bind('<B1-Motion>', move_p2)


def crop_img():
    if current_img:
        messagebox.showinfo(title="Crop Instruction",
                            message="Select area for crop")
        img_window.bind('<Button 1>', start_making)
    else:
        image_does_not_exist_msg()


def rotate_a_img():
    if current_img:
        rotated_img= current_img.rotate(90, expand= 1)
        change_img(rotated_img)
    else:
        image_does_not_exist_msg()


def rotate_c_img():
    if current_img:
        rotated_img= current_img.rotate(-90, expand= 1)
        change_img(rotated_img)
    else:
        image_does_not_exist_msg()


def flip_h_img():
    if current_img:
        flipped_img= current_img.transpose(Image.FLIP_LEFT_RIGHT)
        change_img(flipped_img)
    else:
        image_does_not_exist_msg()


def flip_v_img():
    if current_img:
        flipped_img= current_img.transpose(Image.FLIP_TOP_BOTTOM)
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


resize_window = None


def resize(w, h):
    try:
        width = w.get()
        height = h.get()
        if width <= 0 or height <= 0 or width > 2000 or height > 2000:
            messagebox.showerror(title="Imagify",
                                 message="Please enter 1 to 2000.")
            resize_window.focus()
        else:
            resize_window.destroy()
            if (width, height) != current_img.size:
                change_img(current_img.resize((width, height)))
    except:
        messagebox.showerror(title="Imagify",
                             message="Please enter valid input.")
        resize_window.focus()


var= width= height = None


def aspect_ratio(height_entry):
    try:
        if var.get():
            height_entry.configure(state= DISABLED)
            height.set(int(width.get()*current_img.size[1]/current_img.size[0]))
        else:
            height_entry.configure(state= NORMAL)
    except:
        messagebox.showerror(title="Imagify",
                             message="Please enter valid input.")
        resize_window.focus()

def resize_img():
    if current_img:
        global resize_window
        if resize_window:
            resize_window.destroy()

        resize_window = Toplevel(img_window)
        resize_window.geometry("300x150")
        resize_window.resizable(0, 0)
        Label(resize_window, text="Width").grid(
            row=0, column=0, padx=10, pady=10)
        Label(resize_window, text="Height").grid(row=1, column=0, padx=10)
        i_w, i_h = current_img.size

        global var, width, height
        width = IntVar(value=i_w)
        height = IntVar(value=i_h)
        width_entry = Entry(resize_window, textvariable=width, width=10, )
        width_entry.grid(
            row=0, column=1, padx=10, pady=10, sticky=W)
        height_entry = Entry(resize_window, textvariable=height, width=10)
        height_entry.grid(
            row=1, column=1, padx=10, pady=10, sticky=W)
        width_entry.configure(invcmd= lambda: aspect_ratio(height_entry))
        var = IntVar(value=0)
        Checkbutton(resize_window, text="Keep Aspect Ratio", variable=var, command=lambda: aspect_ratio(height_entry)).grid(
            row=2, column=0, padx=10, pady=10, sticky=W)
        Button(resize_window, text="OK", width=10,
               command=lambda: resize(width, height)).grid(row=2, column=1, padx=10, pady=10, sticky=W)
    else:
        image_does_not_exist_msg()


def undo(event=None):
    global current
    if current_img:
        if current - 1 >= 0:
            current -= 1
            change_img(history_data[current], False)
    else:
        image_does_not_exist_msg()


def redo(event=None):
    global current
    if current_img:
        if current + 1 < len(history_data):
            current += 1
            change_img(history_data[current], False)
    else:
        image_does_not_exist_msg()


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
            title='Open File', initialdir='./', filetypes=filetypes)
    elif type == 'save':
        filename = filedialog.asksaveasfilename(
            title='Save', initialfile='Imagify_img', defaultextension='.png', filetypes=filetypes)

    return filename


def open_img(event=None):
    filename = select_path('open')
    if(filename):
        img = Image.open(filename)
        if img:
            global current
            history_data.clear()
            current = -1
            change_img(img)


def save_img(event=None):
    if current_img:
        path = select_path('save')
        if path:
            current_img.save(path)
    else:
        image_does_not_exist_msg()


def quit(parent):
    if len(history_data) > 1:
        ans = messagebox.askyesnocancel(
            "Imagify", "Do you want to save your changes?", icon='warning')
        if ans == True:
            save_img()
        elif ans == False:
            parent.destroy()
    elif messagebox.askokcancel("Imagify", "Do you want to quit?", icon='warning'):
        parent.destroy()


def about(event=None):
    messagebox.showinfo(
        title="Imagify", message="Imagify", detail="Version: 1.0.1\nProduct of Jam-Burger\nDeveloped by Jay")


def not_done_msg():
    messagebox.showinfo(
        title="Imagify", message="This feature is not done yet.")


def image_does_not_exist_msg():
    messagebox.showerror(title="Imagify",
                         message="Please add an image first.")
