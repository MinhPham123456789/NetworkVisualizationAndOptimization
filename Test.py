from DrawTkinter import *
from ZoomAndDrag import *
from igraph import *
import tkinter as tk
from igraphNewModules import *
from DragObject import *

if __name__ == "__main__":
    # PREPARATION
    NREN = Graph.Read_GraphML("newNREN.graphml")
    test = tk.Tk()
    DrawTk = DrawTkinter(0.06, 350, NREN)
    NREN.vs["color"] = "red"
    NREN.es["color"] = "gray"

    # ADD DRAG AND ZOOM
    imp_draw = ZoomAndDrag(test)    # THIS CLASS CREATE AND SETUP A WHOLE NEW CANVAS

    # ADD DRAG OBJECTS
    mm = MouseMover(imp_draw.canvas, DrawTk.get_moved_center(), NREN)

    # MOTION
    imp_draw.canvas.bind("<Button-3>", mm.select)
    imp_draw.canvas.bind("<B3-Motion>", mm.drag)
    imp_draw.canvas.bind("<Button-1>", imp_draw.move_start)
    imp_draw.canvas.bind("<B1-Motion>", imp_draw.move_move)
    imp_draw.canvas.bind("<Button-4>", imp_draw.zoomerP)
    imp_draw.canvas.bind("<Button-5>", imp_draw.zoomerM)

    # GENERATE COLOR BY WEIGHT
    DrawTk.group_vertex_color("GeoLocation", NREN)

    # DISPLAY SHORTEST PATH
    print(get_path_vertices_object(NREN, 0, 1102))
    print(get_path_edge_object(NREN, 0, 1102))
    DrawTk.resize_vertex_list(get_path_vertices_object(NREN, 0, 1102), NREN, 0.12)
    DrawTk.recolor_edge_list(get_path_edge_object(NREN, 0, 1102), NREN, "#11fb09")

    # LOAD VERTICES AND EDGE FROM GRAPHML (Note: reverse draw edge before vertex for nice visual
    DrawTk.load_vertices(NREN, imp_draw)
    DrawTk.load_edges(NREN, imp_draw)

    print(NREN.vs[0]["x"], NREN.vs[0]["y"])

    # DRAW
    imp_draw.pack(fill="both", expand=True)
    test.mainloop()




    #
    # print(NREN.es[0].source)
    # print(NREN.es[0].target)

    # coord = -10, -10, 100,100
    # oval = C.create_oval(coord, fill='red')
    # line = C.create_line([10,10],[200,200],fill = 'green')
    # C.pack()
    # test.mainloop()
