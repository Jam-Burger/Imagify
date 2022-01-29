from math import sqrt
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance, ImageOps
from PIL.ImageFilter import *
from tkinter import filedialog, messagebox

img_window = None
current_img = None
clipboard_img = None
i_f_w = i_f_h = 0

history_data = []
current = -1

status = None


def set_img_window(i_w, f_w, f_h):
    global img_window, i_f_w, i_f_h
    img_window = i_w
    i_f_w = f_w
    i_f_h = f_h


def set_status(st):
    global status
    status = st

def update_status(val):
    status.configure(text=val)

def success_status():
    update_status("Changes are done successfully")

def fit_image(img, w, h):
    i_w, i_h = img.size
    w_s = i_w/w
    h_s = i_h/h
    global in_w, in_h
    if w_s < h_s:
        in_w = int(i_w/h_s)
        in_h = h
    else:
        in_w = w
        in_h = int(i_h/w_s)
    return img.resize((in_w, in_h))

def change_img(new_img, add_in_history=True, update=True):
    global current_img, photo, current
    w, h = new_img.size
    if w > 2048 or h > 2048:
        new_img = fit_image(new_img, 2048, 2048)

    if update:
        current_img = new_img
    if add_in_history:
        for e in history_data[current+1:]:
            history_data.remove(e)
        history_data.append(new_img)
        current += 1
    new_img = fit_image(new_img, i_f_w, i_f_h)

    photo = ImageTk.PhotoImage(new_img)
    img_window.create_image(in_w/2, in_h/2, image=photo)
    img_window.configure(width=in_w, height=in_h)
    if status is not None and update: success_status()


def origional(cord):
    i_w, i_h = current_img.size
    return (int(cord[0]/in_w*i_w), int(cord[1]/in_h*i_h))


def valid(a, b):
    w = abs(b[0]-a[0])
    h = abs(b[1]-a[1])
    center = [(b[0]+a[0])/2, (b[1]+a[1])/2]
    a = (center[0]-w/2, center[1]-h/2)
    b = (center[0]+w/2, center[1]+h/2)
    return origional(a) + origional(b)


def dist(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**.5


class Selection:
    def __init__(self, cmd, img=None):
        img_window.bind('<Button 1>', self.start)
        self.command = cmd
        self.rect = None
        self.img = img

    def start(self, mouse):
        img_window.unbind('<Button 1>')
        self.p1 = self.p2 = [mouse.x, mouse.y]
        img_window.bind('<B1 Motion>', self.expand)
        img_window.bind('<Double Button 1>', self.end)

    def expand(self, mouse):
        iw_w = img_window.winfo_width()
        iw_h = img_window.winfo_height()
        self.p2 = [mouse.x, mouse.y]
        if self.p2[0] < 0:
            self.p2[0] = 0
        elif self.p2[0] > iw_w - 1:
            self.p2[0] = iw_w - 1
        if self.p2[1] < 0:
            self.p2[1] = 0
        elif self.p2[1] > iw_h - 1:
            self.p2[1] = iw_h - 1
        self.draw()
        update_status("Selecting")
        img_window.bind('<ButtonRelease 1>', self.drew)

    def drew(self, mouse):
        update_status("Double click to confirm selection\nor drag vertices to change selection")
        img_window.unbind('<ButtonRelease 1>')
        img_window.bind('<B1 Motion>', self.update)

    def update(self, mouse):
        iw_w = img_window.winfo_width()
        iw_h = img_window.winfo_height()

        for i, p_ in enumerate((self.p1, self.p2)):
            if dist(p_, (mouse.x, mouse.y)) < 20:
                p = [mouse.x, mouse.y]
                if p[0] < 0:
                    p[0] = 0
                elif p[0] > iw_w - 1:
                    p[0] = iw_w - 1

                if p[1] < 0:
                    p[1] = 0
                elif p[1] > iw_h - 1:
                    p[1] = iw_h - 1
                if i == 0:
                    self.p1 = p
                else:
                    self.p2 = p
                break
        self.draw()

    def end(self, mouse=None):
        img_window.unbind('<B1 Motion>')
        img_window.unbind('<ButtonRelease 1>')
        img_window.unbind('<Double Button 1>')
        img_window.delete(self.rect, self.c1, self.c2)
        self.command(area=valid(self.p1, self.p2))

    def draw(self):
        x1, y1 = self.p1
        x2, y2 = self.p2
        if self.rect is not None:
            img_window.delete(self.rect, self.c1, self.c2)

        if self.img is not None:
            x = (x1+x2)/2
            y = (y1+y2)/2
            w = abs(x1-x2)
            h = abs(y1-y2)
            # print(w, h)
            self.new_img = ImageTk.PhotoImage(self.img.resize((w, h)))
            self.rect = img_window.create_image(x, y, image=self.new_img)
        else:
            self.rect = img_window.create_rectangle(
                x1, y1, x2, y2, outline='white', width=3)
        self.c1 = img_window.create_oval(
            x1 - 5, y1 - 5, x1 + 5, y1 + 5, fill='black')
        self.c2 = img_window.create_oval(
            x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill='black')


def crop_img(area=None):
    if current_img is None:
        image_does_not_exist_msg()
        return
    if area is None:
        update_status("Drag mouse to select area")
        Selection(crop_img)
    else:
        cropped_img = current_img.crop(area)
        change_img(cropped_img)


def rotate_a_img():
    if current_img is None:
        image_does_not_exist_msg()
        return
    rotated_img = current_img.rotate(90, expand=1)
    change_img(rotated_img)


def rotate_c_img():
    if current_img is None:
        image_does_not_exist_msg()
        return
    rotated_img = current_img.rotate(-90, expand=1)
    change_img(rotated_img)


def flip_h_img():
    if current_img is None:
        image_does_not_exist_msg()
        return
    flipped_img = current_img.transpose(Image.FLIP_LEFT_RIGHT)
    change_img(flipped_img)


def flip_v_img():
    if current_img is None:
        image_does_not_exist_msg()
        return
    flipped_img = current_img.transpose(Image.FLIP_TOP_BOTTOM)
    change_img(flipped_img)


def copy(event=None, area=None):
    if current_img is None:
        image_does_not_exist_msg()
        return
    if area is None:
        update_status("Drag mouse to select area")
        Selection(cmd=copy)
    else:
        global clipboard_img
        clipboard_img = current_img.crop(area)
        update_status("Area copied to clipboard")


def paste(event=None, area=None):
    if clipboard_img is not None:
        if area is None:
            update_status("Drag mouse to paste image")
            Selection(cmd=paste, img=clipboard_img)
        else:
            x1, y1, x2, y2 = area
            w = int(abs(x1-x2))
            h = int(abs(y1-y2))

            new_img = current_img.copy()
            new_img.paste(clipboard_img.resize((w, h)), area)
            change_img(new_img)


def inverted_img(img): return ImageOps.invert(img)
def black_n_whited_img(img): return ImageEnhance.Color(img).enhance(0)


# effects addition
effects_list = {'None': NONE, 'Blur': BLUR, 'Contour': CONTOUR, 'Detail': DETAIL, 'Edge Enhance': EDGE_ENHANCE,
                'Edge Enhance More': EDGE_ENHANCE_MORE, 'Emboss': EMBOSS, 'Find Edges': FIND_EDGES,
                'Smooth': SMOOTH, 'Smooth More': SMOOTH_MORE, 'Sharpen': SHARPEN,
                'Max-Filter': MaxFilter(size=3), 'Min-Filter': MinFilter(size=3),
                'Black & White': black_n_whited_img, 'Invert': inverted_img}
effects_images = []
sample_img = Image.open("images/sample.jpg")


class SampleImage:
    def __init__(self, effect, row, column):
        self.effect = effect
        self.row = row
        self.column = column

    def show(self):
        global image
        image = sample_img.resize((150, 150))
        if self.effect in ['Black & White', 'Invert']:
            image = effects_list[self.effect](image)
        elif self.effect != 'None':
            image = image.filter(effects_list[self.effect])

        image = ImageTk.PhotoImage(image)
        effects_images.append(image)

        frame = Frame(effect_window, padx=10, pady=10, cursor='spraycan')
        frame.grid(row=self.row, column=self.column)
        img_label = Label(frame, image=image)
        img_label.pack()
        img_label.bind(
            '<Button 1>', func=lambda event: apply_effect(self.effect))
        Label(frame, text=self.effect).pack()


effect_window = None


def apply_effect(effect):
    effect_window.destroy()
    if effect == 'None':
        update_status("Closed effects window")
        return
    if effect in ['Black & White', 'Invert']:
        new_img = effects_list[effect](current_img)
    else:
        effect = effects_list[effect]
        new_img = current_img.filter(effect)
    change_img(new_img)


def effects():
    if current_img is None:
        image_does_not_exist_msg()
        return
    global effect_window
    if effect_window:
        effect_window.destroy()
    effect_window = Toplevel(img_window)
    effect_window.title("Effects")
    effect_window.resizable(0, 0)
    effect_window.focus()
    effects_images.clear()

    row = column = 0
    for eff in effects_list:
        SampleImage(eff, row, column).show()
        column += 1
        if column % 5 == 0:
            row += 1
            column = 0
    update_status("Choose any effect from window")


filtered_img = None
sliders = []

added_img = None


def add_img(area=None):
    if area is None:
        filename = select_path('open')
        if filename:
            global added_img
            added_img = Image.open(filename)
            if added_img is not None:
                update_status("Drag mouse to add image")
                Selection(cmd=add_img, img=added_img)
    else:
        x1, y1, x2, y2 = area
        w = int(abs(x1-x2))
        h = int(abs(y1-y2))

        new_img = current_img.copy()
        new_img.paste(added_img.resize((w, h)), area)
        change_img(new_img)


def pmap(x, x1, x2, y1, y2):
    m = (y1-y2)/(x1-x2)
    return m*(x - x1) + y1


def update_brightness(val):
    if current_img is None:
        image_does_not_exist_msg()
        for s in sliders:
            s.set(0)
        return
    val = float(val)
    if val > 0:
        val = pmap(val, 0, 50, 1, 3)
    else:
        val = pmap(val, -50, 0, 0, 1)
    global filtered_img
    if filtered_img is None:
        filtered_img = current_img
    filtered_img = ImageEnhance.Brightness(current_img)
    filtered_img = filtered_img.enhance(val)
    change_img(filtered_img, add_in_history=False, update=False)


def update_contrast(val):
    if current_img is None:
        image_does_not_exist_msg()
        for s in sliders:
            s.set(0)
        return
    val = float(val)
    if val > 0:
        val = pmap(val, 0, 50, 1, 3)
    else:
        val = pmap(val, -50, 0, 0.5, 1)

    global filtered_img
    if filtered_img is None:
        filtered_img = current_img
    filtered_img = ImageEnhance.Contrast(current_img)
    filtered_img = filtered_img.enhance(val)
    change_img(filtered_img, add_in_history=False, update=False)


def update_sharpness(val):
    if current_img is None:
        image_does_not_exist_msg()
        for s in sliders:
            s.set(0)
        return
    val = float(val)
    if val > 0:
        val = pmap(val, 0, 50, 1, 5)
    else:
        val = pmap(val, -50, 0, -1, 1)

    global filtered_img
    if filtered_img is None:
        filtered_img = current_img
    filtered_img = ImageEnhance.Sharpness(current_img)
    filtered_img = filtered_img.enhance(val)
    change_img(filtered_img, add_in_history=False, update=False)


def update_color(val):
    if current_img is None:
        image_does_not_exist_msg()
        for s in sliders:
            s.set(0)
        return
    val = pmap(float(val), -50, 50, 0, 2)
    global filtered_img
    if filtered_img is None:
        filtered_img = current_img
    filtered_img = ImageEnhance.Color(current_img)
    filtered_img = filtered_img.enhance(val)
    change_img(filtered_img, add_in_history=False, update=False)


def apply_enhance(event=None):
    global filtered_img
    change_img(filtered_img)
    filtered_img = None
    for s in sliders:
        s.set(0)


def resize():
    try:
        w = width.get()
        h = height.get()
        if var.get():
            h = int(w*current_img.size[1]/current_img.size[0])

        if w <= 0 or h <= 0 or w > 2048 or h > 2048:
            messagebox.showerror(title="Imagify",
                                 message="Please enter from 1 to 2048.")
            resize_window.focus()
        else:
            resize_window.destroy()
            if (w, h) != current_img.size:
                change_img(current_img.resize((w, h)))
    except:
        messagebox.showerror(title="Imagify",
                             message="Please enter valid input.")
        resize_window.focus()


var = width = height = None


def aspect_ratio(height_entry):
    try:
        if var.get():
            height_entry.configure(state=DISABLED)
            height.set(
                int(width.get()*current_img.size[1]/current_img.size[0]))
        else:
            height_entry.configure(state=NORMAL)
    except:
        pass


resize_window = None


def resize_img():
    if current_img is None:
        image_does_not_exist_msg()
        return

    global resize_window
    if resize_window:
        resize_window.destroy()

    resize_window = Toplevel(img_window)
    resize_window.title("Resize")
    resize_window.geometry("300x150")
    resize_window.resizable(0, 0)
    resize_window.focus()
    Label(resize_window, text="Width").grid(
        row=0, column=0, padx=10, pady=10)
    Label(resize_window, text="Height").grid(row=1, column=0, padx=10)
    i_w, i_h = current_img.size

    global var, width, height
    width = IntVar(value=i_w)
    height = IntVar(value=i_h)
    width_entry = Entry(resize_window, textvariable=width, width=10)
    width_entry.grid(
        row=0, column=1, padx=10, pady=10, sticky=W)
    height_entry = Entry(resize_window, textvariable=height, width=10)
    height_entry.grid(
        row=1, column=1, padx=10, pady=10, sticky=W)

    var = IntVar(value=0)
    Checkbutton(resize_window, text="Keep Aspect Ratio", variable=var, command=lambda: aspect_ratio(height_entry)).grid(
        row=2, column=0, padx=10, pady=10, sticky=W)

    width_entry.bind(
        '<KeyRelease>', func=lambda event: aspect_ratio(height_entry))
    Button(resize_window, text="OK", width=10,
           command=lambda: resize()).grid(row=2, column=1, padx=10, pady=10, sticky=W)
    update_status("Enter value of new size")


def undo(event=None):
    global current
    if current_img is None:
        image_does_not_exist_msg()
        return
    if current - 1 >= 0:
        current -= 1
        change_img(history_data[current], add_in_history=False)


def redo(event=None):
    global current
    if current_img is None:
        image_does_not_exist_msg()
        return
    if current + 1 < len(history_data):
        current += 1
        change_img(history_data[current], add_in_history=False)


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
    ans= "no"
    if len(history_data) > 1:
        ans = want_to_save_msg()
        
    if ans is not None:
        filename = select_path('open')
        if filename:
            img = Image.open(filename)
            if img:
                global current
                history_data.clear()
                current = -1
                change_img(img)
                update_status("Opened successfully")


def save_img(event=None):
    if current_img is None:
        image_does_not_exist_msg()
        return
    path = select_path('save')
    if path:
        current_img.save(path)
        update_status("Saved successfully")


def quit(parent):
    if len(history_data) > 1:
        ans = want_to_save_msg()
        if ans == False:
            parent.destroy()
    elif messagebox.askokcancel("Imagify", "Do you want to quit?", icon='warning'):
        parent.destroy()


def about(event=None):
    messagebox.showinfo(
        title="Imagify", message="Imagify", detail="Version: 1.0.1\nProduct of Jam-Burger\nDeveloped by Jay")

def want_to_save_msg():
    ans = messagebox.askyesnocancel(
            "Imagify", "Do you want to save your changes?", icon='warning')
    if ans == True:
        save_img()
    return ans

def image_does_not_exist_msg():
    messagebox.showerror(title="Imagify",
                         message="Please add an image first.")
