from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
import collections
import numpy as np


class Statistic(tk.Frame):
    def __init__(self, parent, controller, stat, attribute):
        tk.Frame.__init__(self, parent)
        fig = Figure(figsize=(8, 4.5), dpi=200)
        ax = fig.add_subplot(111)
        p = fig.gca()
        statistic_dictionary = collections.Counter(x if x else "None" for x in stat)
        # print(statistic_dictionary.keys())
        # print(statistic_dictionary.values())
        # print(statistic_dictionary)
        y_pos = np.arange(len(statistic_dictionary.keys())) # Arrange bar position
        p.bar(y_pos, statistic_dictionary.values(), align='center', alpha=0.5)
        p.set_xticks(y_pos)
        p.set_xticklabels(statistic_dictionary.keys())
        p.set_ylabel('Occurrences', fontsize=15)
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, parent)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        canvas.show()
