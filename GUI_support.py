from igraph import *

from DragObject import MouseMover
from ObjectTk.ObjectManager import *
from ObjectTk.ObjectDrawTkinter import *
from ObjectTk.ObjTkFrame import *
from ObjectTk.ObjTkLayout import GraphLayout
from tkinter import filedialog


class GUI_support():
    def __init__(self, gui):
        self.gui = gui

    def load(self):
        print("Loading")
        graph_name = filedialog.askopenfilename(initialdir="/home", title="Select file",
                                                filetypes=[("graph", "*.graphml")])

        NREN = Graph.Read_GraphML(graph_name)
        self.gui.mg = ObjManager(NREN)  # GET VERTICES AND EDGES FROM GRAPHML AND MAKE THEM OBJECTS
        self.gui.frame.destroy()
        self.gui.frame = ObjTkFrame(self.gui.master)
        self.gui.canvas = self.gui.frame.canvas
        self.gui.drawTk = ObjDrawTkinter(300, self.gui.mg, self.gui.frame)
        self.gui.layout = GraphLayout(NREN)
        # GENERATE ADDITIONAL ATTRIBUTES TODO: create check method before use this
        try:
            NREN.vs["color"]
        except KeyError:
            self.gui.mg.add_attribute("color", "red", True)

        try:
            NREN.es["color"]
        except KeyError:
            self.gui.mg.add_attribute("color", "gray", False)
        self.gui.mg.add_attribute("vertex_size", 0.06, True)
        self.gui.mg.add_attribute_list("service_load", random_value(0.0, 10.0, len(self.gui.mg.vertex)), True)

        # ADD DRAG AND ZOOM
        zm = ZoomAndDrag(self.gui.frame, self.gui.mg)

        # ADD DRAG OBJECTS
        mm = MouseMover(self.gui.frame, self.gui.drawTk, NREN, self.gui.mg)

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
        # DrawTk.load_vertex_text_weight("service_load")
        self.gui.drawTk.test()

        self.gui.frame.pack(fill="both", expand=True)

    def save(self):
        graph_name = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                  filetypes=[("graph", "*.graphml")])
        new_graph = self.gui.mg.save_graph(self.gui.drawTk, self.gui.canvas)
        new_graph.write_graphml(graph_name)

    def Groupvertex(self, value):
        att_name = str(value)
        print(att_name)
        color_list = self.gui.drawTk.group_vertex_color(att_name, self.gui.mg)
        print(self.gui.drawTk)
        print(self.gui.drawTk.group_vertex_color(att_name, self.gui.mg))
        for i in range(len(color_list)):
            self.gui.canvas.itemconfigure(self.gui.drawTk.items_table[self.gui.mg.vertex[i]], fill=color_list[i])

    def start_graph(self):
        coords = self.gui.layout.start_layout()
        for i in range(len(coords)):
            self.change_position_instantly2(coords[i], self.gui.drawTk.items_table.inverse[i + 1])

    def reingold_tilford_circular(self):
        coords = self.gui.layout.reingold_tilford_circular_layout()
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
        vertex_obj_index = int(vertex_obj.get_attribute("id")[1:])  # [1:] because id more than 1 digit
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
            position = self.gui.drawTk.set_weight_text_position(vertex_obj_index, "service_load", self.gui.mg)
            self.gui.canvas.coords(self.gui.drawTk.items_table[rectangle_index], position)
        items = self.gui.canvas.find_withtag("all")
        # print(len(items))
        # print(len(self.mg.vertex))
        # print(len(self.mg.edge))
        # print(source_list)
        # print(target_list)
        print("test")


def random_value(min_point: float, max_point: float, size: int):
    result = [random.uniform(min_point, max_point) for i in range(size)]
    return result
