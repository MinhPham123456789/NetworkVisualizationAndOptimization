from igraph import *
from ObjectTk.ObjectManager import *
from ObjectTk.ObjectDrawTkinter import *
import tkinter as tk
from ZoomAndDrag import *
from igraphNewModules import *
from DragObject import *
from ObjectTk.ObjTkFrame import *
from ObjectTk.ObjTkLayout import GraphLayout
from GUI_support import *
import numpy as np


class Window(Frame):
    def __init__(self, master):  # canvas_frame, drawTk: ObjDrawTkinter, mg: ObjManager, layout_class: GraphLayout, master=None):
        Frame.__init__(self, master)
        self.gui_frame = tk.Frame(self.master)
        self.frame = tk.Frame(self.master)
        self.master = master
        self.init_window()
        # self.canvas = canvas_frame.canvas
        # self.drawTk = drawTk
        # self.mg = mg
        # self.layout = layout_class
        self.gui_support = GUI_support(self)

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill="both", expand=1)
        self.gui_frame.canvas = tk.Canvas(self, width=900, height=0, background="white")
        self.gui_frame.canvas.pack()
        menu = Menu(self.master)
        self.master.config(menu=menu)
        File = Menu(menu)
        Edit = Menu(menu)
        Layout_menu = Menu(menu)
        File.add_command(label="save", command=lambda: self.gui_support.save())
        File.add_command(label="load", command=lambda: self.gui_support.load())
        File.add_command(label="refresh")

        Edit.add_command(label="group_vertex", command=lambda: self.popup_group_vertex())
        Edit.add_command(label="bandwidth", command=lambda: self.Bandwidth())
        Edit.add_command(label="delay")  # , command = self.Delay)

        Layout_menu.add_command(label="original layout",
                                command=lambda: self.gui_support.start_graph())
        Layout_menu.add_command(label="reingold tilford circular",
                                command=lambda: self.gui_support.reingold_tilford_circular())

        menu.add_cascade(label="File", menu=File)
        menu.add_cascade(label="Edit", menu=Edit)
        menu.add_cascade(label="Layout", menu=Layout_menu)

    def popup_group_vertex(self):
        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Window")
        input_name = tk.Label(popupBonusWindow, text="Attribute")
        input_name.grid(row=0)
        input_entry = tk.Entry(popupBonusWindow)
        input_entry.grid(row=0, column=1)
        B1 = tk.Button(popupBonusWindow, text="Okay", command=lambda: self.gui_support.Groupvertex(input_entry.get()))
        B1.grid(row=0, column=2)


    # def Groupvertex(self):
    #     color_list = self.drawTk.group_vertex_color("GeoLocation", self.mg)
    #     for i in range(len(color_list)):
    #         self.canvas.itemconfigure(self.drawTk.items_table[self.mg.vertex[i]], fill=color_list[i])
    #     # self.canvas_frame.canvas.create_oval(0, 0, 100, 100)
    #
    # # def Bandwidth(self, c):
    # #     c.create_oval(150, 150, 200, 200)
    #
    # def reingold_tilford_circular(self):
    #     coords = self.layout.reingold_tilford_circular_layout()
    #     for i in range(len(coords)):
    #         self.change_position_instantly2(coords[i], self.drawTk.items_table.inverse[i+1])

    # def change_position_instantly2(self, new_coord, vertex_obj):  # Use the new bidict
    #     source_list = []
    #     target_list = []
    #     center = self.drawTk.get_moved_center()
    #     vertex_item_index = self.drawTk.items_table[vertex_obj]
    #     xs, ys, xt, yt = self.canvas.coords(vertex_item_index)
    #     old_width_len = 0.03
    #     old_height_len = 0.03
    #     x = (xs + xt) / 2
    #     y = (ys + yt) / 2
    #     x = new_coord[0] + center
    #     y = new_coord[1] + center
    #     # print("item:", self.item[0])
    #     # vertex_obj = self.drawTk.items_table.inverse[self.item[0]]
    #     # print("vertex item:", vertex_obj)
    #     # print("verify:", self.mg.vertex[self.item[0] - 1])
    #     vertex_obj_index = int(vertex_obj.get_attribute("id")[1:])  # [1:] because id more than 1 digit
    #     print("vertex item:", vertex_obj_index)
    #     for edge in self.mg.edge:
    #         if edge.get_attribute("source") == vertex_obj_index:
    #             source_list.append(edge)
    #     for edge in self.mg.edge:
    #         if edge.get_attribute("target") == vertex_obj_index:
    #             target_list.append(edge)
    #     for i in source_list:
    #         edge_item_index = self.drawTk.items_table[i]  # In item index, it starts from 1
    #         # and it adds vertices then edges
    #         print("sedge:", edge_item_index)
    #         x1, y1, x2, y2 = self.canvas.coords(edge_item_index)
    #         self.canvas.coords(edge_item_index, x, y, x2, y2)
    #     for u in target_list:
    #         edge_item_index = self.drawTk.items_table[u]  # In item index, it starts from 1
    #         # and it adds vertices then edges
    #         print("tedge:", edge_item_index)
    #         x1, y1, x2, y2 = self.canvas.coords(edge_item_index)
    #         self.canvas.coords(edge_item_index, x1, y1, x, y)
    #     vx1 = x - old_width_len
    #     vy1 = y - old_height_len
    #     vx2 = x + old_width_len
    #     vy2 = y + old_height_len
    #     self.canvas.coords(vertex_item_index, vx1, vy1, vx2, vy2)
    #     if self.drawTk.rectangle_switch:
    #         rectangle_index = "r" + str(vertex_obj_index)
    #         position = self.drawTk.set_weight_text_position(vertex_obj_index, "service_load", self.mg)
    #         self.canvas.coords(self.drawTk.items_table[rectangle_index], position)
    #     items = self.canvas.find_withtag("all")
    #     # print(len(items))
    #     # print(len(self.mg.vertex))
    #     # print(len(self.mg.edge))
    #     # print(source_list)
    #     # print(target_list)
    #     print("test")

# def Delay(self):
# t = Toplevel(height=1200, width=1300)
# t.title("pop-up")
# exit_button = Button(t, text="exit", command=t.destroy)
# exit_button.place(x=0, y=0)
# canvas1 = Canvas(t, heigh=1200, width=1200)
# canvas1.place(x=100, y=0)
