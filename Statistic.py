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
        p.set_ylabel('Number of edges', fontsize=15)
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, parent)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        canvas.show()

class Statistic2(tk.Frame):
    def __init__(self, parent, controller, stat, attribute, hour):
        tk.Frame.__init__(self, parent)
        fig = Figure(figsize=(8, 4.5), dpi=200)
        ax = fig.add_subplot(111)
        self.p = fig.gca()

        self.statistic_dictionary = collections.Counter(x for x in stat if x < 1)
        print(self.statistic_dictionary.keys())
        print(self.statistic_dictionary.values())
        print(self.statistic_dictionary)
        self.statistic_dictionary = collections.OrderedDict(sorted(self.statistic_dictionary.items(), key=lambda t: t[0]))
        print(self.statistic_dictionary.keys())
        print(self.statistic_dictionary.values())
        print(self.statistic_dictionary)
        y_pos = np.arange(len(self.statistic_dictionary.keys()))  # Arrange bar position
        self.p.bar(y_pos, self.statistic_dictionary.values(), align='center', alpha=0.5)
        self.p.set_xticks(y_pos)
        self.p.set_xticklabels(self.statistic_dictionary.keys())
        self.p.set_ylabel('Number of edges', fontsize=15)
        self.p.set_xlabel('Statistic in hour {}'.format(hour), fontsize=15)

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, parent)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        canvas.show()


class StatisticPie(tk.Frame):
    def __init__(self, stat, attribute):
        self.statistic_dictionary = collections.Counter(x if x else "None" for x in stat)
        print(self.statistic_dictionary.keys())
        print(self.statistic_dictionary.values())
        print(self.statistic_dictionary)
        self.statistic_dictionary = collections.OrderedDict(
            sorted(self.statistic_dictionary.items(), key=lambda t: t[0]))
        keys = list(self.statistic_dictionary.keys())
        values = np.array(list(self.statistic_dictionary.values()))
        percent = 100.*values/values.sum()
        labels = ['{0} - {1:1.2f} % ({2})'.format(i,j,z) for i,j,z in zip(keys, percent, values)]
        colors = randomcolor(len(self.statistic_dictionary))
        patches, texts = plt.pie(values, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="upper left")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


class StatisticPie2(tk.Frame):
    def __init__(self, parent, stat, attribute, hour):
        tk.Frame.__init__(self, parent)
        fig = Figure(figsize=(8, 4.5), dpi=200)
        ax = fig.add_subplot(111)
        self.p = fig.gca()

        self.statistic_dictionary = collections.Counter(x for x in stat if x < 1)
        print(self.statistic_dictionary.keys())
        print(self.statistic_dictionary.values())
        print(self.statistic_dictionary)
        self.statistic_dictionary = collections.OrderedDict(
            sorted(self.statistic_dictionary.items(), key=lambda t: t[0]))
        print(self.statistic_dictionary.keys())
        print(self.statistic_dictionary.values())
        print(self.statistic_dictionary)
        # print(self.statistic_dictionary.keys())
        # print(self.statistic_dictionary.values())
        # print(self.statistic_dictionary)

        keys = list(self.statistic_dictionary.keys())
        values = np.array(list(self.statistic_dictionary.values()))
        percent = 100.*values/values.sum()
        labels = ['{0} - {1:1.2f} % ({2})'.format(i,j,z) for i,j,z in zip(keys, percent, values)]
        colors = randomcolor(len(self.statistic_dictionary))
        patches, texts = self.p.pie(values, labels=keys, labeldistance=1.04, colors=colors, startangle=90)
        self.p.legend(patches, labels, bbox_to_anchor=(0.16, 1.1))
        self.p.axis('equal')
        self.p.set_title("Throughput of the edges in the hour {}".format(hour))
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, parent)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        canvas.show()

def randomcolor(amount):
    colors = []
    reds = []
    blues = []
    greens = []
    reds.append(np.random.randint(255))
    blues.append(np.random.randint(255))
    greens.append(np.random.randint(255))
    for i in range(amount):
        red = np.random.randint(255)
        green = np.random.randint(255)
        blue = np.random.randint(255)
        while (np.math.fabs(reds[i] - red) < 80) & (np.math.fabs(blues[i] - blue) < 80) & (
                np.math.fabs(greens[i] - green) < 80):
            red = np.random.randint(255)
            green = np.random.randint(255)
            blue = np.random.randint(255)
        reds.append(red)
        blues.append(blue)
        greens.append(green)
        color = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
        colors.append(color)
    return colors