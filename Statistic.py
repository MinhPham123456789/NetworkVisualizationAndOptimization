from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *


class Statistic(tk.Frame):
    def __init__(self, parent, controller, stat, attribute):
        tk.Frame.__init__(self, parent)
        fig = Figure(figsize=(8, 4.5), dpi=200)
        ax = fig.add_subplot(111)
        p = fig.gca()
        p.hist(stat, 100)
        p.set_xlabel('{}'.format(attribute), fontsize=15)
        p.set_ylabel('Frequency', fontsize=15)
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, parent)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        canvas.show()
