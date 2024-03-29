from Statistic import StatisticPie2
from GUI_support import *
from MapLocate import *
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
        self.master.title("Netzwerkvisualisierung von TeamWhite - v1.0")
        self.pack(fill="both", expand=1)
        self.gui_frame.canvas = tk.Canvas(self, width=900, height=0, background="white")
        self.gui_frame.canvas.pack()
        menu = Menu(self.master)
        self.master.config(menu=menu)
        File = Menu(menu)
        Vertex_highlight = Menu(menu)
        Edge_highlight = Menu(menu)
        Layout_menu = Menu(menu)
        Search = Menu(menu)
        Centrality = Menu(menu)
        Add = Menu(menu)
        Delete = Menu(menu)

        File.add_command(label="Open", command=lambda: self.gui_support.open())
        File.add_command(label="Save", command=lambda: self.gui_support.save())
        File.add_command(label="Exit", command=lambda: self.master.destroy())

        Vertex_highlight.add_command(label="Highlight vertex by color", command=lambda: self.popup_group_vertex())
        Vertex_highlight.add_command(label="Vertex text box", command=lambda: self.popup_vertex_text())
        # Vertex_highlight.add_command(label="vertex_size", command=lambda: self.popup_vertex_size())

        Edge_highlight.add_command(label="Highlight edge by width", command=lambda: self.popup_group_edge_width())
        Edge_highlight.add_command(label="Highlight edge by color", command=lambda: self.popup_group_edge_color())

        Layout_menu.add_command(label="Original layout",
                                command=lambda: self.gui_support.start_graph())
        Layout_menu.add_command(label="Reingold tilford circular",
                                command=lambda: self.gui_support.reingold_tilford_circular())
        Layout_menu.add_command(label="Fruchterman reingold",
                                command=lambda: self.gui_support.fruchterman_reingold())
        Layout_menu.add_command(label="Circle",
                                command=lambda: self.gui_support.circle())
        Layout_menu.add_command(label="Mds",
                                command=lambda: self.gui_support.mds())
        Layout_menu.add_command(label="Random",
                                command=lambda: self.gui_support.random_lay())

        Search.add_command(label="Vertex", command= lambda: self.popup_search_vertex())
        Search.add_command(label="Edge", command=lambda: self.popup_search_edge())
        # create add vertex button
        Add.add_command(label="Add vertex", command=lambda: self.gui_support.add_vertex())
        Add.add_command(label="Add edge", command=lambda: self.gui_support.add_edge())

        Delete.add_command(label="Delete vertex", command=lambda: self.gui_support.delete_vertex())
        Delete.add_command(label="Delete edge", command=lambda: self.gui_support.delete_edge())

        Centrality.add_command(label="Vertex", command= lambda: self.popup_vertex_centrality())
        Centrality.add_command(label="Edge", command= lambda: self.popup_edge_centrality())

        menu.add_cascade(label="File", menu=File)
        menu.add_cascade(label="Vertex Highlight", menu=Vertex_highlight)
        menu.add_cascade(label="Edge Highlight", menu=Edge_highlight)
        menu.add_cascade(label="Layout", menu=Layout_menu)
        menu.add_command(label="Throughput", command=lambda: self.popup_throughput())
        menu.add_cascade(label="Search", menu=Search)
        menu.add_command(label="GeoWindow", command=lambda: self.popup_geo_window())
        menu.add_command(label="Statistics", command=lambda: self.popup_statistic())
        menu.add_cascade(label="Centrality", menu=Centrality)
        menu.add_cascade(label="Add", menu=Add)
        menu.add_cascade(label="Delete", menu=Delete)
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

        # Vertex size bar x=10, y=680 #####################################
        input_name = tk.Label(self, text="Vertex size")
        input_name.place(x=10, y=680)
        scale = tk.Scale(self, orient='horizontal', from_=0, to=10,
                         length=160,
                         command=lambda x: self.gui_support.set_vertex_size(scale.get()))
        scale.place(x=100, y=660)

        # x=100, y=680 ##############################################

    def popup_group_vertex(self):
        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Vertex color")

        tkVar = StringVar(popupBonusWindow)
        vertex_att = self.gui_support.vertex_attributes("group")
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
        vertex_att = self.gui_support.vertex_attributes("text box")
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
        scale.place(x=10, y=10)

    def popup_search_vertex(self):
        # popupBonusWindow = tk.Tk()
        # popupBonusWindow.wm_title("Search vertex")
        # input_att = tk.Label(popupBonusWindow, text="Attribute")
        # input_att.grid()
        # att_entry = tk.Entry(popupBonusWindow)
        # att_entry.grid(row=0, column=1)

        # B1 = tk.Button(popupBonusWindow, text="Okay",
        #                command=lambda: self.gui_support.search_vertex(att_entry.get(), att_value_entry.get()))
        # B2 = tk.Button(popupBonusWindow, text="Clear", command=lambda: self.gui_support.clear_search_vertex())
        # B1.grid(row=2, column=1)
        # B2.grid(row=3, column=1)

        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Search vertex")

        tkVar = StringVar(popupBonusWindow)
        vertex_att = self.gui_support.vertex_attributes("search")
        tkVar.set(vertex_att[0])

        input_name = tk.Label(popupBonusWindow, text="Choose Attribute")
        input_name.grid(row=0, padx=10, pady=5)
        input_entry = OptionMenu(popupBonusWindow, tkVar, *vertex_att)
        input_entry.grid(row=0, column=1, padx=10, pady=5)

        input_value = tk.Label(popupBonusWindow, text="Value")
        input_value.grid(row=1)
        att_value_entry = tk.Entry(popupBonusWindow)
        att_value_entry.grid(row=1, column=1, padx=10, pady=5)

        def change_dropdown(*args):
            print(tkVar.get())

        tkVar.trace('w', change_dropdown)
        B1 = tk.Button(popupBonusWindow, text="Okay",
                         command=lambda: [self.gui_support.clear_search_vertex(),
                             self.gui_support.search_vertex(tkVar.get(), att_value_entry.get())])
        B1.grid(row=2, column=0, pady=5)
        B2 = tk.Button(popupBonusWindow, text="Clear", command=lambda: self.gui_support.clear_search_vertex())
        B2.grid(row=2, column=1, pady=5)

    def popup_edge_centrality(self):
        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Edge centrality")

        tkVar = StringVar(popupBonusWindow)
        edge_att = self.gui_support.edge_attributes("width")
        tkVar.set(edge_att[0])

        input_name = tk.Label(popupBonusWindow, text="Choose Attribute")
        input_name.grid(row=0, padx=10, pady=5)
        input_entry = OptionMenu(popupBonusWindow, tkVar, *edge_att)
        input_entry.grid(row=0, column=1, padx=10, pady=5)

        def change_dropdown(*args):
            print(tkVar.get())
            self.gui_support.show_edge_centrality(tkVar.get())

        tkVar.trace('w', change_dropdown)

    def popup_vertex_centrality(self):
        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Vertex centrality")

        tkVar = StringVar(popupBonusWindow)
        edge_att = self.gui_support.edge_attributes("width")
        tkVar.set(edge_att[0])

        input_name = tk.Label(popupBonusWindow, text="Choose Attribute")
        input_name.grid(row=0, padx=10, pady=5)
        input_entry = OptionMenu(popupBonusWindow, tkVar, *edge_att)
        input_entry.grid(row=0, column=1, padx=10, pady=5)

        def change_dropdown(*args):
            print(tkVar.get())
            self.gui_support.show_vertex_centrality(tkVar.get())

        tkVar.trace('w', change_dropdown)

    def popup_search_edge(self):
        # popupBonusWindow = tk.Tk()
        # popupBonusWindow.wm_title("Search edge")
        # input_att = tk.Label(popupBonusWindow, text="Attribute")
        # input_att.grid()
        # att_entry = tk.Entry(popupBonusWindow)
        # att_entry.grid(row=0, column=1)

        # B1 = tk.Button(popupBonusWindow, text="Okay",
        #                command=lambda: self.gui_support.search_edge(att_entry.get(), att_value_entry.get()))
        # B2 = tk.Button(popupBonusWindow, text="Clear", command=lambda: self.gui_support.clear_search_edge())
        # B1.grid(row=2, column=1)
        # B2.grid(row=3, column=1)

        popupBonusWindow = tk.Tk()
        popupBonusWindow.wm_title("Search edge")

        tkVar = StringVar(popupBonusWindow)
        edge_att = self.gui_support.edge_attributes("search")
        tkVar.set(edge_att[0])

        input_name = tk.Label(popupBonusWindow, text="Choose Attribute")
        input_name.grid(row=0, padx=10, pady=5)
        input_entry = OptionMenu(popupBonusWindow, tkVar, *edge_att)
        input_entry.grid(row=0, column=1, padx=10, pady=5)

        input_value = tk.Label(popupBonusWindow, text="Value")
        input_value.grid(row=1)
        att_value_entry = tk.Entry(popupBonusWindow)
        att_value_entry.grid(row=1, column=1, padx=10, pady=5)

        def change_dropdown(*args):
            print(tkVar.get())

        tkVar.trace('w', change_dropdown)
        B1 = tk.Button(popupBonusWindow, text="Okay",
                         command=lambda: [self.gui_support.clear_search_edge()
                             ,self.gui_support.search_edge(tkVar.get(), att_value_entry.get())])
        B1.grid(row=2, column=0, pady=5)
        B2 = tk.Button(popupBonusWindow, text="Clear", command=lambda: self.gui_support.clear_search_edge())
        B2.grid(row=2, column=1, pady=5)

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
        edge_att = self.gui_support.edge_attributes("width")
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
        edge_att = self.gui_support.edge_attributes("color")
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
        input_name.grid(row=0, padx=5, pady=2)
        input_entry = Entry(popup_bonus_window)
        input_entry.grid(row=0, column=1, padx=5, pady=2)
        throughput_threshold = Label(popup_bonus_window, text="Threshold")
        throughput_threshold.grid(row=1, column=0, padx=5, pady=2)
        input_throughput_threshold = Entry(popup_bonus_window)
        input_throughput_threshold.insert(0, "0.9")
        input_throughput_threshold.grid(row=1, column=1, padx=5, pady=2)
        B1 = Button(popup_bonus_window, text="Browse",
                    command=lambda: [input_entry.delete(0, "end"),
                                     self.get_throughput_name(self.gui_support.open_throughput()),
                                     input_entry.insert(0, self.gui_support.throughput),
                                     self.gui_support.get_throughput_time(spin_box_1.get(),
                                                                          self.gui_support.throughput,
                                                                          float(input_throughput_threshold.get()))])
        B1.grid(row=0, column=2, sticky="W", padx=5, pady=2)
        spin_box_1 = tk.Spinbox(popup_bonus_window, from_=0, to=23, width=18,
                                command=lambda: self.gui_support.get_throughput_time(spin_box_1.get(),
                                                                                     self.gui_support.throughput,
                                                                                     float(input_throughput_threshold.get())))
        spin_box_1.grid(row=3, column=1, padx=5, pady=2)
        threshold_button = Button(popup_bonus_window, text="Apply",
                                  command=lambda: [self.gui_support.get_throughput_time(spin_box_1.get(),
                                                                                        self.gui_support.throughput,
                                                                                        float(
                                                                                            input_throughput_threshold.get()))])
        threshold_button.grid(row=1, column=2, sticky="W", padx=5, pady=2)

        hour_label = Label(popup_bonus_window, text="Hour")
        hour_label.grid(row=3, column=0, padx=5, pady=2)

        tkVar = StringVar(popup_bonus_window)
        edge_att = ["Pie Chart", "Bar Chart"]
        tkVar.set("Threshold statistic")

        input_stat = OptionMenu(popup_bonus_window, tkVar, *edge_att)
        input_stat.grid(row=3, column=2, columnspan=2, sticky="W", padx=5, pady=2)

        def change_dropdown(*args):
            print(tkVar.get())
            self.call_statistic_throughput(int(spin_box_1.get()), tkVar.get())

        tkVar.trace('w', change_dropdown)
        #########
        # tkVar2 = StringVar(popup_bonus_window)
        # edge_att2 = ["Pie Chart", "Bar Chart"]
        # tkVar2.set("Label Statistic")    #TODO: turn it into bar chart only and make both total by link label and high throughput

        # input_stat2 = OptionMenu(popup_bonus_window, tkVar2, *edge_att2)
        # input_stat2.grid(row=2, column=2, sticky="W", padx=5, pady=2)
        input_stat2 = Button(popup_bonus_window,text="Label Statistic", command = lambda:self.call_statistic_throughput_label(int(spin_box_1.get()),
                                                 float(input_throughput_threshold.get()), "Bar Chart"))
        input_stat2.grid(row=1, column=3)

        # def change_dropdown2(*args):
        #     print(tkVar2.get())
        #     self.call_statistic_throughput_label(int(spin_box_1.get()),
        #                                          float(input_throughput_threshold.get()), tkVar2.get())
        #
        # tkVar2.trace('w', change_dropdown2)


        # TODO clear when close

    def popup_geo_window(self):
        window = Toplevel(self.master)
        window.wm_title("Geo Window")
        frame = tk.Frame(window)
        frame.pack(side="top", fill="both", expand=True)
        GeoPage.GeoPage(frame, window, self.gui_support.graph_path)

    def popup_statistic(self):
        # window = tk.Tk()
        # window.wm_title("Statistic")
        # frame = tk.Frame(window)
        # input_name = tk.Label(window, text='Attribute')
        # input_name.grid(row=0, column=1)
        # input_entry = tk.Entry(window)
        # input_entry.grid(row=0, column=1)
        # # frame.pack(side="top", fill="both", expand=True)
        # # Statistic(frame, window, self.mg.get_all_attribute_value("LinkSpeedRaw",False),'LinkSpeedRaw')
        # B1 = tk.Button(window, text="Stat pls", command=lambda: [self.call_statistic_window(input_entry.get()),
        #                                                          window.destroy()])
        # B1.grid(row=0, column=2)


        window = tk.Tk()
        window.wm_title("Statistic")
        frame = tk.Frame(window)
        input_name = tk.Label(window, text="Choose Attribute")
        input_name.grid(row=0, column=1, padx=10, pady=5)

        tkVar = StringVar(window)
        edge_att = self.gui_support.edge_attributes("statistic")
        tkVar.set(edge_att[0])

        inputentry = OptionMenu(window, tkVar, *edge_att)
        inputentry.grid(row=0, column=2, padx=10, pady=5)

        def change_dropdown(*args):
            print(tkVar.get())

        tkVar.trace('w', change_dropdown)
        B1 = tk.Button(window, text="Statistic", command=lambda: [self.call_statistic_window(tkVar.get()),
                                                                 window.destroy()])
        B1.grid(row=0, column=3, padx=10, pady=5)

    def call_statistic_window(self, att):
        from Statistic import StatisticPie
        StatisticPie(self.mg.get_all_attribute_value(att, False), att)

    def call_statistic_throughput(self, hour, chart):
        from ThroughputInformation import get_throughput_information
        from Statistic import Statistic2
        import numpy as np
        window = tk.Tk()
        csv_table = get_throughput_information(self.gui_support.throughput)
        throughput_list = csv_table[hour].tolist()
        edgelink = self.mg.get_all_attribute_value('LinkSpeedRaw', False)
        # result = [i / j for i, j in zip(throughput_list, edgelink)]
        result = []
        for i in range(len(edgelink)):
            result.append(float(throughput_list[i]) / float(edgelink[i]))
        edgelist = np.round(np.array(result), 1)
        print(edgelist)
        window.wm_title("Statistic")
        frame = tk.Frame(window)
        frame.pack(side="top", fill="both", expand=True)
        if chart == "Pie Chart":
            StatisticPie2(window, edgelist, 'something', hour)
        elif chart == "Bar Chart":
            Statistic2(window, frame, edgelist, 'something', hour)

    def call_statistic_throughput_label(self, hour, threshold, chart):
        from ThroughputInformation import get_throughput_information
        from Statistic import StatisticPie3, Statistic3
        import numpy as np
        window = tk.Tk()
        csv_table = get_throughput_information(self.gui_support.throughput)
        throughput_list = csv_table[hour].tolist()
        edgelink = self.mg.get_all_attribute_value('LinkSpeedRaw', False)
        # result = [i / j for i, j in zip(throughput_list, edgelink)]
        result = []
        for i in range(len(edgelink)):
            result.append(float(throughput_list[i]) / float(edgelink[i]))
        edgelist = np.round(np.array(result), 1)
        print(edgelist)
        window.wm_title("Statistic")
        frame = tk.Frame(window)
        frame.pack(side="top", fill="both", expand=True)
        if chart == "Pie Chart":
            StatisticPie3(window, edgelist, self.mg, hour, threshold)
        elif chart == "Bar Chart":
            Statistic3(window, edgelist, self.mg, hour, threshold)
        pass