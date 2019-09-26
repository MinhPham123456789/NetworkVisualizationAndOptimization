from igraph import *
from ObjectTk.ObjectManager import *
from ObjectTk.ObjectDrawTkinter import *
from ObjectTk.ObjTkFrame import *
from ObjectTk.ObjTkLayout import GraphLayout
import tkinter as tk
from ZoomAndDrag import *
from igraphNewModules import *
from DragObject import *
import numpy as np
from GUI import *


def test_redraw():
    imp_draw.canvas.delete("all")
    DrawTk.load_vertices()
    DrawTk.load_edges()
    DrawTk.load_vertex_load_weight("service_load", mg)

    print("OK")

def a():
    pass
    # show_text_weight(text_weight_toggle)

def toggle_text_weight():
    if text_weight_toggle:
        for i in range(len(mg.vertex)):
            index = "r" + str(i)
            imp_draw.canvas.itemconfigure(DrawTk.items_table[index], state=HIDDEN)
    else:
        for u in range(len(mg.vertex)):
            index = "r" + str(u)
            imp_draw.canvas.itemconfigure(DrawTk.items_table[index], state=NORMAL)
    # text_weight_toggle += 1
    print("toggle", text_weight_toggle)

def draw_circle():
    print("darw")



def save_position():
    imp_draw.save_all_position(DrawTk.get_moved_center())


def random_value(min_point: float, max_point: float, size: int):
    result = [random.uniform(min_point, max_point) for i in range(size)]
    return result

###GENERAL RULE PLOT ALL VERTICES AND VERTICES ATTRIBUTE BEFORE EDGES AND EDGES ATTRIBUTE###########

if __name__ == "__main__":
    test = tk.Tk()
    NREN = Graph.Read_GraphML("newNREN.graphml")
    mg = ObjManager(NREN)  # GET VERTICES AND EDGES FROM GRAPHML AND MAKE THEM OBJECTS
    imp_draw = ObjTkFrame(test)
    DrawTk = ObjDrawTkinter(300, mg, imp_draw)
    layout_class = GraphLayout(NREN)
    Window(imp_draw, DrawTk, mg, layout_class, test)      # GUI
    # DrawTk = ObjDrawTkinter(0.06, 300, mg)

    # TOGGLE VARIABLE
    text_weight_toggle = 1

    # GENERATE ADDITIONAL ATTRIBUTES
    mg.add_attribute("color", "red", True)
    mg.add_attribute("color", "gray", False)
    mg.add_attribute("vertex_size", 0.06, True)
    mg.add_attribute_list("service_load", random_value(0.0, 10.0, len(mg.vertex)), True)

    print(mg.vertex[0].list_attributes())
    print(mg.edge[0].list_attributes())

    # ADD DRAG AND ZOOM
    zm = ZoomAndDrag(imp_draw, mg)  # THIS CLASS CREATE AND SETUP A WHOLE NEW CANVAS

    # ADD DRAG OBJECTS
    mm = MouseMover(imp_draw, DrawTk, NREN, mg)

    # MOTION
    imp_draw.canvas.bind("<Button-3>", mm.select)
    imp_draw.canvas.bind("<B3-Motion>", mm.drag)
    imp_draw.canvas.bind("<Button-1>", zm.move_start)
    imp_draw.canvas.bind("<B1-Motion>", zm.move_move)
    imp_draw.canvas.bind("<Button-4>", zm.zoomIn)
    imp_draw.canvas.bind("<Button-5>", zm.zoomOut)

    # GENERATE COLOR BY WEIGHT
    # DrawTk.group_vertex_color("GeoLocation", mg)

    # DISPLAY SHORTEST PATH
    print(get_path_vertices_object(NREN, 0, 1102))
    print(get_path_edge_object(NREN, 0, 1102))
    DrawTk.resize_vertex_list(get_path_vertices_object(NREN, 0, 1102), mg, 0.12)
    DrawTk.recolor_edge_list(get_path_edge_object(NREN, 0, 1102), mg, "#11fb09")

    # LOAD VERTICES AND EDGE FROM GRAPHML (Note: reverse draw edge before vertex for nice visual
    DrawTk.load_vertices()
    DrawTk.load_edges()
    # DrawTk.load_vertex_text_weight("service_load")
    DrawTk.test()

    imp_draw.pack(fill="both", expand=True)

    # button = tk.Button(test, text="save", command=save_position)
    # button2 = tk.Button(test, text="refresh", command=test_redraw)
    # button3 = tk.Checkbutton(test, text="toggle_text", variable=text_weight_toggle, command=toggle_text_weight
    #                          , onvalue=1, offvalue=0)
    # button.pack()
    # button2.pack()
    # button3.pack()


    test.mainloop()
