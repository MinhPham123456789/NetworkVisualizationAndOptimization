import tkinter as tk
import random
from ObjectTk.ObjectManager import *


class ZoomAndDrag(tk.Frame):
    def __init__(self, root, mg: ObjManager):
        tk.Frame.__init__(self, root)  # TODO: Consider remove this for better structure code
        self.canvas = tk.Canvas(self, width=900, height=900, background="white")
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.canvas.configure(scrollregion=(0, 0, 1000, 1000))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mg = mg
        self.scale = 1
        self.offset = 350
        self.current_scale = [self.offset, self.offset, self.scale, self.scale]

        self.offset_in = []  # Constructing
        self.offset_out = []  # Constructing
        self.scale_in = 2  # Constructing
        self.scale_out = 0.5  # Constructing
        # Plot some rectangles
        # for n in range(50):
        #     x0 = random.randint(0, 900)
        #     y0 = random.randint(50, 900)
        #     x1 = x0 + random.randint(50, 100)
        #     y1 = y0 + random.randint(50, 100)
        #     color = ("red", "orange", "yellow", "green", "blue")[random.randint(0, 4)]
        #     self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill=color, activefill="black", tags=n)
        # self.canvas.create_text(50, 10, anchor="nw", text="Click and drag to move the canvas\nScroll to zoom.")

        # This is what enables using the mouse:
        # self.canvas.bind("<ButtonPress-1>", self.move_start)
        # self.canvas.bind("<B1-Motion>", self.move_move)
        # linux scroll
        # self.canvas.bind("<Button-4>", self.zoomerP)
        # self.canvas.bind("<Button-5>", self.zoomerM)
        # windows scroll
        # self.canvas.bind("<MouseWheel>", self.zoomer)

    # move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # windows zoom
    # def zoomer(self, event):
    #     if (event.delta > 0):
    #         self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
    #     elif (event.delta < 0):
    #         self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
    #     self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # linux zoom
    def zoomerP(self, event):
        true_x = self.offset #self.canvas.canvasx(event.x)  # help zoom focus
        true_y = self.offset #self.canvas.canvasy(event.y)  # help zoom focus
        self.canvas.scale("all", true_x, true_y, self.scale_in, self.scale_in)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scale *= self.scale_in

        self.offset_in.append([true_x, true_y])  # Constructing

        self.current_scale = [self.offset, self.offset, self.scale, self.scale]

    def zoomerM(self, event):
        true_x = self.offset #self.canvas.canvasx(event.x)  # help zoom focus
        true_y = self.offset #self.canvas.canvasy(event.y)  # help zoom focus
        self.canvas.scale("all", true_x, true_y, self.scale_out, self.scale_out)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scale *= self.scale_out

        self.offset_out.append([true_x, true_y])  # Constructing

        self.current_scale = [self.offset, self.offset, self.scale, self.scale]

    # def get_current_scale(self):
    #     return self.current_scale

    # def get_scale_in(self):
    #     return self.scale_in
    #
    # def get_scale_out(self):
    #     return self.scale_out
    #
    # def get_offset_in(self):
    #     return self.offset_in
    #
    # def get_offset_out(self):
    #     return self.offset_out

    def zoomIn(self, event):
        true_x = self.canvas.canvasx(event.x)  # help zoom focus
        true_y = self.canvas.canvasy(event.y)  # help zoom focus
        items = self.canvas.find_withtag("all")

        for item in items:
            coords = self.canvas.coords(item)
            if len(coords) > 2:
                x1, y1, x2, y2 = coords
                x1 = x1 * self.scale_in - (true_x*self.scale_in - true_x)
                y1 = y1 * self.scale_in - (true_y*self.scale_in - true_y)
                x2 = x2 * self.scale_in - (true_x*self.scale_in - true_x)
                y2 = y2 * self.scale_in - (true_y*self.scale_in - true_y)
                self.canvas.coords(item, x1, y1, x2, y2)
            else:
                x, y = coords
                x = x * self.scale_in - (true_x * self.scale_in - true_x)
                y = y * self.scale_in - (true_y * self.scale_in - true_y)
                self.canvas.coords(item, x, y)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoomOut(self, event):
        true_x = self.canvas.canvasx(event.x)  # help zoom focus
        true_y = self.canvas.canvasy(event.y)  # help zoom focus
        items = self.canvas.find_withtag("all")

        for item in items:
            coords = self.canvas.coords(item)
            if len(coords) > 2:
                x1, y1, x2, y2 = coords
                x1 = x1 * self.scale_out - (true_x * self.scale_out - true_x)
                y1 = y1 * self.scale_out - (true_y * self.scale_out - true_y)
                x2 = x2 * self.scale_out - (true_x * self.scale_out - true_x)
                y2 = y2 * self.scale_out - (true_y * self.scale_out - true_y)
                self.canvas.coords(item, x1, y1, x2, y2)
            else:
                x, y = coords
                x = x * self.scale_out - (true_x * self.scale_out - true_x)
                y = y * self.scale_out - (true_y * self.scale_out - true_y)
                self.canvas.coords(item, x, y)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save_all_position(self, center_point):
        items = self.canvas.find_withtag("all")
        x_list = []
        y_list = []
        size_list = []
        for i in range(len(self.mg.vertex)):
            x1, y1, x2, y2 = self.canvas.coords(items[i])
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            radius_size = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            x_list.append(x - self.mg.vertex[i].get_attribute("vertex_size") - center_point)
            y_list.append(y - self.mg.vertex[i].get_attribute("vertex_size") - center_point)
            size_list.append(radius_size/4)
        self.mg.change_attribute_value_list("x", x_list, True)
        self.mg.change_attribute_value_list("y", y_list, True)
        self.mg.change_attribute_value_list("vertex_size", size_list, True)


    # def revert_scale(self, coord_x, coord_y):
    #     for offset_i in self.offset_in:
    #         coord_x = (coord_x - offset_i[0])/self.scale_in + offset_i[0]
    #         coord_y = (coord_y - offset_i[1])/self.scale_in + offset_i[1]
    #     for offset_o in self.offset_out:
    #         coord_x = (coord_x - offset_o[0])/self.scale_out + offset_o[0]
    #         coord_y = (coord_y - offset_o[1])/self.scale_out + offset_o[1]
    #     return coord_x, coord_y
    #
    # def do_scale(self, coord_x, coord_y):
    #     for offset_i in self.offset_in:
    #         coord_x = (coord_x - offset_i[0])*self.scale_in + offset_i[0]
    #         coord_y = (coord_y - offset_i[1])*self.scale_in + offset_i[1]
    #     for offset_o in self.offset_out:
    #         coord_x = (coord_x - offset_o[0])*self.scale_out + offset_o[0]
    #         coord_y = (coord_y - offset_o[1])*self.scale_out + offset_o[1]
    #     return coord_x, coord_y

#Debug zoom
    # print(items[0])
    # x1, y1, x2, y2 = self.canvas.coords(items[0])
    # x = (x1+x2)/2
    # y = (y1+y2)/2
    # # print("Test")
    # # print(x,y)
    # x1 = x1*self.scale_in - true_x
    # y1 = y1*self.scale_in - true_y
    # x2 = x2*self.scale_in - true_x
    # y2 = y2*self.scale_in - true_y
    # x = (x1 + x2) / 2
    # y = (y1 + y2) / 2
    # # print(x,y)
    # self.canvas.coords(items[0],x1,y1,x2,y2)