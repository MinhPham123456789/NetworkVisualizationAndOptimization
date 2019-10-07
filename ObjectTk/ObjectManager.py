from igraph import *

from ObjectTk.ObjectTkinter import *
import tkinter as tk


class ObjManager:
    def __init__(self, graph: Graph = None):
        self.vertex = []
        self.edge = []
        self.graph = graph
        if graph is not None:
            for vertex in graph.vs:
                self.vertex.append(VertexObj(graph, vertex.index))
            for edge in graph.es:
                self.edge.append(EdgeObj(graph, edge.index))

    def add_attribute(self, attribute_name: str, value, is_vertex: bool):
        if is_vertex:
            for vertex in self.vertex:
                vertex.add_attribute(attribute_name, value)
        else:
            for edge in self.edge:
                edge.add_attribute(attribute_name, value)

    def add_attribute_list(self, attribute_name: str, value: list, is_vertex: bool):
        if is_vertex:
            for i in range(len(self.vertex)):
                self.vertex[i].add_attribute(attribute_name, value[i])
        else:
            for i in range(len(self.edge)):
                self.edge[i].add_attribute(attribute_name, value[i])

    def change_attribute(self, attribute_name: str, value, is_vertex: bool):
        if is_vertex:
            for vertex in self.vertex:
                vertex.set_attribute(attribute_name, value)
        else:
            for edge in self.edge:
                edge.set_attribute(attribute_name, value)

    def change_attribute_value_list(self, attribute_name: str, value: list, is_vertex: bool):
        if is_vertex:
            for i in range(len(self.vertex)):
                self.vertex[i].set_attribute(attribute_name, value[i])
        else:
            for i in range(len(self.edge)):
                self.edge[i].set_attribute(attribute_name, value[i])

    def get_all_attribute_value(self, attribute_name: str, is_vertex: bool):
        result = []
        if is_vertex:
            for vertex in self.vertex:
                result.append(vertex.get_attribute(attribute_name))
            return result

        else:
            for edge in self.edge:
                result.append(edge.get_attribute(attribute_name))
            return result

    def save_graph(self, drawTk, canvas_frame):
        for attribute in self.vertex[0].properties.keys():
            self.graph.vs[attribute] = self.get_all_attribute_value(attribute, True)
        for attribute2 in self.edge[0].properties.keys():
            self.graph.es[attribute2] = self.get_all_attribute_value(attribute2, False)
        for index in range(len(self.vertex)):
            x1, y1, x2, y2 = canvas_frame.coords(drawTk.items_table[self.vertex[index]])
            self.graph.vs[index]["x"] = ((x1 + x2) / 2 - drawTk.get_moved_center()) / 8
            self.graph.vs[index]["y"] = ((y1 + y2) / 2 - drawTk.get_moved_center()) / 8
        for edge_index in range(len(self.edge)):
            self.graph.es[edge_index]["color"] = canvas_frame.itemcget(drawTk.items_table[self.edge[edge_index]], "fill")
            # print(canvas_frame.itemcget(drawTk.items_table[self.edge[edge_index]], "fill"))
        return self.graph
