from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
except ImportError:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from igraph import *
import tkinter as tk
from tkinter import *


class GeoPage(tk.Frame):
    def __init__(self, parent, controler, graph_path):
        tk.Frame.__init__(self, parent)
        fig = Figure(figsize=(8, 4.5), dpi=200)
        ax = fig.add_subplot(111)
        g = read(graph_path)
        westlimit = 180
        southlimit = 85
        eastlimit = -180
        northlimit = -85
        for i in range(len(g.vs)):  # loop through every nodes
            lo, la = g.vs[i]["Longitude"], g.vs[i]["Latitude"]
            if westlimit > lo:
                westlimit = lo
            if southlimit > la:
                southlimit = la
            if eastlimit < lo:
                eastlimit = lo
            if northlimit < la:
                northlimit = la
        m = Basemap(projection='cyl', llcrnrlon=westlimit - 2, llcrnrlat=southlimit - 2, urcrnrlon=eastlimit + 2,
                    urcrnrlat=northlimit + 2, resolution='c', ax=ax)
        m.drawcoastlines()
        m.drawcountries()
        m.bluemarble()

        for i in range(len(g.es)):
            s, t = g.es[i].source, g.es[i].target
            x1, y1 = g.vs[s]["Longitude"], g.vs[s]["Latitude"]
            x2, y2 = g.vs[t]["Longitude"], g.vs[t]["Latitude"]
            x = m(x1, x2)
            y = m(y1, y2)
            ax.plot(x, y, linewidth=0.8, color='cyan', linestyle='-', zorder=1)

        for i in range(len(g.vs)):  # loop through every nodes
            lo, la = g.vs[i]["Longitude"], g.vs[i]["Latitude"]  # get x and y on i th node
            x, y = lo, la
            ax.scatter(x, y, marker='o', color='orange', zorder=2)
            ax.annotate(i, (x, y), size=7, ha='center', va='center')

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, parent)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

    def quit(self):
        self.quit()
        self.destroy()
