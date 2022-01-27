from tkinter import *
from functions import sliders
color_1 = "#041a3d"
color_2 = "#fff3b8"


class LabeledButton:
    def __init__(self, master, row, column, image, text, command):
        frame = Frame(master, bg=color_1)
        frame.grid(row=row, column=column)
        btn = Label(frame, image=image, cursor="circle")
        btn.bind('<Button 1>', func=lambda event: command())
        btn.pack(padx=30)
        Label(frame, text=text).pack()
        for w in frame.winfo_children():
            w.configure(font=('Consolas', 11), bg=color_1, fg=color_2)


class DoubleLabledButton:
    def __init__(self, master, row, column, text, data1, data2):
        frame = Frame(master, bg=color_1)
        frame.grid(row=row, column=column, columnspan=2)
        for i in range(2):
            frame.columnconfigure(i, weight=1)
        btn1 = Label(frame, image=data1[0], cursor="circle")
        btn1.bind('<Button 1>', func=lambda event: data1[1]())
        btn1.grid(row=0, column=0, padx=30)

        btn2 = Label(frame, image=data2[0], cursor="circle")
        btn2.bind('<Button 1>', func=lambda event: data2[1]())
        btn2.grid(row=0, column=1, padx=30)

        Label(frame, text=text).grid(row=1, column=0, columnspan=2)
        for w in frame.winfo_children():
            w.configure(font=('Consolas', 11), bg=color_1, fg=color_2)


class Slider:
    def __init__(self, master, row, length, label, update_command, release_command):
        self.scale = Scale(master, label=label, command=update_command, orient=HORIZONTAL, from_=-50, to=50,
                showvalue=False, length=length, font=('Consolas', 11), bg=color_1, fg=color_2)
        self.scale.grid(row=row, column=0, pady=(20, 0), columnspan=4)
        self.scale.bind('<ButtonRelease 1>', release_command)
        sliders.append(self.scale)

class Line:
    def __init__(self, master, row):
        Label(master, text = "-"*50, font = ('Consolas', 11), bg = color_1,
              fg = color_2).grid(row = row, column = 0, columnspan = 4)
