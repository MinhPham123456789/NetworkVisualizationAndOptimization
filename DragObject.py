from tkinter import *
from igraph import *
from ZoomAndDrag import *
from ObjectTk.ObjectManager import *

class MouseMover():
    def __init__(self, tk_frame: ZoomAndDrag, DrawTkinter_center, graph:Graph, mg: ObjManager):
        self.item = 0
        self.previous = (0, 0)
        self.canvas = tk_frame.canvas
        self.reverse_position_key = DrawTkinter_center
        self.graph = graph
        self.tk_frame = tk_frame
        self.mg = mg
        self.last_pos = []
        self.new_pos = []

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
        self.last_pos = self.canvas.coords(self.item)
        print(self.canvas.coords(self.item))



    def drag(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        yc = widget.canvasx(event.y)
        index = self.item[0]-1
        # current_size = math.sqrt((self.last_pos[0] - self.last_pos[2])**2 + (self.last_pos[1] - self.last_pos[3])**2)
        # x1 = xc - current_size/2
        # y1 = yc - current_size/2
        # x2 = xc + current_size/2
        # y2 = yc + current_size/2
        # self.canvas.coords(self.item, x1, y1, x2, y2)
        self.canvas.move(self.item, xc - self.previous[0], yc - self.previous[1])
        print("Bis:")
        print((xc, yc, self.item[0]))
        print(self.canvas.coords(self.item))
        self.previous = (xc, yc)
        self.change_position_instantly()

    def change_position_instantly(self):
        items = self.canvas.find_withtag("all")
        for item in items:
            x1, y1, x2, y2 = self.canvas.coords(item)
            self.canvas.coords(item, x1, y1, x2, y2)
        print("test")

##Storage#############
    #select
        # print(self.tk_frame.revert_scale(self.canvas.coords(self.item)[0], self.canvas.coords(self.item)[1]))
        # print(self.tk_frame.revert_scale(self.canvas.coords(self.item)[2], self.canvas.coords(self.item)[3]))
        # test_1 = self.tk_frame.revert_scale(self.canvas.coords(self.item)[0], self.canvas.coords(self.item)[1])
        # test_2 = self.tk_frame.revert_scale(self.canvas.coords(self.item)[2], self.canvas.coords(self.item)[3])
        # print((test_1[0] + test_2[0]) / 2, (test_1[1] + test_2[1]) / 2)

        # print(self.mg.vertex[self.item[0] - 1])

    #drag
        # self.new_pos = (xc, yc)
        # newx, newy = self.tk_frame.revert_scale(self.new_pos[0], self.new_pos[1])
        # print(newx,newy)
        # self.mg.vertex[self.item[0] - 1].set_attribute("x", newx-300-0.06)
        # self.mg.vertex[self.item[0] - 1].set_attribute("y", newy-300-0.06)

        # vector = [self.new_pos[0] - self.last_pos[0], self.new_pos[1] - self.last_pos[1]]
        # old_x = self.mg.vertex[self.item[0] - 1].get_attribute("x")
        # old_y = self.mg.vertex[self.item[0] - 1].get_attribute("y")
        # s_vectorx, s_vectory = self.tk_frame.revert_scale(vector[0], vector[1])
        # self.mg.vertex[self.item[0] - 1].set_attribute("x", old_x + s_vectorx)
        # self.mg.vertex[self.item[0] - 1].set_attribute("y", old_y + s_vectory)

        # if int(self.item[0])-1 < len(self.graph.vs):
        #     new_x = xc - self.reverse_position_key - self.graph.vs[self.item[0]-1]["vertex_size"]
        #     new_y = yc - self.reverse_position_key - self.graph.vs[self.item[0]-1]["vertex_size"]