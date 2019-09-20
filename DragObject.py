from tkinter import *
from igraph import *

class MouseMover():
    def __init__(self, canvas:Canvas, DrawTkinter_center, graph:Graph):
        self.item = 0
        self.previous = (0, 0)
        self.canvas = canvas
        self.reverse_position_key = DrawTkinter_center
        self.graph = graph

    def select(self, event):
        widget = event.widget  # Get handle to canvas
        # Convert screen coordinates to canvas coordinates
        xc = widget.canvasx(event.x)
        yc = widget.canvasx(event.y)
        # self.item = widget.find_closest(xc, yc)[0]  # ID for closest
        self.item = self.canvas.find_withtag(CURRENT)  # Better than closest only move object when you click the right one
        self.previous = (xc, yc)
        print("Von:")
        print((xc, yc, self.item))

    def drag(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        yc = widget.canvasx(event.y)
        self.canvas.move(self.item, xc - self.previous[0], yc - self.previous[1])
        print("Bis:")
        print((xc, yc, self.item[0]))
        self.previous = (xc, yc)
        if int(self.item[0])-1 < len(self.graph.vs):
            new_x = xc - self.reverse_position_key - self.graph.vs[self.item[0]-1]["vertex_size"]
            new_y = yc - self.reverse_position_key - self.graph.vs[self.item[0]-1]["vertex_size"]
            self.graph.vs[self.item[0]-1]["x"] = new_x
            self.graph.vs[self.item[0]-1]["y"] = new_y