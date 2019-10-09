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
        self.bins = 10
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

        # p.hist(stat,bins =50,range=[0, 2])
        # p.set_xlabel('{}'.format(attribute), fontsize=15)
        # p.set_ylabel('Frequency', fontsize=15)
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, parent)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        canvas.show()

    def update(self, stat):
        self.statistic_dictionary = collections.Counter(x if x else "None" for x in stat)

        # print(statistic_dictionary.keys())
        # print(statistic_dictionary.values())
        # print(statistic_dictionary)
        y_pos = np.arange(len(self.statistic_dictionary.keys()))  # Arrange bar position
        self.p.bar(y_pos, self.statistic_dictionary.values(), align='center', alpha=0.5)
        self.p.set_xticks(y_pos)
        self.p.set_xticklabels(self.statistic_dictionary.keys())

        # mv = smean.val
        # stdv = sstd.val
        # n_sample = round(sn.val)
        # nd = np.random.normal(loc=mv, scale=stdv, size=n_sample)
        # # Redraw histogram
        # ax.cla()
        # ax.hist(nd, normed=True, bins=n_bins0, alpha=0.5)
        # plt.draw()

    # def reset(self, event):
    #     bins.reset()


class StatisticPie(tk.Frame):
    def __init__(self, stat, attribute):
        # tk.Frame.__init__(self, parent)
        # self.bins = 10
        # fig = Figure(figsize=(8, 4.5), dpi=200)
        # ax = fig.add_subplot(111)
        # self.p = fig.gca()

        self.statistic_dictionary = collections.Counter(x if x else "None" for x in stat)
        print(self.statistic_dictionary.keys())
        print(self.statistic_dictionary.values())
        print(self.statistic_dictionary)
        self.statistic_dictionary = collections.OrderedDict(
            sorted(self.statistic_dictionary.items(), key=lambda t: t[0]))
        # print(self.statistic_dictionary.keys())
        # print(self.statistic_dictionary.values())
        # print(self.statistic_dictionary)
        # y_pos = np.arange(len(self.statistic_dictionary.keys()))  # Arrange bar position
        # self.p.bar(y_pos, self.statistic_dictionary.values(), align='center', alpha=0.5)
        # self.p.set_xticks(y_pos)
        # self.p.set_xticklabels(self.statistic_dictionary.keys())
        # self.p.set_ylabel('Number of edges', fontsize=15)
        # self.p.set_xlabel('Statistic in hour {}'.format(hour), fontsize=15)

        keys = list(self.statistic_dictionary.keys())
        values = np.array(list(self.statistic_dictionary.values()))
        percent = 100.*values/values.sum()
        labels = ['{0} - {1:1.2f} % ({2})'.format(i,j,z) for i,j,z in zip(keys, percent, values)]
        colors = self.randomcolor(len(self.statistic_dictionary))
        patches, texts = plt.pie(values, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

        # p.hist(stat,bins =50,range=[0, 2])
        # p.set_xlabel('{}'.format(attribute), fontsize=15)
        # p.set_ylabel('Frequency', fontsize=15)
        # canvas = FigureCanvasTkAgg(fig, parent)
        # canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        # toolbar = NavigationToolbar2TkAgg(canvas, parent)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        # canvas.show()

    def update(self, stat):
        self.statistic_dictionary = collections.Counter(x if x else "None" for x in stat)

        # print(statistic_dictionary.keys())
        # print(statistic_dictionary.values())
        # print(statistic_dictionary)
        y_pos = np.arange(len(self.statistic_dictionary.keys()))  # Arrange bar position
        self.p.bar(y_pos, self.statistic_dictionary.values(), align='center', alpha=0.5)
        self.p.set_xticks(y_pos)
        self.p.set_xticklabels(self.statistic_dictionary.keys())

        # mv = smean.val
        # stdv = sstd.val
        # n_sample = round(sn.val)
        # nd = np.random.normal(loc=mv, scale=stdv, size=n_sample)
        # # Redraw histogram
        # ax.cla()
        # ax.hist(nd, normed=True, bins=n_bins0, alpha=0.5)
        # plt.draw()

    # def reset(self, event):
    #     bins.reset()
    def randomcolor(self, amount):
        # colors = []
        # for i in range(amount):
        #     red = np.random.randint(255)
        #     green = np.random.randint(255)
        #     blue = np.random.randint(255)
        #     while (np.math.fabs(red - green) < 120) & (np.math.fabs(blue - green) < 120) & (np.math.fabs(red - blue) < 120):
        #         red = np.random.randint(255)
        #         green = np.random.randint(255)
        #         blue = np.random.randint(255)
        #     color = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
        #     colors.append(color)
        # return colors

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
            while (np.math.fabs(reds[i] - red) < 80) & (np.math.fabs(blues[i] - blue) < 80) & (np.math.fabs(greens[i] - green) < 80):
                red = np.random.randint(255)
                green = np.random.randint(255)
                blue = np.random.randint(255)
            reds.append(red)
            blues.append(blue)
            greens.append(green)
            color = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
            colors.append(color)
        return colors