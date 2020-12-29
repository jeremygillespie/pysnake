import tkinter as tk


class App(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        self.entry = tk.Entry()
        self.entry.pack()

        self.contents = tk.StringVar()
        self.contents.set("")
        self.entry["textvar"] = self.contents

        self.entry.bind('<Key-Return>', self.output)

    def output(self, event):
        print(self.contents.get())
        self.contents.set("")


def initialize():
    root = tk.Tk()
    app = App(root)
    app.mainloop()
