from igraph import *


class GraphLayout:
    def __init__(self, graph: Graph):
        self.graph = graph

    def start_layout(self):
        new_layout_coords = list(zip(self.graph.vs["x"], self.graph.vs["y"]))
        return new_layout_coords

    def reingold_tilford_circular_layout(self):
        new_layout_coords = self.graph.layout_reingold_tilford_circular()
        return new_layout_coords

