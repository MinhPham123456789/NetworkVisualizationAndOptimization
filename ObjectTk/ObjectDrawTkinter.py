from igraph import *
import numpy as np
from ObjectTk.ObjectManager import *
from ObjectTk.ObjectTkinter import *
from ZoomAndDrag import *
from bidict import bidict

class ObjDrawTkinter:
    def __init__(self, center, manager: ObjManager, tk_frame: ZoomAndDrag):
        self.center = center
        self.mg = manager
        self.tk_frame =tk_frame
        self.items_table = bidict()
        self.current_max = 0
        self.rectangle_switch = False

    def rgb_2_hex(self, r, g, b):
        result = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        return result

    def get_moved_center(self):
        return self.center

    def add_items_table(self, obj_list):
        for index in range(len(obj_list)):
            self.items_table[obj_list[index]] = index + 1 + self.current_max
        self.current_max = self.current_max + len(obj_list)

    def test(self):
        print(self.items_table)

    # Vertex utilities ################################################################################################
    def transform_to_oval_position(self, vertex: VertexObj, MG: ObjManager):
        min_x = math.fabs(min(MG.get_all_attribute_value("x", True)))  # move the graph to all positive side
        min_y = math.fabs(min(MG.get_all_attribute_value("y", True)))  # move the graph to all positive side
        x = vertex.get_attribute("x") + min_x + self.center \
            + vertex.get_attribute("vertex_size")  # if vertex has center 0,0 then the graph will move to adapt this
        y = vertex.get_attribute("y") + min_y + self.center + \
            vertex.get_attribute("vertex_size")  # if vertex has center 0,0 then the graph will move to adapt this
        x1 = x - vertex.get_attribute("vertex_size")
        y1 = y - vertex.get_attribute("vertex_size")
        x2 = x + vertex.get_attribute("vertex_size")
        y2 = y + vertex.get_attribute("vertex_size")
        # print(min_x,min_y)
        # print(x1,y1,x2,y2)
        # x1, y1 = self.tk_frame.do_scale(x1, y1)
        # x2, y2 = self.tk_frame.do_scale(x2, y2)
        return [x1, y1, x2, y2]

    def group_vertex_color(self, vertex_weight: str, MG: ObjManager):
        the_list = MG.get_all_attribute_value(vertex_weight, True)
        color_dict = {}
        unique_list = np.unique(the_list)
        print(len(unique_list))
        red = np.random.randint(255, size=len(unique_list))
        green = np.random.randint(255, size=len(unique_list))
        blue = np.random.randint(255, size=len(unique_list))
        for i in range(len(unique_list)):
            color = self.rgb_2_hex(red[i], green[i], blue[i])
            color_dict.update({unique_list[i]: color})
        new_color = []
        for key in the_list:
            new_color.append(color_dict[key])
        MG.change_attribute_value_list("color", new_color, True)

    def resize_vertex_list(self, vertex_list, MG: ObjManager, size):
        for i in vertex_list:
            MG.vertex[i.index].set_attribute("vertex_size", size)

    def set_weight_text_position(self, index: int, vertex_weight: str, mg: ObjManager):
        min_weight = min(mg.get_all_attribute_value(vertex_weight, True))
        max_weight = max(mg.get_all_attribute_value(vertex_weight, True))
        ratio = (mg.vertex[index].get_attribute(vertex_weight) - min_weight) / (max_weight - min_weight)
        coords = self.tk_frame.canvas.coords(self.items_table[mg.vertex[index]])
        height_mid = (coords[1] + coords[3]) / 2
        height_len = (height_mid - coords[1]) / 2
        width_mid = (coords[0] + coords[2]) / 2
        width_len = (width_mid - coords[0])*2
        position = [width_mid - width_len, coords[3], width_mid + width_len, coords[3] + height_len*2]
        print(position[0] - position[2], index)
        print(coords[0] - position[0], coords[2] - position[2])
        print((position[0] - position[2]) / (coords[0] - coords[2]))
        new = [width_mid, height_mid + height_len*3]
        return new

    def load_vertex_text_weight(self, vertex_weight: str):
        self.rectangle_switch = True
        min_weight = min(self.mg.get_all_attribute_value(vertex_weight, True))
        max_weight = max(self.mg.get_all_attribute_value(vertex_weight, True))
        items_table_list = []
        for index in range(len(self.mg.vertex)):
            ratio = (self.mg.vertex[index].get_attribute(vertex_weight) - min_weight) / (max_weight - min_weight)
            position = self.set_weight_text_position(index, vertex_weight, self.mg)
            if ratio > 0.8:
                self.tk_frame.canvas.create_text(position, fill="red",
                                                 text=str(round(self.mg.vertex[index].get_attribute(vertex_weight), 2)))
            else:
                self.tk_frame.canvas.create_text(position, fill="green",
                                                 text=str(round(self.mg.vertex[index].get_attribute(vertex_weight), 2)))
            items_table_list.append("r" + str(index))
        self.add_items_table(items_table_list)

    def load_vertices(self):
        for i in range(len(self.mg.vertex)):
            # print(graph.vs[i]["x"])
            # print(transform_to_oval_position(graph.vs[i]["x"], graph.vs[i]["y"], 10))
            self.tk_frame.canvas.create_oval(self.transform_to_oval_position(self.mg.vertex[i], self.mg),
                                        fill=self.mg.vertex[i].get_attribute("color"))
        self.add_items_table(self.mg.vertex)
        return self.tk_frame

    # Edge utilities ##################################################################################################
    def transform_to_line_position(self, edge: EdgeObj, MG: ObjManager):
        min_x = math.fabs(min(MG.get_all_attribute_value("x", True))) + self.center # move the graph to all positive side
        min_y = math.fabs(min(MG.get_all_attribute_value("y", True))) +self.center # move the graph to all positive side

        begin = [MG.vertex[edge.get_attribute("source")].get_attribute("x") + min_x +
                 MG.vertex[edge.get_attribute("source")].get_attribute("vertex_size"),
                 MG.vertex[edge.get_attribute("source")].get_attribute("y") + min_y +
                 MG.vertex[edge.get_attribute("source")].get_attribute("vertex_size")]
        end = [MG.vertex[edge.get_attribute("target")].get_attribute("x") + min_x +
               MG.vertex[edge.get_attribute("target")].get_attribute("vertex_size"),
               MG.vertex[edge.get_attribute("target")].get_attribute("y") + min_y +
               MG.vertex[edge.get_attribute("target")].get_attribute("vertex_size")]
        return begin, end

    def recolor_edge_list(self, edge_list, MG: ObjManager, color: str):
        for i in edge_list:
            MG.edge[i.index].set_attribute("color", color)

    def load_edges(self):
        for i in range(len(self.mg.edge)):
            self.tk_frame.canvas.create_line(self.transform_to_line_position(self.mg.edge[i], self.mg),
                                        fill=self.mg.edge[i].get_attribute("color"))
        self.add_items_table(self.mg.edge)
        return self.tk_frame
