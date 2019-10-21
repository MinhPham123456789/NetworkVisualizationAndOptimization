from igraph import *
from ObjectTk.ObjectManager import ObjManager


class Centrality:
    def __init__(self, graph: Graph, mg: ObjManager):
        self.graph = graph
        self.mg = mg

    def edge_centrality(self, edge_weights: list):
        self.mg.add_attribute_list("centrality", self.graph.edge_betweenness(weights=edge_weights), False)

    def eigenvector_vertex_centrality(self, edge_weights: list):
        self.mg.add_attribute_list("centrality", self.graph.eigenvector_centrality(weights=edge_weights), True)

