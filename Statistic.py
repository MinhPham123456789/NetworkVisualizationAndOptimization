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
        y_pos = np.arange(len(statistic_dictionary.keys()))  # Arrange bar position
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
        self.statistic_dictionary = collections.OrderedDict(
            sorted(self.statistic_dictionary.items(), key=lambda t: t[0]))
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

class Statistic3(tk.Frame):
    def __init__(self, parent, stat, mg, hour, threshold):
        tk.Frame.__init__(self, parent)
        fig = Figure(figsize=(8, 4.5), dpi=200)
        ax = fig.add_subplot(111)
        self.p = fig.gca()

        stat_dict = {}
        stat_dict_total = {}
        all_label = mg.get_all_attribute_value("LinkLabel", False)
        all_label = set(all_label)
        print(all_label)
        for u in all_label:
            stat_dict.update({u: 0})
            stat_dict_total.update({u: 0})
        for i in range(len(stat)):
            stat_dict_total[mg.edge[i].properties["LinkLabel"]] = stat_dict_total[mg.edge[i].properties["LinkLabel"]] + 1
            if stat[i] >= threshold:
                stat_dict[mg.edge[i].properties["LinkLabel"]] = stat_dict[mg.edge[i].properties["LinkLabel"]] + 1

        stat_dict = collections.OrderedDict(
            sorted(stat_dict.items(), key=lambda t: t[0]))
        stat_dict_total = collections.OrderedDict(
            sorted(stat_dict_total.items(), key=lambda t: t[0]))
        print("stat_dict", stat_dict)
        print("stat_dict_total", stat_dict_total)

        y_pos = np.arange(len(stat_dict.keys()))  # Arrange bar position
        y_pos_total = np.arange(len(stat_dict_total.keys())) + 0.09
        self.p.bar(y_pos_total, stat_dict_total.values(), align='center', alpha=0.8, color="green")
        self.p.bar(y_pos, stat_dict.values(), align='center', alpha=0.8)
        self.p.set_xticks(y_pos)
        self.p.set_xticklabels(stat_dict.keys())
        self.p.set_ylabel('Number of edges', fontsize=15)
        self.p.set_xlabel("Number of edges with high throughput group by LinkLabel in the hour {0}, threshold {1}"
                          .format(hour, threshold), fontsize=10)
        self.p.legend(["Total number of edges", "Number of edges with high throughput"],fontsize="small",
                      bbox_to_anchor=(0.3, 1.16))

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, parent)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        canvas.show()

class StatisticPie:
    def __init__(self, stat, attribute):
        self.statistic_dictionary = collections.Counter(x if x else "None" for x in stat)
        print(self.statistic_dictionary.keys())
        print(self.statistic_dictionary.values())
        print(self.statistic_dictionary)
        self.statistic_dictionary = collections.OrderedDict(
            sorted(self.statistic_dictionary.items(), key=lambda t: t[0]))
        keys = list(self.statistic_dictionary.keys())
        values = np.array(list(self.statistic_dictionary.values()))
        percent = 100. * values / values.sum()
        labels = ['{0} - {1:1.2f} % ({2})'.format(i, j, z) for i, j, z in zip(keys, percent, values)]
        colors = random_color(len(self.statistic_dictionary))
        patches, texts = plt.pie(values, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="upper left")
        plt.axis('equal')
        plt.tight_layout()
        plt.title("Group edges by {}".format(attribute))
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

        keys = list(self.statistic_dictionary.keys())
        values = np.array(list(self.statistic_dictionary.values()))
        percent = 100. * values / values.sum()
        labels = ['{0} - {1:1.2f} % ({2})'.format(i, j, z) for i, j, z in zip(keys, percent, values)]
        colors = random_color(len(self.statistic_dictionary))
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

class StatisticPie3(tk.Frame):
    def __init__(self, parent, stat, mg, hour, threshold):
        tk.Frame.__init__(self, parent)
        fig = Figure(figsize=(8, 4.5), dpi=200)
        ax = fig.add_subplot(111)
        self.p = fig.gca()
        stat_dict = {}
        all_label = mg.get_all_attribute_value("LinkLabel", False)
        all_label = set(all_label)
        print(all_label)
        for u in all_label:
            stat_dict.update({u: 0})
        for i in range(len(stat)):
            if stat[i] >= threshold:
                stat_dict[mg.edge[i].properties["LinkLabel"]] = stat_dict[mg.edge[i].properties["LinkLabel"]] + 1

        stat_dict = collections.OrderedDict(
            sorted(stat_dict.items(), key=lambda t: t[0]))
        print(stat_dict)
        keys = list(stat_dict.keys())
        values = np.array(list(stat_dict.values()))
        percent = 100. * values / values.sum()
        labels = ['{0} - {1:1.2f} % ({2})'.format(i, j, z) for i, j, z in zip(keys, percent, values)]
        colors = random_color(len(stat_dict))
        patches, texts = self.p.pie(values, labels=keys, labeldistance=1.04, colors=colors, startangle=90)
        self.p.legend(patches, labels, bbox_to_anchor=(0.2, 1))
        self.p.axis('equal')
        self.p.set_title("Number of edges with high throughput group by LinkLabel in the hour {0}, threshold {1}"
                         .format(hour, threshold))
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, parent)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        canvas.show()


def random_color(amount):
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
