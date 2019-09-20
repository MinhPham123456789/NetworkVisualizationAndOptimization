from igraph import *


class Vertex:
    def __init__(self, graph:Graph, index):
        properties_dict = {}
        for key in graph.vs[index].attribute_names():
            properties_dict.update({key: graph.vs[index][key]})
        self.properties = properties_dict

    pass


class Edge:
    def __init__(self, graph:Graph, index):
        properties_dict = {}
        for key in graph.es[index].attribute_names():
            properties_dict.update({key: graph.es[index][key]})
        self.properties = properties_dict

    pass
