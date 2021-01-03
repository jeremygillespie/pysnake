import tkinter as tk


def initialize():
    root = tk.Tk()
    app = App(root)
    app.mainloop()


class App(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        self.display = Display(parent)


class Display(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        self.canvas = tk.Canvas(width=900, height=600)
        self.canvas.pack()
