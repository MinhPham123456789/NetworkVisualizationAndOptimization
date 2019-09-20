from igraph import *


def get_path_edge_object(graph, source, target):
    v_set = graph.get_shortest_paths(source, to=target, weights="bufferDelay", mode=ALL, output="vpath")
    #     print(v_set[0])
    v_set = set(v_set[0])
    s_path = graph.es.select(_source_in=v_set, _target_in=v_set)
    return s_path


def get_path_vertices_object(graph, source, target):
    v_set = graph.get_shortest_paths(source, to=target, weights="bufferDelay", mode=ALL, output="vpath")
    #     print(v_set[0])
    v_set = set(v_set[0])
    s_vertices = VertexSeq(graph, v_set)
    return s_vertices
