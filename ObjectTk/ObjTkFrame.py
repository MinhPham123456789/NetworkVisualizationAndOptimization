import tkinter as tk
from ObjectTk.ObjectManager import *


class ObjTkFrame(tk.Frame):
    def __init__(self, root, gui_canvas=None):
        # gui_canvas here is the gui canvas layer then we overlap the drawing canvas layer on it
        tk.Frame.__init__(self, root)  # TODO: Consider remove this for better structure code
        self.canvas = tk.Canvas(self, width=1100, height=980, background="#979a9a")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, 1600, 1600))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
