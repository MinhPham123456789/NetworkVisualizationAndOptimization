from tkinter import *
from igraph import *

from ObjectTk import ObjectTkinter
from ZoomAndDrag import *
from ObjectTk.ObjectManager import *
from ObjectTk.ObjectDrawTkinter import *


class MouseMover():
    def __init__(self, tk_frame: Frame, drawTk: ObjDrawTkinter, graph: Graph, mg: ObjManager, gui_support):
        self.item = (0)
        self.previous = (0, 0)
        self.canvas = tk_frame.canvas
        self.drawTk = drawTk
        self.reverse_position_key = drawTk.get_moved_center()
        self.graph = graph
        self.tk_frame = tk_frame
        self.mg = mg
        self.gui_support = gui_support
        self.last_pos = []
        self.new_pos = []

    def select(self, event):
        widget = event.widget  # Get handle to canvas
        # Convert screen coordinates to canvas coordinates
        xc = widget.canvasx(event.x)
        yc = widget.canvasx(event.y)
        # self.item = widget.find_closest(xc, yc)[0]  # ID for closest
        self.item = self.canvas.find_withtag(
            CURRENT)  # Better than closest only move object when you click the right one
        self.previous = (xc, yc)
        print("Von:")
        print((xc, yc, self.item))
        self.last_pos = self.canvas.coords(self.item)
        if len(self.item) > 0 and isinstance(self.drawTk.items_table.inverse[self.item[0]], ObjectTkinter.VertexObj):
            self.gui_support.get_vertex_value(self.item[0])
            self.gui_support.is_vertex = True
        elif isinstance(self.drawTk.items_table.inverse[self.item[0]], ObjectTkinter.EdgeObj):
            self.gui_support.get_edge_value(self.item[0])
            self.gui_support.is_vertex = False
        # self.drawTk.set_weight_text_position(
        #     int(self.drawTk.items_table.inverse[self.item[0]].get_attribute("id")[1:]), "service_load", self.mg)
        # vertex_obj = self.drawTk.items_table.inverse[self.item[0]]
        # vertex_obj_index = int(vertex_obj.get_attribute("id")[1:])  # [1:] because id more than 1 digit
        # rectangle_index = "r" + str(vertex_obj_index)
        # print(self.canvas.coords(self.item))

    def drag(self, event):
        widget = event.widget
        xc = widget.canvasx(event.x)
        yc = widget.canvasx(event.y)
        # print(len(self.item))
        if len(self.item) >= 1 and self.item[0] <= len(self.mg.vertex):
            self.canvas.move(self.item, xc - self.previous[0], yc - self.previous[1])
            print("Bis:")
            print((xc, yc, self.item[0]))
            print(self.canvas.coords(self.item))

            self.previous = (xc, yc)
            self.change_position_instantly2()

    def change_position_instantly(self):
        source_list = []
        target_list = []
        xs, ys, xt, yt = self.canvas.coords(self.item)
        x = (xs + xt) / 2
        y = (ys + yt) / 2
        vertex_item_index = self.item[0] - 1
        # print("vertex item:", vertex_item_index)
        for index in range(len(self.mg.edge)):
            if self.mg.edge[index].get_attribute("source") == vertex_item_index:
                source_list.append(index)
        for index in range(len(self.mg.edge)):
            if self.mg.edge[index].get_attribute("target") == vertex_item_index:
                target_list.append(index)
        for i in source_list:
            edge_item_index = i + 1 + len(
                self.mg.vertex)  # In item index, it starts from 1 and it adds all vertices then all edges
            # print("sedge:", edge_item_index)
            x1, y1, x2, y2 = self.canvas.coords(edge_item_index)
            self.canvas.coords(edge_item_index, x, y, x2, y2)
        for u in target_list:
            edge_item_index = u + 1 + len(
                self.mg.vertex)  # In item index, it starts from 1 and it adds all vertices then all edges
            # print("tedge:", edge_item_index)
            x1, y1, x2, y2 = self.canvas.coords(edge_item_index)
            self.canvas.coords(edge_item_index, x1, y1, x, y)
        items = self.canvas.find_withtag("all")
        # print(len(items))
        # print(len(self.mg.vertex))
        # print(len(self.mg.edge))
        # print(source_list)
        # print(target_list)
        # for item in items:
        #     x1, y1, x2, y2 = self.canvas.coords(item)
        #     self.canvas.coords(item, x, y, x2, y2)
        # print("test")

    def change_position_instantly2(self):  # Use the new bidict
        source_list = []
        target_list = []
        xs, ys, xt, yt = self.canvas.coords(self.item)
        x = (xs + xt) / 2
        y = (ys + yt) / 2
        print("item:", self.item[0])
        vertex_obj = self.drawTk.items_table.inverse[self.item[0]]
        # print("vertex item:", vertex_obj)
        # print("verify:", self.mg.vertex[self.item[0] - 1])
        try:
            vertex_obj_index = int(vertex_obj.get_attribute("id")[1:])  # [1:] because id more than 1 digit
        except TypeError:
            vertex_obj_index = int(vertex_obj.get_attribute("id"))
        print("vertex item:", vertex_obj_index)
        for edge in self.mg.edge:
            if edge.get_attribute("source") == vertex_obj_index:
                source_list.append(edge)
        for edge in self.mg.edge:
            if edge.get_attribute("target") == vertex_obj_index:
                target_list.append(edge)
        for i in source_list:
            edge_item_index = self.drawTk.items_table[i]  # In item index, it starts from 1
            # and it adds vertices then edges
            print("sedge:", edge_item_index)
            x1, y1, x2, y2 = self.canvas.coords(edge_item_index)
            self.canvas.coords(edge_item_index, x, y, x2, y2)
        for u in target_list:
            edge_item_index = self.drawTk.items_table[u]  # In item index, it starts from 1
            # and it adds vertices then edges
            print("tedge:", edge_item_index)
            x1, y1, x2, y2 = self.canvas.coords(edge_item_index)
            self.canvas.coords(edge_item_index, x1, y1, x, y)
        if self.drawTk.rectangle_switch:
            rectangle_index = "r" + str(vertex_obj_index)
            position = self.drawTk.set_weight_text_position(vertex_obj_index, self.mg)
            self.canvas.coords(self.drawTk.items_table[rectangle_index], position)
        items = self.canvas.find_withtag("all")
        # print(len(items))
        # print(len(self.mg.vertex))
        # print(len(self.mg.edge))
        # print(source_list)
        # print(target_list)
        print("test")


##Storage#############
# select
# print(self.tk_frame.revert_scale(self.canvas.coords(self.item)[0], self.canvas.coords(self.item)[1]))
# print(self.tk_frame.revert_scale(self.canvas.coords(self.item)[2], self.canvas.coords(self.item)[3]))
# test_1 = self.tk_frame.revert_scale(self.canvas.coords(self.item)[0], self.canvas.coords(self.item)[1])
# test_2 = self.tk_frame.revert_scale(self.canvas.coords(self.item)[2], self.canvas.coords(self.item)[3])
# print((test_1[0] + test_2[0]) / 2, (test_1[1] + test_2[1]) / 2)

# print(self.mg.vertex[self.item[0] - 1])



