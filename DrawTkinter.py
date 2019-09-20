from igraph import *
import numpy as np
import tkinter as tk


class DrawTkinter:

    def __init__(self, radius, center, graph: Graph):
        graph.vs["vertex_size"] = radius
        self.center = center

    def rgb_2_hex(self, r, g, b):
        result = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        return result

    def get_moved_center(self):
        return self.center

    # Vertex utilities ################################################################################################
    def transform_to_oval_position(self, vertex: Graph.vs, graph: Graph):
        min_x = math.fabs(min(graph.vs["x"]))  # move the graph to all positive side
        min_y = math.fabs(min(graph.vs["y"]))  # move the graph to all positive side
        x = vertex["x"] + min_x + self.center \
            + vertex["vertex_size"]  # if vertex has center 0,0 then the graph will move to adapt this
        y = vertex["y"] + min_y + self.center + \
            vertex["vertex_size"]  # if vertex has center 0,0 then the graph will move to adapt this
        x1 = x - vertex["vertex_size"]
        y1 = y - vertex["vertex_size"]
        x2 = x + vertex["vertex_size"]
        y2 = y + vertex["vertex_size"]
        return [x1, y1, x2, y2]

    def group_vertex_color(self, vertex_weight: str, graph: Graph):
        the_list = graph.vs[vertex_weight]
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
        graph.vs["color"] = new_color

    def resize_vertex_list(self, vertex_list, graph: Graph, size):
        for i in vertex_list:
            graph.vs[i.index]["vertex_size"] = size

    def load_vertices(self, graph: Graph, tk_frame):
        for i in range(len(graph.vs)):
            # print(graph.vs[i]["x"])
            # print(transform_to_oval_position(graph.vs[i]["x"], graph.vs[i]["y"], 10))
            tk_frame.canvas.create_oval(self.transform_to_oval_position(graph.vs[i], graph),
                                        fill=graph.vs[i]["color"])

        return tk_frame

    # Edge utilities ##################################################################################################
    def transform_to_line_position(self, edge: Graph.es, graph: Graph):
        min_x = math.fabs(min(graph.vs["x"])) + self.center  # move the graph to all positive side
        min_y = math.fabs(min(graph.vs["y"])) + self.center  # move the graph to all positive side
        begin = [graph.vs[edge.source]["x"] + min_x + graph.vs[edge.source]["vertex_size"],
                 graph.vs[edge.source]["y"] + min_y + graph.vs[edge.source]["vertex_size"]]
        end = [graph.vs[edge.target]["x"] + min_x + graph.vs[edge.target]["vertex_size"],
               graph.vs[edge.target]["y"] + min_y + graph.vs[edge.target]["vertex_size"]]
        return begin, end

    def recolor_edge_list(self, edge_list, graph: Graph, color: str):
        for i in edge_list:
            graph.es[i.index]["color"] = color

    def load_edges(self, graph: Graph, tk_frame):
        for i in range(len(graph.es)):
            tk_frame.canvas.create_line(self.transform_to_line_position(graph.es[i], graph), fill=graph.es[i]["color"])
        return tk_frame
