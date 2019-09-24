from igraph import *
from ObjectTk.ObjectManager import *
from ObjectTk.ObjectDrawTkinter import *
import tkinter as tk
from ZoomAndDrag import *
from igraphNewModules import *
from DragObject import *


def test_redraw():
    imp_draw.canvas.delete("all")
    DrawTk.load_vertices()
    DrawTk.load_edges()

    print("OK")


def draw_circle():
    print("darw")
    #new_item = imp_draw.canvas.create_oval(imp_draw.do_scale(325,325), imp_draw.do_scale(370,370), fill="red")
    # imp_draw.do_scale(325,325)
    # imp_draw.do_scale(370,370)

def save_position():
    imp_draw.save_all_position(DrawTk.get_moved_center())

if __name__ == "__main__":
    test = tk.Tk()
    NREN = Graph.Read_GraphML("newNREN.graphml")
    mg = ObjManager(NREN)  # GET VERTICES AND EDGES FROM GRAPHML AND MAKE THEM OBJECTS
    # DrawTk = ObjDrawTkinter(0.06, 300, mg)

    mg.add_attribute("color", "red", True)
    mg.add_attribute("color", "gray", False)
    mg.add_attribute("vertex_size", 0.06, True)

    print(mg.vertex[0].list_attributes())
    print(mg.edge[0].list_attributes())

    # ADD DRAG AND ZOOM
    imp_draw = ZoomAndDrag(test, mg)  # THIS CLASS CREATE AND SETUP A WHOLE NEW CANVAS
    DrawTk = ObjDrawTkinter(300, mg, imp_draw)

    # print(DrawTk.transform_to_oval_position(mg.vertex[0], mg))
    # ADD DRAG OBJECTS
    mm = MouseMover(imp_draw, DrawTk.get_moved_center(), NREN, mg)

    # MOTION
    imp_draw.canvas.bind("<Button-3>", mm.select)
    imp_draw.canvas.bind("<B3-Motion>", mm.drag)
    imp_draw.canvas.bind("<Button-1>", imp_draw.move_start)
    imp_draw.canvas.bind("<B1-Motion>", imp_draw.move_move)
    imp_draw.canvas.bind("<Button-4>", imp_draw.zoomIn)
    imp_draw.canvas.bind("<Button-5>", imp_draw.zoomOut)

    # GENERATE COLOR BY WEIGHT
    DrawTk.group_vertex_color("GeoLocation", mg)

    # DISPLAY SHORTEST PATH
    print(get_path_vertices_object(NREN, 0, 1102))
    print(get_path_edge_object(NREN, 0, 1102))
    DrawTk.resize_vertex_list(get_path_vertices_object(NREN, 0, 1102), mg, 0.12)
    DrawTk.recolor_edge_list(get_path_edge_object(NREN, 0, 1102), mg, "#11fb09")

    # LOAD VERTICES AND EDGE FROM GRAPHML (Note: reverse draw edge before vertex for nice visual
    DrawTk.load_vertices()
    DrawTk.load_edges()

    imp_draw.pack(fill="both", expand=True)

    button = tk.Button(test, text="save", command=save_position)
    button2 = tk.Button(test, text="refresh", command=test_redraw)
    button.pack()
    button2.pack()

    test.mainloop()
