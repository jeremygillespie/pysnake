from tkinter import *


class App(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        self.entry = Entry()
        self.entry.pack()

        self.contents = StringVar()
        self.contents.set("")
        self.entry["textvar"] = self.contents

        self.entry.bind('<Key-Return>', self.output)

    def output(self, event):
        print(self.contents.get())
        self.contents.set("")


def initialize():
    root = Tk()
    app = App(root)
    app.mainloop()
