import pandas as pd
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
from MapLocate import *
import numpy as np
import GeoPage


class Window(Frame):
    def __init__(self, master):
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
        Vertex_highlight = Menu(menu)
        Edge_highlight = Menu(menu)
        Layout_menu = Menu(menu)
        Throughput = Menu(menu)
        Search = Menu(menu)

        File.add_command(label="open", command=lambda: self.gui_support.open())
        File.add_command(label="save", command=lambda: self.gui_support.save())
        File.add_command(label="refresh")

        Vertex_highlight.add_command(label="group_vertex_by_color", command=lambda: self.popup_group_vertex())
        Vertex_highlight.add_command(label="vertex_text_box", command=lambda: self.popup_vertex_text())
        Vertex_highlight.add_command(label="vertex_size", command=lambda: self.popup_vertex_size())

        Edge_highlight.add_command(label="group_edge_by_width", command=lambda: self.popup_group_edge_width())
        Edge_highlight.add_command(label="group_edge_by_color", command=lambda: self.popup_group_edge_color())

        Layout_menu.add_command(label="original layout",
                                command=lambda: self.gui_support.start_graph())
        Layout_menu.add_command(label="reingold tilford circular",
                                command=lambda: self.gui_support.reingold_tilford_circular())

        Throughput.add_command(label="Throughput", command=lambda: self.popup_throughput())

        Search.add_command(label="Vertex", command= lambda: self.popup_search_vertex())

        menu.add_cascade(label="File", menu=File)
        menu.add_cascade(label="Vertex Highlight", menu=Vertex_highlight)
        menu.add_cascade(label="Edge Highlight", menu=Edge_highlight)
        menu.add_cascade(label="Layout", menu=Layout_menu)
        menu.add_cascade(label="Throughput", menu=Throughput)
        menu.add_cascade(label="Search", menu=Search)
        menu.add_command(label="GeoWindow", command=lambda: self.popup_geo_window())
        menu.add_command(label="Statistics", command=lambda: self.popup_statistic())

        # VERTEX x=0, y=0###############################################3

        vertex_information = Label(self, text="Vertex", font="Helvetica 16 bold")
        id_node = Label(self, text="ID")
        country_node = Label(self, text="Geolocation")
        network = Label(self, text="Network")
        label_node = Label(self, text="Label")
        asn = Label(self, text="ASN")
        service_load = Label(self, text="Internal")
        longitude = Label(self, text="Longitude")
        latitude = Label(self, text="Latitude")

        self.idnode_entry = Entry(self)
        self.countrynode_entry = Entry(self)
        self.network_entry = Entry(self)
        self.label_node_entry = Entry(self)
        self.asn_entry = Entry(self)
        self.serviceload_entry = Entry(self)
        self.longitude_entry = Entry(self)
        self.latitude_entry = Entry(self)

        self.idnode_entry.insert(0, "")
        self.countrynode_entry.insert(0, "")
        self.network_entry.insert(0, "")
        self.label_node_entry.insert(0, "")
        self.asn_entry.insert(0, "")
        self.serviceload_entry.insert(0, "")
        self.longitude_entry.insert(0, "")
        self.latitude_entry.insert(0, "")

        vertex_information.place(x=90, y=0)
        id_node.place(x=0, y=30)
        country_node.place(x=0, y=60)
        network.place(x=0, y=90)
        label_node.place(x=0, y=120)
        asn.place(x=0, y=150)
        service_load.place(x=0, y=180)
        longitude.place(x=0, y=210)
        latitude.place(x=0, y=240)

        self.idnode_entry.place(x=100, y=30)
        self.countrynode_entry.place(x=100, y=60)
        self.network_entry.place(x=100, y=90)
        self.label_node_entry.place(x=100, y=120)
        self.asn_entry.place(x=100, y=150)
        self.serviceload_entry.place(x=100, y=180)
        self.longitude_entry.place(x=100, y=210)
        self.latitude_entry.place(x=100, y=240)

        vertex_apply = Button(self, text="Apply change", command=lambda: self.gui_support.set_vertex_value())
        vertex_apply.place(x=17, y=270)
        vertext_locate = Button(self, text="Map Locate", command=lambda: self.gui_support.open_map())
        vertext_locate.place(x=147, y=270)
        # x=0, y=270##############################################

        # EDGE x = 0, y = 300 ###################################
        edge_infomation = Label(self, text="Edge", font="Helvetica 16 bold")
        link_type = Label(self, text="LinkType")
        link_node = Label(self, text="LinkNote")
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

        self.link_type_entry.insert(0, "")
        self.link_note_entry.insert(0, "")
        self.link_label_entry.insert(0, "")
        self.link_speed_raw_entry.insert(0, "")
        self.buffer_delay_entry.insert(0, "")
        self.transmission_delay_entry.insert(0, "")
        self.propagation_delay_entry.insert(0, "")

        edge_infomation.place(x=100, y=300)
        link_type.place(x=0, y=330)
        link_node.place(x=0, y=360)
        link_label.place(x=0, y=390)
        link_speed_raw.place(x=0, y=420)
        buffer_delay.place(x=0, y=450)
        transmission_delay.place(x=0, y=480)
        propagation_delay.place(x=0, y=510)

        self.link_type_entry.place(x=100, y=330)
        self.link_note_entry.place(x=100, y=360)
        self.link_label_entry.place(x=100, y=390)
        self.link_speed_raw_entry.place(x=100, y=420)
        self.buffer_delay_entry.place(x=100, y=450)
        self.transmission_delay_entry.place(x=100, y=480)
        self.propagation_delay_entry.place(x=100, y=510)

        edge_apply = Button(self, text="Apply change", command=lambda: self.gui_support.set_edge_value())
        edge_apply.place(x=17, y=540)

        # x=0, y=540 ##############################

        # RESET Buttons x=15, y=600 ###########################
        # TODO: clear out or bring back to the original
        vertex_color_reset = Button(self, text="Reset vertex ",
                                    command=lambda: [self.gui_support.reset_vertex_color(),
                                                     self.gui_support.reset_note_vertex()])
        vertex_color_reset.place(x=17, y=600)
        edge_color_reset = Button(self, text="Reset edge ",
                                  command=lambda: [self.gui_support.reset_edge_color(),
                                                   self.gui_support.reset_note_edge(),
                                                   self.gui_support.reset_edge_width()])
        edge_color_reset.place(x=150, y=600)

        # x=15, y=600 #########################################

    def popup_group_vertex(self):
        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Vertex color")

        tkVar = StringVar(popupBonusWindow)
        vertex_att = self.gui_support.vertex_attributes()
        tkVar.set(vertex_att[0])

        input_name = tk.Label(popupBonusWindow, text="Choose Attribute")
        input_name.grid(row=0, padx=10, pady=5)
        input_entry = OptionMenu(popupBonusWindow, tkVar, *vertex_att)
        input_entry.grid(row=0, column=1, padx=10, pady=5)

        def change_dropdown(*args):
            print(tkVar.get())
            self.gui_support.group_vertex(tkVar.get())

        tkVar.trace('w', change_dropdown)

    def popup_vertex_text(self):    # TODO: generalize
        # popupBonusWindow = tk.Tk()
        # popupBonusWindow.wm_title("Vertex text box")
        # input_name = tk.Label(popupBonusWindow, text="Attribute")
        # input_name.grid(row=0)
        # input_entry = tk.Entry(popupBonusWindow)
        # input_entry.grid(row=0, column=1)
        # B1 = tk.Button(popupBonusWindow, text="Okay", command=lambda: self.gui_support.set_vertex_box(input_entry.get()))
        # B2 = tk.Button(popupBonusWindow, text="Clear", command=lambda: self.gui_support.clear_vertex_text_box())
        # B1.grid(row=0, column=2)
        # B2.grid(row=1, column=1)

        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Vertex text box")

        tkVar = StringVar(popupBonusWindow)
        vertex_att = self.gui_support.vertex_attributes_nofilter()
        tkVar.set(vertex_att[0])

        input_name = tk.Label(popupBonusWindow, text="Choose Attribute")
        input_name.grid(row=0, padx=10, pady=5)
        input_entry = OptionMenu(popupBonusWindow, tkVar, *vertex_att)
        input_entry.grid(row=0, column=1, padx=10, pady=5)

        def change_dropdown(*args):
            print(tkVar.get())
            self.gui_support.set_vertex_box(tkVar.get())

        tkVar.trace('w', change_dropdown)
        B2 = tk.Button(popupBonusWindow, text="Clear", command=lambda: self.gui_support.clear_vertex_text_box())
        B2.grid(row=1, column=0, columnspan=2)

    def popup_vertex_size(self):       # TODO: Maybe improve
        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Vertex size")
        input_name = tk.Label(popupBonusWindow, text="Radius")
        # input_name.grid()
        scale = tk.Scale(popupBonusWindow, orient='horizontal', from_=0, to=10,
                         length=100,
                         command=lambda x: self.gui_support.set_vertex_size(scale.get()))
        scale.grid()

    def popup_search_vertex(self):
        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Search vertex")
        input_att = tk.Label(popupBonusWindow, text="Attribute")
        input_att.grid()
        att_entry = tk.Entry(popupBonusWindow)
        att_entry.grid(row=0, column=1)
        input_value = tk.Label(popupBonusWindow, text="Value")
        input_value.grid(row=1)
        att_value_entry = tk.Entry(popupBonusWindow)
        att_value_entry.grid(row=1, column=1)
        B1 = tk.Button(popupBonusWindow, text="Okay",
                       command=lambda: self.gui_support.search_vertex(att_entry.get(), att_value_entry.get()))
        B2 = tk.Button(popupBonusWindow, text="Clear", command=lambda: self.gui_support.clear_search_vertex())
        B1.grid(row=2, column=1)
        B2.grid(row=3, column=1)

    def get_vertex_value(self, list_value):
        self.idnode_entry.delete(0, "end")
        self.countrynode_entry.delete(0, "end")
        self.network_entry.delete(0, "end")
        self.label_node_entry.delete(0, "end")
        self.asn_entry.delete(0, "end")
        self.serviceload_entry.delete(0, "end")
        self.longitude_entry.delete(0, "end")
        self.latitude_entry.delete(0, "end")

        self.idnode_entry.insert(0, list_value[0])
        self.countrynode_entry.insert(0, list_value[1])
        self.network_entry.insert(0, list_value[2])
        self.label_node_entry.insert(0, list_value[3])
        self.asn_entry.insert(0, list_value[4])
        self.serviceload_entry.insert(0, list_value[5])
        self.longitude_entry.insert(0, list_value[6])
        self.latitude_entry.insert(0, list_value[7])

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
        input_name = tk.Label(popup_bonus_window, text="Choose Attribute")
        input_name.grid(row=0, padx=10, pady=5)

        tkVar = StringVar(popup_bonus_window)
        edge_att = self.gui_support.edge_attributes()
        tkVar.set(edge_att[0])

        def change_dropdown(*args):
            print(tkVar.get())
            self.gui_support.edge_width(tkVar.get())

        tkVar.trace('w', change_dropdown)

        input_entry = OptionMenu(popup_bonus_window, tkVar, *edge_att)
        input_entry.grid(row=0, column=1, padx=10, pady=5)

    def popup_group_edge_color(self):
        print("into func. self.Delay")
        popup_window = tk.Tk()
        popup_window.wm_title("Edge color")
        input_name = tk.Label(popup_window, text="Choose Attribute")
        input_name.grid(row=0, padx=10, pady=5)

        tkVar = StringVar(popup_window)
        edge_att = self.gui_support.edge_attributes()
        tkVar.set(edge_att[0])

        inputentry = OptionMenu(popup_window, tkVar, *edge_att)
        inputentry.grid(row=0, column=1, padx=10, pady=5)

        def change_dropdown(*args):
            print(tkVar.get())
            self.gui_support.edge_color(tkVar.get())

        tkVar.trace('w', change_dropdown)

    def get_throughput_name(self, value):
        self.gui_support.throughput = value[0]
        self.gui_support.throughput_len = value[1]

    def popup_throughput(self):
        popup_bonus_window = Tk()
        popup_bonus_window.wm_title("Throughput window")
        input_name = Label(popup_bonus_window, text="Throughput file")
        input_name.grid(row=0)
        input_entry = Entry(popup_bonus_window)
        input_entry.grid(row=0, column=1)
        throughput_threshold = Label(popup_bonus_window, text="Threshold")
        throughput_threshold.grid(row=1, column=0)
        input_throughput_threshold = Entry(popup_bonus_window)
        input_throughput_threshold.insert(0, "0.9")
        input_throughput_threshold.grid(row=1, column=1)
        B1 = Button(popup_bonus_window, text="Browse",
                    command=lambda: [input_entry.delete(0, "end"),
                                     self.get_throughput_name(self.gui_support.open_throughput()),
                                     input_entry.insert(0, self.gui_support.throughput),
                                     self.gui_support.get_throughput_time(spin_box_1.get(),
                                                                          self.gui_support.throughput,
                                                                          float(input_throughput_threshold.get()))])
        B1.grid(row=0, column=2)
        spin_box_1 = tk.Spinbox(popup_bonus_window, from_=0, to=23, width=18,
                                command=lambda: self.gui_support.get_throughput_time(spin_box_1.get(),
                                                                                     self.gui_support.throughput,
                                                                                     float(input_throughput_threshold.get())))
        spin_box_1.grid(row=2, column=1)
        threshold_button = Button(popup_bonus_window, text="Apply",
                                  command=lambda: [self.gui_support.get_throughput_time(spin_box_1.get(),
                                                                                        self.gui_support.throughput,
                                                                                        float(
                                                                                            input_throughput_threshold.get()))])
        threshold_button.grid(row=1, column=2)
        # TODO clear when close
        # popup_bonus_window.protocol("WM_DELETE_WINDOW", print("hello"))

    def popup_geo_window(self):
        window = Toplevel(self.master)
        window.wm_title("Geo Window")
        frame = tk.Frame(window)
        frame.pack(side="top", fill="both", expand=True)
        GeoPage.GeoPage(frame, window, self.gui_support.graph_path)

    def popup_statistic(self):
        from Statistic import Statistic
        window = tk.Tk()
        window.wm_title("Statistic")
        frame = tk.Frame(window)
        input_name = tk.Label(window, text='Attribute')
        input_name.grid(row=0, column=1)
        input_entry = tk.Entry(window)
        input_entry.grid(row=0, column=1)
        # frame.pack(side="top", fill="both", expand=True)
        # Statistic(frame, window, self.mg.get_all_attribute_value("LinkSpeedRaw",False),'LinkSpeedRaw')
        B1 = tk.Button(window, text="Stat pls", command=lambda: Statistic(frame, window,
                                                                            self.mg.get_all_attribute_value(
                                                                                input_entry.get(), False), input_entry.get()))
        B1.grid(row=0, column=2)