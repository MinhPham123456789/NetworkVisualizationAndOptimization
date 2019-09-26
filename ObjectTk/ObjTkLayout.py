from igraph import *


class GraphLayout:
    def __init__(self, graph: Graph):
        self.graph = graph

    def reingold_tilford_circular_layout(self):
        new_layout_coords = self.graph.layout_reingold_tilford_circular()
        return new_layout_coords

