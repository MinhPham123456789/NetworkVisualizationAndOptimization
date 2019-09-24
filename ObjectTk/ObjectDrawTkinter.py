from igraph import *
import numpy as np
from ObjectTk.ObjectManager import *
from ObjectTk.ObjectTkinter import *
from ZoomAndDrag import *

class ObjDrawTkinter:
    def __init__(self, center, manager: ObjManager, tk_frame: ZoomAndDrag):
        self.center = center
        self.mg = manager
        self.tk_frame =tk_frame

    def rgb_2_hex(self, r, g, b):
        result = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        return result

    def get_moved_center(self):
        return self.center

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

    def load_vertices(self):
        for i in range(len(self.mg.vertex)):
            # print(graph.vs[i]["x"])
            # print(transform_to_oval_position(graph.vs[i]["x"], graph.vs[i]["y"], 10))
            self.tk_frame.canvas.create_oval(self.transform_to_oval_position(self.mg.vertex[i], self.mg),
                                        fill=self.mg.vertex[i].get_attribute("color"))
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
        return self.tk_frame
