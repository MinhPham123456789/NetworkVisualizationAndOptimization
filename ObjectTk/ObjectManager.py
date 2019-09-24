from igraph import *
from ObjectTk.ObjectTkinter import *


class ObjManager:
    def __init__(self, graph: Graph = None):
        self.vertex = []
        self.edge = []
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
