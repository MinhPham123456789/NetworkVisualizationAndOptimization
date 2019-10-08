import random
from tkinter import filedialog
from typing import List

from AttributeFilter import AttFilter
from DragObject import MouseMover
from MapLocate import *
from Note import *
from ObjectTk.ObjTkFrame import *
from ObjectTk.ObjTkLayout import GraphLayout
from ObjectTk.ObjectDrawTkinter import ObjDrawTkinter
from ZoomAndDrag import ZoomAndDrag


class GUI_support():
    def __init__(self, gui):
        self.gui = gui
        self.selected_vertex = None
        self.selected_edge = None
        self.is_vertex = False
        self.list_note = []
        self.maplocate = None

    def open(self):
        print("Loading")
        graph_name = filedialog.askopenfilename(initialdir="/home", title="Select file",
                                                filetypes=[("graph", "*.graphml")])

        NREN = Graph.Read_GraphML(graph_name)
        self.graph = NREN
        self.graph_path = graph_name  # Help in geo window
        self.gui.mg = ObjManager(NREN)  # GET VERTICES AND EDGES FROM GRAPHML AND MAKE THEM OBJECTS
        self.gui.frame.destroy()
        self.gui.frame = ObjTkFrame(self.gui.master)
        self.gui.canvas = self.gui.frame.canvas
        self.gui.drawTk = ObjDrawTkinter(300, self.gui.mg, self.gui.frame)
        self.gui.layout = GraphLayout(NREN)
        # GENERATE ADDITIONAL ATTRIBUTES TODO: coordinate problem
        try:
            NREN.vs["x"]
        except KeyError:
            self.gui.mg.add_attribute_list("x", NREN.vs["Longitude"], True)
            NREN.vs["x"] = NREN.vs["Longitude"]

        try:
            NREN.vs["y"]
        except KeyError:
            NREN.vs["y"] = [i * (-1) for i in NREN.vs["Latitude"]]
            self.gui.mg.add_attribute_list("y", NREN.vs["y"], True)

        try:
            NREN["Network"]
            self.gui.mg.add_attribute("Network", NREN["Network"], True)
        except KeyError:
            pass

        try:
            NREN.vs["color"]
        except KeyError:
            self.gui.mg.add_attribute("color", "red", True)

        try:
            NREN.es["color"]
        except KeyError:
            self.gui.mg.add_attribute("color", "white", False)

        try:
            NREN.vs["vertex_size"]
        except KeyError:
            self.gui.mg.add_attribute("vertex_size", 0.08, True)

        try:
            NREN.vs["Internal"]
        except KeyError:
            self.gui.mg.add_attribute_list("Internal", random_value(0.0, 10.0, len(self.gui.mg.vertex)), True)

        # ADD DRAG AND ZOOM
        zm = ZoomAndDrag(self.gui.frame, self.gui.mg)

        # ADD DRAG OBJECTS
        mm = MouseMover(self.gui.frame, self.gui.drawTk, NREN, self.gui.mg, self)

        # MOTION
        self.gui.frame.canvas.bind("<Button-3>", mm.select)
        self.gui.frame.canvas.bind("<B3-Motion>", mm.drag)
        self.gui.frame.canvas.bind("<Button-1>", zm.move_start)
        self.gui.frame.canvas.bind("<B1-Motion>", zm.move_move)
        self.gui.frame.canvas.bind("<Button-4>", zm.zoomIn)
        self.gui.frame.canvas.bind("<Button-5>", zm.zoomOut)

        # LOAD VERTICES AND EDGE FROM GRAPHML (Note: reverse draw edge before vertex for nice visual
        self.gui.drawTk.load_vertices()
        self.gui.drawTk.load_edges()
        self.gui.drawTk.load_vertex_text_weight("service_load")
        self.gui.drawTk.test()
        # self.note = Note(self.gui.master)
        self.gui.frame.place(x=300, y=0)
        #reset note
        self.reset_note_vertex()
        self.reset_note_edge()
        #load_note
        self.loadnode(NREN)

    def loadnode(self,graph):
        try:
            self.edge_width(graph["note_edge_width"])
        except: pass
        try:
            self.edge_color(graph["note_edge_color"])
        except: pass
        try:
            color_dict = {}
            list_attribute = self.gui.mg.get_all_attribute_value(graph["note_vertex_color"],True)
            list_color = self.gui.mg.get_all_attribute_value("color",True)
            for i in range(len(list_attribute)):
                color_dict.update({list_attribute[i]:list_color[i]})
            note = Note(self.gui.master, color_dict, "group_vertex", graph["note_vertex_color"])
            self.list_note.append(note)
            note.display()
            print("load node color")
        except: pass

    def save(self):
        graph_name = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                  filetypes=[("graph", "*.graphml")])
        new_graph = self.gui.mg.save_graph(self.gui.drawTk, self.gui.canvas)
        new_graph["note_edge_width"] = Note.note_edge_width
        new_graph["note_edge_color"] = Note.note_edge_color
        new_graph["note_vertex_color"] = Note.note_vertex_color
        new_graph.write_graphml(graph_name)

    def get_vertex_value(self, vertex_item_index):
        vertex_obj: VertexObj = self.gui.drawTk.items_table.inverse[vertex_item_index]
        self.selected_vertex = vertex_obj
        node_id = str(vertex_obj.get_attribute("id"))
        country = str(vertex_obj.get_attribute("Country"))
        network = str(vertex_obj.get_attribute("Network"))
        label = str(vertex_obj.get_attribute("label"))
        asn = str(vertex_obj.get_attribute("asn"))
        service_load = str(vertex_obj.get_attribute("Internal"))
        longitude = str(vertex_obj.get_attribute("Longitude"))
        latitude = str(vertex_obj.get_attribute("Latitude"))
        result_list: List[str] = [node_id, country, network, label, asn, service_load, longitude, latitude]
        self.gui.get_vertex_value(result_list)

    def set_vertex_value(self):
        if self.is_vertex:
            new_country = self.gui.countrynode_entry.get()
            new_network = self.gui.network_entry.get()
            new_label = self.gui.label_node_entry.get()
            new_asn = self.gui.asn_entry.get()
            new_service_load = self.gui.serviceload_entry.get()
            self.selected_vertex.set_attribute("Country", new_country)
            self.selected_vertex.set_attribute("Network", new_network)
            self.selected_vertex.set_attribute("label", new_label)
            self.selected_vertex.set_attribute("asn", new_asn)
            self.selected_vertex.set_attribute("Internal", new_service_load)
            result = [new_country, new_network, new_label, new_asn, new_service_load]
            print(result)
        else:
            print("not vertex")

        ##new##

    def get_edge_value(self, edge_item_index):
        edge_obj: EdgeObj = self.gui.drawTk.items_table.inverse[edge_item_index]
        self.selected_edge = edge_obj
        link_type = str(edge_obj.get_attribute("LinkType"))
        link_node = str(edge_obj.get_attribute("LinkNote"))
        link_label = str(edge_obj.get_attribute("LinkLabel"))
        link_speed_raw = str(edge_obj.get_attribute("LinkSpeedRaw"))
        buffer_delay = str(edge_obj.get_attribute("bufferDelay"))
        transmission_delay = str(edge_obj.get_attribute("tranmissionDelay"))
        propagation_delay = str(edge_obj.get_attribute("propagationDelay"))
        result_list: List[str] = [link_type, link_node, link_label, link_speed_raw, buffer_delay,
                                  transmission_delay, propagation_delay]
        self.gui.get_edge_value(result_list)

    def set_edge_value(self):
        if not self.is_vertex:
            new_link_type = self.gui.link_type_entry.get()
            new_link_note = self.gui.link_note_entry.get()
            new_link_label = self.gui.link_label_entry.get()
            new_link_speed_raw = self.gui.link_speed_raw_entry.get()
            new_buffer_delay = self.gui.buffer_delay_entry.get()
            new_transmission_delay = self.gui.transmission_delay_entry.get()
            new_propagation_delay = self.gui.propagation_delay_entry.get()
            self.selected_edge.set_attribute("LinkType", new_link_type)
            self.selected_edge.set_attribute("LinkNote", new_link_note)
            self.selected_edge.set_attribute("LinkLabel", new_link_label)
            self.selected_edge.set_attribute("LinkSpeedRaw", new_link_speed_raw)
            self.selected_edge.set_attribute("bufferDelay", new_buffer_delay)
            self.selected_edge.set_attribute("tranmissionDelay", new_transmission_delay)
            self.selected_edge.set_attribute("propagationDelay", new_propagation_delay)
            result = [new_link_type, new_link_note, new_link_label, new_link_speed_raw, new_buffer_delay,
                      new_transmission_delay, new_propagation_delay]
            print(result)
        else:
            print("not edge")

    def open_throughput(self, ):
        import pandas as pd
        throughput_name = filedialog.askopenfilename(initialdir="/home", title="Select file",
                                                     filetypes=[("throughput", "*.csv")])
        csv_test = pd.read_csv(throughput_name)
        return throughput_name, len(csv_test.columns)

    def get_throughput_time(self, value, csv_table, threshold: float):
        from ThroughputInformation import get_throughput_information
        value = int(value)
        threshold_ratio = threshold
        csv_table = get_throughput_information(csv_table)
        throughput_list = csv_table[value].tolist()
        bandwidth_list = self.gui.mg.get_all_attribute_value("LinkSpeedRaw", False)
        print("throughput_list", throughput_list)
        print("bandwidth_list", bandwidth_list)
        edge_index_list = []
        for i in range(len(bandwidth_list)):
            if float(throughput_list[i] / bandwidth_list[i]) > threshold_ratio:
                edge_index_list.append(i)
        self.gui.drawTk.recolor_edge_current()
        self.gui.drawTk.recolor_edge_index_list(edge_index_list, self.gui.mg, "#a02aa9")
        pass

    def group_vertex(self, value):
        att_name = str(value)
        print(att_name)
        result = self.gui.drawTk.group_vertex_color(att_name, self.gui.mg)
        color_list = result[1]
        color_dict = result[0]

        for i in range(len(color_list)):
            self.gui.canvas.itemconfigure(self.gui.drawTk.items_table[self.gui.mg.vertex[i]], fill=color_list[i])
        for note in self.list_note:
            if note.title == "group_vertex":
                self.list_note.remove(note)
                self.update_note()
                note.regenerate(color_dict,att_name)
                note.display()
                self.list_note.append(note)
                return
        note = Note(self.gui.master, color_dict, "group_vertex",att_name)
        self.list_note.append(note)
        note.display()

    def set_vertex_size(self, radius):
        self.gui.drawTk.resize_vertex_list(radius)

    def search_vertex(self, attribute, value):
        vertex_obj_list = []
        for vertex in self.gui.mg.vertex:
            if vertex.get_attribute(attribute) == value:
                vertex_obj_list.append(vertex)
        self.gui.drawTk.search_vertex_outline(vertex_obj_list, 3, True)
        self.search_vertex_list = vertex_obj_list

    def clear_search_vertex(self):
        self.gui.drawTk.search_vertex_outline(self.search_vertex_list, 1, False)
        self.search_vertex_list = []

    def reset_vertex_color(self):
        self.gui.drawTk.recolor_vertex_list(self.gui.mg.vertex, self.gui.mg, "red")

    def reset_edge_color(self):
        self.gui.drawTk.recolor_edge_list(self.gui.mg.edge, self.gui.mg, "#fafafa")

    def reset_edge_width(self):
        for edge in self.gui.mg.edge:
            self.gui.canvas.itemconfigure(self.gui.drawTk.items_table[edge], width=1)

    def set_vertex_box(self, vertex_weight):
        self.gui.drawTk.change_vertex_text_weight(vertex_weight, self.gui.canvas)

    def clear_vertex_text_box(self):
        for i in range(len(self.gui.mg.vertex)):
            index = "r" + str(i)
            self.gui.canvas.itemconfigure(self.gui.drawTk.items_table[index], state="hidden")

    # update existing node
    def update_note(self):
        Note.x = 1420
        Note.y = 0
        for note in self.list_note:
            note.display()

    def reset_note_edge(self):
        note = None
        Note.note_edge_width = None
        Note.note_edge_color = None
        for i in range(len(self.list_note)):
            if self.list_note[i].title == "group_vertex":
                note = self.list_note[i]
            else: self.list_note[i].hideframe()
        self.list_note = []
        if note != None:
            self.list_note.append(note)
        self.update_note()

    def reset_note_vertex(self):
        note1 = note2 = None
        Note.note_vertex_color = None
        for i in range(len(self.list_note)):
            if self.list_note[i].title == "edge_width":
                note1 = self.list_note[i]
            elif self.list_note[i].title == "edge_color":
                note2 = self.list_note[i]
            else: self.list_note[i].hideframe()
        self.list_note = []
        if note1 != None:
            self.list_note.append(note1)
        if note2 != None:
            self.list_note.append(note2)
        self.update_note()

    # kiet linkspeedraw:
    def edge_width(self, value):
        att_name = str(value)
        result = self.gui.drawTk.group_edge_bandwidth(att_name, self.gui.mg)
        threshold1 = float("{0:.2f}".format(result[0]))
        threshold2 = float("{0:.2f}".format(result[1]))
        threshold3 = float("{0:.2f}".format(result[2]))
        width_dict = result[3]
        for i in range(len(width_dict)):
            self.gui.canvas.itemconfigure(self.gui.drawTk.items_table[self.gui.mg.edge[i]], width=width_dict[i])
        note_dict = {threshold1: 1, threshold2: 3, threshold3: 6}
        for note in self.list_note:
            if note.title == "edge_width":
                self.list_note.remove(note)
                self.update_note()
                note.regenerate(note_dict,att_name)
                note.display()
                self.list_note.append(note)
                return
        note = Note(self.gui.master, note_dict, "edge_width",att_name)
        self.list_note.append(note)
        note.display()

    # thao          ##add note to function
    def edge_color(self, value):
        attribute = str(value)
        print("----GUI_support.edge_color()----")
        result = self.gui.drawTk.edge_color(attribute, self.gui.mg)
        edge_color_list = result[1]
        for i in range(len(edge_color_list)):
            self.gui.canvas.itemconfigure(self.gui.drawTk.items_table[self.gui.mg.edge[i]], fill=edge_color_list[i])
        print("//----GUI_support.edge_color()----")
        note_dict = result[0]
        for note in self.list_note:
            if note.title == "edge_color":
                self.list_note.remove(note)
                self.update_note()
                note.regenerate(note_dict,attribute)
                note.display()
                self.list_note.append(note)
                return
        note = Note(self.gui.master, note_dict, "edge_color",attribute)
        self.list_note.append(note)
        note.display()

    def start_graph(self):
        coords = self.gui.layout.start_layout()
        for i in range(len(coords)):
            self.change_position_instantly2(coords[i], self.gui.drawTk.items_table.inverse[i + 1])

    def reingold_tilford_circular(self):
        coords = self.gui.layout.reingold_tilford_circular_layout()
        for i in range(len(coords)):
            self.change_position_instantly2(coords[i], self.gui.drawTk.items_table.inverse[i + 1])

    def fruchterman_reingold(self):
        coords = self.gui.layout.fruchterman_reingold_layout()
        for i in range(len(coords)):
            self.change_position_instantly2(coords[i], self.gui.drawTk.items_table.inverse[i + 1])

    def circle(self):
        coords = self.gui.layout.circle_layout()
        for i in range(len(coords)):
            self.change_position_instantly2(coords[i], self.gui.drawTk.items_table.inverse[i + 1])

    def mds(self):
        coords = self.gui.layout.mds_layout()
        for i in range(len(coords)):
            self.change_position_instantly2(coords[i], self.gui.drawTk.items_table.inverse[i + 1])

    def random_lay(self):
        coords = self.gui.layout.random_layout()
        for i in range(len(coords)):
            self.change_position_instantly2(coords[i], self.gui.drawTk.items_table.inverse[i + 1])

    def change_position_instantly2(self, new_coord, vertex_obj):  # Use the new bidict
        source_list = []
        target_list = []
        center = self.gui.drawTk.get_moved_center()
        vertex_item_index = self.gui.drawTk.items_table[vertex_obj]
        xs, ys, xt, yt = self.gui.canvas.coords(vertex_item_index)
        old_width_len = 0.03
        old_height_len = 0.03
        x = new_coord[0] + center
        y = new_coord[1] + center
        try:
            vertex_obj_index = int(vertex_obj.get_attribute("id")[1:])  # [1:] because id more than 1 digit
        except TypeError:
            vertex_obj_index = int(vertex_obj.get_attribute("id"))
        print("vertex item:", vertex_obj_index)
        for edge in self.gui.mg.edge:
            if edge.get_attribute("source") == vertex_obj_index:
                source_list.append(edge)
        for edge in self.gui.mg.edge:
            if edge.get_attribute("target") == vertex_obj_index:
                target_list.append(edge)
        for i in source_list:
            edge_item_index = self.gui.drawTk.items_table[i]  # In item index, it starts from 1
            # and it adds vertices then edges
            print("sedge:", edge_item_index)
            x1, y1, x2, y2 = self.gui.canvas.coords(edge_item_index)
            self.gui.canvas.coords(edge_item_index, x, y, x2, y2)
        for u in target_list:
            edge_item_index = self.gui.drawTk.items_table[u]  # In item index, it starts from 1
            # and it adds vertices then edges
            print("tedge:", edge_item_index)
            x1, y1, x2, y2 = self.gui.canvas.coords(edge_item_index)
            self.gui.canvas.coords(edge_item_index, x1, y1, x, y)
        vx1 = x - old_width_len
        vy1 = y - old_height_len
        vx2 = x + old_width_len
        vy2 = y + old_height_len
        self.gui.canvas.coords(vertex_item_index, vx1, vy1, vx2, vy2)
        if self.gui.drawTk.rectangle_switch:
            rectangle_index = "r" + str(vertex_obj_index)
            position = self.gui.drawTk.set_weight_text_position(vertex_obj_index, self.gui.mg)
            self.gui.canvas.coords(self.gui.drawTk.items_table[rectangle_index], position)
        items = self.gui.canvas.find_withtag("all")
        # print(len(items))
        # print(len(self.mg.vertex))
        # print(len(self.mg.edge))
        # print(source_list)
        # print(target_list)
        print("test")

    def open_map(self):
        if self.is_vertex:
            print("----GUI Support func openmap()-----")
            self.maplocate = MapLocate(self.selected_vertex)
            self.maplocate.get_map()
            print("//----GUI Support func openmap()-----")

    def vertex_attributes(self):
        vertex_att_list = list(self.gui.mg.vertex[0].properties.keys())
        att_filter = AttFilter(vertex_att_list, True)
        att_list = att_filter.filter()
        return att_list

    def edge_attributes(self):
        edge_att_list = list(self.gui.mg.edge[0].properties.keys())
        att_filter = AttFilter(edge_att_list, False)
        att_list = att_filter.filter()
        return att_list

    def vertex_attributes_nofilter(self):
        vertex_att_list = list(self.gui.mg.vertex[0].properties.keys())
        return vertex_att_list


def random_value(min_point: float, max_point: float, size: int):
    result = [random.uniform(min_point, max_point) for i in range(size)]
    return result

# Storage
# # print(get_path_vertices_object(self.graph, 0, 1102))
# edge_count = {}
# for i in range(len(self.gui.mg.vertex)):
#     print("i", i)
#     for u in range(i+1, len(self.gui.mg.vertex)):
#         edge_list = get_path_edge_object(self.graph, i, u)
#         for e in edge_list:
#             try:
#                 edge_count[self.gui.drawTk.items_table[self.gui.mg.edge[e.index]]] += 1
#             except KeyError:
#                 edge_count[self.gui.drawTk.items_table[self.gui.mg.edge[e.index]]] = 1
#         # self.gui.drawTk.resize_vertex_list(get_path_vertices_object(self.graph, 0, 1102), self.gui.mg, 0.12)
#         self.gui.drawTk.recolor_edge_list(get_path_edge_object(self.graph, i, u), self.gui.mg, "#11fb09")
#         # for i in edge_list:
#         #     self.gui.canvas.itemconfigure(self.gui.drawTk.items_table[self.gui.mg.edge[i.index]], fill=self.gui.mg.edge[i.index].properties["color"])
