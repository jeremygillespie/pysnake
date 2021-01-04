import tkinter as tk
from graph import Graph, Point


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Snake')
        self.root.protocol('WM_DELETE_WINDOW', self.on_quit)

        self.running = True

        self.board = Board()

        self.graph = Graph(20, 10)
        self.graph.occupied[0, 0] = 1
        self.graph.occupied[0, 1] = 2
        self.graph.occupied[1, 1] = 3

        self.update_board()

        self.root.mainloop()

    def on_quit(self):
        self.running = False
        self.root.destroy()

    def update_board(self):
        self.board.show(self.graph)
        if self.running:
            self.root.after(1000, self.update_board)


class Board(tk.Canvas):
    def __init__(self):
        super().__init__(width=100, height=100, bg='black')
        self.pack()

        self.vert_size = 30
        self.vert_padding = 10

    def show(self, graph):
        self.delete(all)

        self.config(width=self.vert_size * graph.width + self.vert_padding,
                    height=self.vert_size * graph.height + self.vert_padding)

        for x in range(graph.width):
            for y in range(graph.height):
                point = Point(x, graph.height - 1 - y)
                if graph.occupied[point] > 0:
                    x0 = x*self.vert_size + self.vert_padding
                    y0 = y*self.vert_size + self.vert_padding
                    x1 = x0+self.vert_size - self.vert_padding
                    y1 = y0+self.vert_size - self.vert_padding
                    self.create_rectangle(
                        x0, y0, x1, y1, fill='green', outline='')

                    off = graph.outgoing(point)
                    if off:
                        x0 += off.dx * 0.5 * self.vert_size
                        x1 += off.dx * 0.5 * self.vert_size
                        y0 -= off.dy * 0.5 * self.vert_size
                        y1 -= off.dy * 0.5 * self.vert_size
                        self.create_rectangle(
                            x0, y0, x1, y1, fill='green', outline='')


if __name__ == '__main__':
    app = App()
