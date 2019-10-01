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
import tk_tools as tkt
import numpy as np
import GeoPage

class Window(Frame):
    def __init__(self,
                 master):  # canvas_frame, drawTk: ObjDrawTkinter, mg: ObjManager, layout_class: GraphLayout, master=None):
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
        Throughput = Menu(menu)

        File.add_command(label="open", command=lambda: self.gui_support.open())
        File.add_command(label="save", command=lambda: self.gui_support.save())
        File.add_command(label="refresh")

        Edit.add_command(label="group_vertex_by_color", command=lambda: self.popup_group_vertex())
        Edit.add_command(label="group_edge_by_width", command=lambda: self.popup_group_edge_width())
        Edit.add_command(label="group_edge_by_color", command=lambda: self.popup_group_edge_color())

        Layout_menu.add_command(label="original layout",
                                command=lambda: self.gui_support.start_graph())
        Layout_menu.add_command(label="reingold tilford circular",
                                command=lambda: self.gui_support.reingold_tilford_circular())

        Throughput.add_command(label="Throughput", command=lambda: self.popup_throughput())

        menu.add_cascade(label="File", menu=File)
        menu.add_cascade(label="Edit", menu=Edit)
        menu.add_cascade(label="Layout", menu=Layout_menu)
        menu.add_cascade(label="Throughput", menu=Throughput)
        menu.add_command(label="GeoWindow", command=lambda: self.popup_geo_window())

        # VERTEX x=0, y=0###############################################3

        vertex_information = Label(self, text="Vertex")
        id_node = Label(self, text="ID")
        country_node = Label(self, text="Geolocation")
        network = Label(self, text="Network")
        label_node = Label(self, text="Label")
        asn = Label(self, text="ASN")
        service_load = Label(self, text="Service load")

        self.idnode_entry = Entry(self)
        self.countrynode_entry = Entry(self)
        self.network_entry = Entry(self)
        self.label_node_entry = Entry(self)
        self.asn_entry = Entry(self)
        self.serviceload_entry = Entry(self)

        self.idnode_entry.insert(0, "default value")
        self.countrynode_entry.insert(0, "default value")
        self.network_entry.insert(0, "default value")
        self.label_node_entry.insert(0, "default value")
        self.asn_entry.insert(0, "default value")
        self.serviceload_entry.insert(0, "default value")

        vertex_information.place(x=0, y=0)
        id_node.place(x=0, y=30)
        country_node.place(x=0, y=60)
        network.place(x=0, y=90)
        label_node.place(x=0, y=120)
        asn.place(x=0, y=150)
        service_load.place(x=0, y=180)

        self.idnode_entry.place(x=100, y=30)
        self.countrynode_entry.place(x=100, y=60)
        self.network_entry.place(x=100, y=90)
        self.label_node_entry.place(x=100, y=120)
        self.asn_entry.place(x=100, y=150)
        self.serviceload_entry.place(x=100, y=180)

        vertex_apply = Button(self, text="Apply change", command=lambda: self.gui_support.set_vertex_value())
        vertex_apply.place(x=60, y=210)
        # x=0, y=210##############################################

        # EDGE x = 0, y = 240 ###################################
        edge_infomation = Label(self, text="Edge")
        link_type = Label(self, text="LinkType")
        link_node = Label(self, text="LinkNode")
        link_label = Label(self, text="LinkLabel")
        link_speed_raw = Label(self, text="LinkSpeedRaw")
        buffer_delay = Label(self, text="BufferDelay")
        transmission_delay = Label(self, text="TransDelay")
        propagation_delay = Label(self, text="PropDelay")

        self.link_type_entry = Entry(self)
        self.link_note_entry = Entry(self)
        self.link_label_entry = Entry(self)
        self.link_speed_raw_entry = Entry(self)
        self.buffer_delay_entry = Entry(self)
        self.transmission_delay_entry = Entry(self)
        self.propagation_delay_entry = Entry(self)

        self.link_type_entry.insert(0, "default value")
        self.link_note_entry.insert(0, "default value")
        self.link_label_entry.insert(0, "default value")
        self.link_speed_raw_entry.insert(0, "default value")
        self.buffer_delay_entry.insert(0, "default value")
        self.transmission_delay_entry.insert(0, "default value")
        self.propagation_delay_entry.insert(0, "default value")

        edge_infomation.place(x=0, y=240)
        link_type.place(x=0, y=270)
        link_node.place(x=0, y=300)
        link_label.place(x=0, y=330)
        link_speed_raw.place(x=0, y=360)
        buffer_delay.place(x=0, y=390)
        transmission_delay.place(x=0, y=420)
        propagation_delay.place(x=0, y=450)

        self.link_type_entry.place(x=100, y=270)
        self.link_note_entry.place(x=100, y=300)
        self.link_label_entry.place(x=100, y=330)
        self.link_speed_raw_entry.place(x=100, y=360)
        self.buffer_delay_entry.place(x=100, y=390)
        self.transmission_delay_entry.place(x=100, y=420)
        self.propagation_delay_entry.place(x=100, y=450)

        edge_apply = Button(self, text="Apply change", command=lambda: self.gui_support.set_edge_value())
        edge_apply.place(x=60, y=480)

        # x=0, y=420 ##############################

    def popup_group_vertex(self):
        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Vertex color")
        input_name = tk.Label(popupBonusWindow, text="Attribute")
        input_name.grid(row=0)
        input_entry = tk.Entry(popupBonusWindow)
        input_entry.grid(row=0, column=1)
        B1 = tk.Button(popupBonusWindow, text="Okay", command=lambda: self.gui_support.group_vertex(input_entry.get()))
        B1.grid(row=0, column=2)

    def get_vertex_value(self, list_value):
        self.idnode_entry.delete(0, "end")
        self.countrynode_entry.delete(0, "end")
        self.network_entry.delete(0, "end")
        self.label_node_entry.delete(0, "end")
        self.asn_entry.delete(0, "end")
        self.serviceload_entry.delete(0, "end")

        self.idnode_entry.insert(0, list_value[0])
        self.countrynode_entry.insert(0, list_value[1])
        self.network_entry.insert(0, list_value[2])
        self.label_node_entry.insert(0, list_value[3])
        self.asn_entry.insert(0, list_value[4])
        self.serviceload_entry.insert(0, list_value[5])

    ##new##
    def get_edge_value(self, list_value):
        self.link_type_entry.delete(0, "end")
        self.link_note_entry.delete(0, "end")
        self.link_label_entry.delete(0, "end")
        self.link_speed_raw_entry.delete(0, "end")
        self.buffer_delay_entry.delete(0, "end")
        self.transmission_delay_entry.delete(0, "end")
        self.propagation_delay_entry.delete(0, "end")

        self.link_type_entry.insert(0, list_value[0])
        self.link_note_entry.insert(0, list_value[1])
        self.link_label_entry.insert(0, list_value[2])
        self.link_speed_raw_entry.insert(0, list_value[3])
        self.buffer_delay_entry.insert(0, list_value[4])
        self.transmission_delay_entry.insert(0, list_value[5])
        self.propagation_delay_entry.insert(0, list_value[6])

    def popup_group_edge_width(self):
        popup_bonus_window = Tk()
        popup_bonus_window.wm_title("Edge width")
        input_name = Label(popup_bonus_window, text="Attribute")
        input_name.grid(row=0)
        input_entry = Entry(popup_bonus_window)
        input_entry.grid(row=0, column=1)
        B1 = Button(popup_bonus_window, text="Okay", command=lambda: self.gui_support.edge_width(input_entry.get()))
        B1.grid(row=0, column=2)

    def popup_group_edge_color(self):
        print("into func. self.Delay")
        popup_window = tk.Tk()
        popup_window.wm_title("Edge color")
        input_name = tk.Label(popup_window, text="Attribute")
        input_name.grid(row=0)
        inputentry = tk.Entry(popup_window)
        inputentry.grid(row=0, column=1)
        Btn = tk.Button(popup_window, text="Okay", command=lambda: self.gui_support.edge_color(inputentry.get()))
        Btn.grid(row=0, column=2)

    def get_throughput_name(self, value):
        self.gui_support.throughput = value

    def popup_throughput(self):
        popup_bonus_window = Tk()
        popup_bonus_window.wm_title("Throughput window")
        input_name = Label(popup_bonus_window, text="Throughput file")
        input_name.grid(row=0)
        input_entry = Entry(popup_bonus_window)
        input_entry.grid(row=0, column=1)
        B1 = Button(popup_bonus_window, text="Browse",
                    command=lambda: [input_entry.delete(0, "end"),
                                     self.get_throughput_name(self.gui_support.open_throughput()),
                                     input_entry.insert(0, self.gui_support.throughput)])
        B1.grid(row=0, column=2)
        # TODO: Consider set range based on the range of the csv input
        spin_box_1 = tk.Spinbox(popup_bonus_window, from_=0, to=23, width=18,
                                command=lambda: self.gui_support.get_throughput_time(spin_box_1.get(),
                                                                                     self.gui_support.throughput))
        spin_box_1.grid(row=1, column=1)

    def popup_geo_window(self):
        window = Toplevel(self.master)
        window.wm_title("Geo Window")
        frame = tk.Frame(window)
        frame.pack(side="top", fill="both", expand=True)
        GeoPage.GeoPage(frame, window, self.gui_support.graph_path)



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
