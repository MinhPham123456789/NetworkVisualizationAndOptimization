from igraph import *
from ObjectTk.ObjectManager import *
from ObjectTk.ObjectDrawTkinter import *
from ObjectTk.ObjTkFrame import *
from ObjectTk.ObjTkLayout import GraphLayout
import tkinter as tk
from ZoomAndDrag import *
from igraphNewModules import *
from DragObject import *

from ObjectTk.ObjTkFrame import *
from GUI import *

import numpy as np
from GUI import *


# def test_redraw():
#     imp_draw.canvas.delete("all")
#     DrawTk.load_vertices()
#     DrawTk.load_edges()
#     DrawTk.load_vertex_load_weight("service_load", mg)
#
#     print("OK")

def a():
    pass
    # show_text_weight(text_weight_toggle)


def random_value(min_point: float, max_point: float, size: int):
    result = [random.uniform(min_point, max_point) for i in range(size)]
    return result


if __name__ == "__main__":
    test = tk.Tk()
    test.attributes("-zoomed", True)
    main_window = Window(test)
    test.mainloop()
