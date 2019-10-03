from igraph import *


class VertexObj:
    def __init__(self, graph: Graph, index=None):
        properties_dict = {}
        if index is not None:
            for key in graph.vs[index].attribute_names():
                properties_dict.update({key: graph.vs[index][key]})
        self.properties = properties_dict

    def get_attribute(self, attribute_name: str):
        try:
            return self.properties[attribute_name]
        except KeyError:
            return None

    def add_attribute(self, attribute_name: str, value):
        self.properties.update({attribute_name: value})

    def set_attribute(self, attribute_name: str, value):
        self.properties[attribute_name] = value

    def list_attributes(self):
        return self.properties


class EdgeObj:
    def __init__(self, graph: Graph, index=None):
        properties_dict = {}
        if index is not None:
            for key in graph.es[index].attribute_names():
                properties_dict.update({key: graph.es[index][key]})
        properties_dict.update({"source": graph.es[index].source})
        properties_dict.update({"target": graph.es[index].target})
        self.properties = properties_dict

    def get_attribute(self, attribute_name: str):
        try:
            return self.properties[attribute_name]
        except KeyError:
            return None

    def add_attribute(self, attribute_name: str, value):
        self.properties.update({attribute_name: value})

    def set_attribute(self, attribute_name: str, value):
        self.properties[attribute_name] = value

    def list_attributes(self):
        return self.properties
