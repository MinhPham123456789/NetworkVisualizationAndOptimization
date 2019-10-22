from igraph import *
import tkinter as tk
import numpy as np
from ObjectTk.ObjectManager import ObjManager
from ObjectTk.ObjectTkinter import *
from ZoomAndDrag import *
from bidict import bidict


class ObjDrawTkinter:
    def __init__(self, center, manager: ObjManager, tk_frame: tk.Frame):
        self.center = center
        self.mg = manager
        self.tk_frame = tk_frame
        self.items_table = bidict()
        self.current_max = 0
        self.rectangle_switch = False
        self.count_node = len(self.mg.vertex)
    @staticmethod
    def rgb_2_hex(r, g, b):
        result = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        return result

    def get_moved_center(self):
        return self.center

    def add_items_table(self, obj_list):
        for index in range(len(obj_list)):
            self.items_table[obj_list[index]] = index + 1 + self.current_max
        self.current_max = self.current_max + len(obj_list)

    def test(self):
        print(self.items_table)

    # Vertex utilities ################################################################################################
    def transform_to_oval_position(self, vertex: VertexObj, MG: ObjManager):
        # print("Vertex id: ", vertex.get_attribute("id"))
        # print("x y: ", vertex.get_attribute("x"), vertex.get_attribute("y"))
        min_x = math.fabs(min(MG.get_all_attribute_value("x", True)))  # move the graph to all positive side
        min_y = math.fabs(min(MG.get_all_attribute_value("y", True)))  # move the graph to all positive side
        x = vertex.get_attribute("x") + min_x + self.center \
            + vertex.get_attribute("vertex_size")  # if vertex has center 0,0 then the graph will move to adapt this
        y = vertex.get_attribute("y") + min_y + self.center + \
            vertex.get_attribute("vertex_size")  # if vertex has center 0,0 then the graph will move to adapt this
        x1 = x - vertex.get_attribute("vertex_size")
        y1 = y - vertex.get_attribute("vertex_size")
        x2 = x + vertex.get_attribute("vertex_size")
        y2 = y + vertex.get_attribute("vertex_size")
        # print(min_x,min_y)
        # print(x,y)
        # print("Size", vertex.get_attribute("vertex_size"))
        # print("After calculation:", x1,y1,x2,y2)
        return [x1, y1, x2, y2]

    def group_vertex_color(self, vertex_weight: str, MG: ObjManager):
        the_list = MG.get_all_attribute_value(vertex_weight, True)
        color_dict = {}
        unique_list = np.unique(the_list)
        red = np.random.randint(255, size=len(unique_list))
        green = np.random.randint(255, size=len(unique_list))
        blue = np.random.randint(255, size=len(unique_list))
        for i in range(len(unique_list)):
            color = self.rgb_2_hex(red[i], green[i], blue[i])
            color_dict.update({str(unique_list[i]): color})
        new_color = []
        for key in the_list:
            # print(color_dict[str(key)], key)
            new_color.append(color_dict[str(key)])
        MG.change_attribute_value_list("color", new_color, True)
        return [color_dict, new_color]

    def group_vertex_color_gradient(self, vertex_weight: str, MG):
        try:
            weight_list = list(map(float, MG.get_all_attribute_value(vertex_weight, True)))
        except ValueError:
            weight_list = list(map(str, MG.get_all_attribute_value(vertex_weight, True)))
        if isinstance(weight_list[0], str):
            tuple = self.edge_color_str(weight_list, MG)
            return tuple
        else:
            color_list = []
            maxweight = max(weight_list)
            minweight = min(weight_list)
            rangeweight = maxweight - minweight
            onethird = rangeweight / 3
            for i in range(len(MG.vertex)):
                if weight_list[i] < minweight + onethird:
                    percent = (weight_list[i] - minweight) / onethird
                    color = self.rgb_2_hex(0, 255, int(255 - 255 * percent))
                elif weight_list[i] < minweight + onethird * 2:
                    percent = (weight_list[i] - minweight - onethird) / onethird
                    color = self.rgb_2_hex(int(255 * percent), 255, 0)
                else:
                    percent = (weight_list[i] - minweight - onethird * 2) / onethird
                    color = self.rgb_2_hex(255, int(255 - percent * 255), 0)
                color_list.append(color)
            MG.change_attribute_value_list("color", color_list, True)
            threshold1 = float("{0:.2f}".format(onethird + minweight))
            threshold2 = float("{0:.2f}".format(onethird * 2 + minweight))
            threshold3 = float("{0:.2f}".format(onethird * 3 + minweight))
            color_dict = {threshold1: [self.rgb_2_hex(0, 255, 255), self.rgb_2_hex(0, 255, 0)],
                          threshold2: [self.rgb_2_hex(0, 255, 0), self.rgb_2_hex(255, 255, 0)],
                          threshold3: [self.rgb_2_hex(255, 255, 0), self.rgb_2_hex(255, 0, 0)]}
            return [color_dict, color_list]

    def recolor_vertex_list(self, vertex_obj_list: list, mg: ObjManager, color: str):
        for i in range(len(vertex_obj_list)):
            mg.vertex[i].set_attribute("color", color)
            self.tk_frame.canvas.itemconfigure(self.items_table[mg.vertex[i]], fill=color)


    def resize_vertex(self, vertex_obj, radius):
        x1, y1, x2, y2 = self.tk_frame.canvas.coords(self.items_table[vertex_obj])
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        nx1 = x - radius
        nx2 = x + radius
        ny1 = y - radius
        ny2 = y + radius
        return [nx1, ny1, nx2, ny2]

    def resize_vertex_list(self, size):
        for vertex_obj in self.mg.vertex:
            vertex_obj.set_attribute("vertex_size", size)
            self.tk_frame.canvas.coords(self.items_table[vertex_obj], self.resize_vertex(vertex_obj, size))

    def set_weight_text_position(self, index: int, mg: ObjManager):
        coords = self.tk_frame.canvas.coords(self.items_table[mg.vertex[index]])
        height_mid = (coords[1] + coords[3]) / 2
        height_len = (height_mid - coords[1]) / 2
        width_mid = (coords[0] + coords[2]) / 2
        width_len = (width_mid - coords[0]) * 2
        position = [width_mid - width_len, coords[3], width_mid + width_len, coords[3] + height_len * 2]
        # print(position[0] - position[2], index)
        # print(coords[0] - position[0], coords[2] - position[2])
        # print((position[0] - position[2]) / (coords[0] - coords[2]))
        new = [width_mid, height_mid + height_len * 3]
        return new

    def load_vertex_text_weight(self, vertex_weight: str):
        self.rectangle_switch = True
        # min_weight = min(self.mg.get_all_attribute_value(vertex_weight, True))
        # max_weight = max(self.mg.get_all_attribute_value(vertex_weight, True))
        items_table_list = []
        for index in range(len(self.mg.vertex)):
            position = self.set_weight_text_position(index, self.mg)
            self.tk_frame.canvas.create_text(position, fill="#96ff33",
                                             text=str(self.mg.vertex[index].get_attribute(vertex_weight)),
                                             state="hidden")
            items_table_list.append("r" + str(self.mg.vertex[index]))
        self.add_items_table(items_table_list)

    def add_vertex_text_weight(self, vertex : VertexObj):
        position = self.set_weight_text_position(self.mg.vertex.index(vertex), self.mg)
        self.tk_frame.canvas.create_text(position, fill="#96ff33",
                                         text=vertex.get_attribute("id"),
                                         state="hidden")
        self.add_items_table(["r"+str(vertex)])

    def delete_vertex_text_weight(self,vertex:VertexObj):
        self.tk_frame.canvas.delete(self.items_table["r" + str(vertex)])
        self.items_table.pop("r"+str(vertex))

    def change_vertex_text_weight(self, vertex_weight: str, canvas):
        for index in range(len(self.mg.vertex)):
            text_index = "r" + str(self.mg.vertex[index])
            text_item_index = self.items_table[text_index]
            print(index, text_index, text_item_index)
            canvas.itemconfigure(text_item_index,
                                 text=str(self.mg.vertex[index].properties[vertex_weight]),
                                 state="normal")

    def search_vertex_outline(self, vertex_obj_list, width_value, check_search):

        for vertex in vertex_obj_list:
            if check_search:
                self.tk_frame.canvas.itemconfigure(self.items_table[vertex], width=width_value, outline="#66fc09")
            else:
                self.tk_frame.canvas.itemconfigure(self.items_table[vertex], width=width_value, outline="black")

    def load_vertices(self):
        for i in range(len(self.mg.vertex)):
            # print(graph.vs[i]["x"])
            # print(transform_to_oval_position(graph.vs[i]["x"], graph.vs[i]["y"], 10))
            self.tk_frame.canvas.create_oval(self.transform_to_oval_position(self.mg.vertex[i], self.mg),
                                             fill=self.mg.vertex[i].get_attribute("color"))
        self.add_items_table(self.mg.vertex)
        return self.tk_frame

    # Edge utilities ##################################################################################################
    def transform_to_line_position(self, edge: EdgeObj, MG: ObjManager):
        min_x = math.fabs(min(MG.get_all_attribute_value("x", True))) + self.center  # move the graph to all positive side
        min_y = math.fabs(min(MG.get_all_attribute_value("y", True))) + self.center  # move the graph to all positive side

        begin = [MG.vertex[edge.get_attribute("source")].get_attribute("x") + min_x +
                 MG.vertex[edge.get_attribute("source")].get_attribute("vertex_size"),
                 MG.vertex[edge.get_attribute("source")].get_attribute("y") + min_y +
                 MG.vertex[edge.get_attribute("source")].get_attribute("vertex_size")]
        end = [MG.vertex[edge.get_attribute("target")].get_attribute("x") + min_x +
               MG.vertex[edge.get_attribute("target")].get_attribute("vertex_size"),
               MG.vertex[edge.get_attribute("target")].get_attribute("y") + min_y +
               MG.vertex[edge.get_attribute("target")].get_attribute("vertex_size")]
        return begin, end

    def recolor_edge_list(self, edge_list, MG: ObjManager, color: str):
        for i in range(len(edge_list)):
            MG.edge[i].set_attribute("color", color)
            self.tk_frame.canvas.itemconfigure(self.items_table[MG.edge[i]], fill=color)

    def recolor_edge_index_list(self, edge_index_list, MG: ObjManager, color: str):
        for i in edge_index_list:
            # MG.edge[i].set_attribute("color", color)
            self.tk_frame.canvas.itemconfigure(self.items_table[MG.edge[i]], fill=color)

    def recolor_edge_current(self):
        for one_edge in self.mg.edge:
            self.tk_frame.canvas.itemconfigure(self.items_table[one_edge], fill=one_edge.properties["color"])

    # handle clicked edge
    def visual_clicked_edge(self, edge: EdgeObj):
        prewidth =  self.tk_frame.canvas.itemcget(self.items_table[edge], "width")
        self.tk_frame.canvas.itemconfigure(self.items_table[edge], width = 13)
        return prewidth
    def free_clicked_edge(self, edge: EdgeObj, previous_width):
        self.tk_frame.canvas.itemconfigure(self.items_table[edge], width = previous_width)

        # handle the clicked node
    def visual_clicked_node(self, vertex_obj):
        preoutline = self.tk_frame.canvas.itemcget(self.items_table[vertex_obj], "outline")
        prewidth = self.tk_frame.canvas.itemcget(self.items_table[vertex_obj], "width")
        self.tk_frame.canvas.itemconfigure(self.items_table[vertex_obj], width=6, outline="white")
        return preoutline,prewidth
    def free_clicked_node(self, vertex_obj, preoutline,prewidth):
        self.tk_frame.canvas.itemconfigure(self.items_table[vertex_obj], width=prewidth, outline=preoutline)
    # change return value
    def group_edge_bandwidth(self, edge_weight: str, MG: ObjManager):
        the_list = list(map(float, MG.get_all_attribute_value(edge_weight, False)))
        min_weight = min(the_list)
        max_weight = max(the_list)
        threshold1 = (max_weight - min_weight) / 3 + min_weight
        threshold2 = (max_weight - min_weight) / 3 * 2 + min_weight
        width_dict = []
        for key in the_list:
            if key < threshold1:
                width_dict.append(1)
            elif key < threshold2:
                width_dict.append(3)
            else:
                width_dict.append(6)
        MG.add_attribute_list("width", width_dict, False)
        return [threshold1, threshold2, max_weight, width_dict]

    # change return value
    def edge_color(self, edge_weight: str, MG: ObjManager):
        try:
            weight_list = list(map(float, MG.get_all_attribute_value(edge_weight, False)))
        except ValueError:
            weight_list = list(map(str, MG.get_all_attribute_value(edge_weight, False)))
        if isinstance(weight_list[0], str):
            tuple = self.edge_color_str(weight_list, MG)
            return tuple
        else:
            color_list = []
            maxweight = max(weight_list)
            minweight = min(weight_list)
            rangeweight = maxweight - minweight
            onethird = rangeweight / 3
            for i in range(len(MG.edge)):
                if weight_list[i] < minweight + onethird:
                    percent = (weight_list[i] - minweight) / onethird
                    color = self.rgb_2_hex(0, 255, int(255 - 255 * percent))
                elif weight_list[i] < minweight + onethird * 2:
                    percent = (weight_list[i] - minweight - onethird) / onethird
                    color = self.rgb_2_hex(int(255 * percent), 255, 0)
                else:
                    percent = (weight_list[i] - minweight - onethird * 2) / onethird
                    color = self.rgb_2_hex(255, int(255 - percent * 255), 0)
                color_list.append(color)
            MG.change_attribute_value_list("color", color_list, False)
            threshold1 = float("{0:.2f}".format(onethird + minweight))
            threshold2 = float("{0:.2f}".format(onethird*2 + minweight))
            threshold3 = float("{0:.2f}".format(onethird*3 + minweight))
            color_dict = {threshold1:[self.rgb_2_hex(0,255,255),self.rgb_2_hex(0,255,0)],threshold2:[self.rgb_2_hex(0,255,0),self.rgb_2_hex(255,255,0)],threshold3:[self.rgb_2_hex(255,255,0),self.rgb_2_hex(255,0,0)]}
            return [color_dict, color_list]

    #def edge_color_string(self, edge_weight, MG: ObjManager):


    def edge_color_by_delay(self, MG: ObjManager):
        delay_list = []
        for edge in MG.edge:
            delay = edge.get_attribute("tranmissionDelay") + edge.get_attribute("bufferDelay") + edge.get_attribute(
                "propagationDelay")
            delay_list.append(delay)
        return delay_list

    def search_edge_dash(self, edge_obj_list, check_search):    #TODO: add color memory
        color_memory=[]
        width_memory=[]
        count = 0
        for edge in edge_obj_list:
            print(count)
            if check_search:
                color_memory.append(self.tk_frame.canvas.itemcget(self.items_table[edge], "fill"))
                width_memory.append(self.tk_frame.canvas.itemcget(self.items_table[edge], "width"))
                self.tk_frame.canvas.itemconfigure(self.items_table[edge], dash=(4, 4), width=9)
            else:
                self.tk_frame.canvas.itemconfigure(self.items_table[edge], dash=(),
                                                   width=self.width_memory[count])
            count = count + 1
        self.color_memory = color_memory
        self.width_memory = width_memory
        pass

    def load_edges(self):
        try:
            if self.mg.edge[0].get_attribute("width") is None:
                raise KeyError("Received None")
            else:
                for i in range(len(self.mg.edge)):
                    self.tk_frame.canvas.create_line(self.transform_to_line_position(self.mg.edge[i], self.mg),
                                                     fill=self.mg.edge[i].get_attribute("color"),
                                                     width=self.mg.edge[i].get_attribute("width"))
        except KeyError:
            for i in range(len(self.mg.edge)):
                self.tk_frame.canvas.create_line(self.transform_to_line_position(self.mg.edge[i], self.mg),
                                                 fill=self.mg.edge[i].get_attribute("color"),
                                                 width=2)
        self.add_items_table(self.mg.edge)
        return self.tk_frame

    def edge_color_str(self, weight_list, MG):
        color_dict = {}
        uniq_weight_list = np.unique(weight_list)
        red = np.random.randint(255, size=len(uniq_weight_list))
        green = np.random.randint(255, size=len(uniq_weight_list))
        blue = np.random.randint(255, size=len(uniq_weight_list))
        for i in range(len(uniq_weight_list)):
            color = self.rgb_2_hex(red[i], green[i], blue[i])
            color_dict.update({uniq_weight_list[i]: color})
        new_color = []
        for key in weight_list:
            new_color.append(color_dict[key])
        MG.change_attribute_value_list("color", new_color, False)
        return [color_dict, new_color]

    # create new vertex and add it to manager, items table, draw on canvas
    def add_new_vertex(self,xc,yc):
        new_vertex = VertexObj(None)
        new_vertex.set_attribute("id",self.count_node)
        new_vertex.set_attribute("color","red")
        new_vertex.set_attribute("Country", "New")
        new_vertex.set_attribute("Network", "New")
        new_vertex.set_attribute("label", "New")
        new_vertex.set_attribute("Internal", "0.0")
        new_vertex.set_attribute("asn", "New")
        new_vertex.set_attribute("Longitude", 0.0)
        new_vertex.set_attribute("Latitude", 0.0)
        new_vertex.set_attribute("x", xc)
        new_vertex.set_attribute("y", yc)
        self.mg.vertex.append(new_vertex)
        self.add_items_table([new_vertex])
        self.tk_frame.canvas.create_oval(xc-5,yc-5,xc+5,yc+5, fill = "red")
        self.count_node +=1
        self.add_vertex_text_weight(new_vertex)
        return new_vertex

    def add_new_edge(self,vertex1:VertexObj,vertex2:VertexObj):
        coord1 = self.tk_frame.canvas.coords(self.items_table[vertex1])
        coord2 = self.tk_frame.canvas.coords(self.items_table[vertex2])
        center_x1 = (coord1[0] + coord1[2]) / 2
        center_y1 = (coord1[1] + coord1[3]) / 2
        center_x2 = (coord2[0] + coord2[2]) / 2
        center_y2 = (coord2[1] + coord2[3]) / 2
        self.tk_frame.canvas.create_line(center_x1, center_y1, center_x2, center_y2,fill="white",width=2)
        self.tk_frame.canvas.lift(self.items_table[vertex1])
        self.tk_frame.canvas.lift(self.items_table[vertex2])
        new_edge = EdgeObj(None)
        new_edge.set_attribute("source",vertex1.get_attribute("id"))
        new_edge.set_attribute("target",vertex2.get_attribute("id"))
        new_edge.set_attribute("LinkType", "New")
        new_edge.set_attribute("LinkNote", "New")
        new_edge.set_attribute("LinkLabel", "New")
        new_edge.set_attribute("LinkSpeedRaw", 10000000000)
        new_edge.set_attribute("bufferDelay", 1)
        new_edge.set_attribute("tranmissionDelay", 1)
        new_edge.set_attribute("propagationDelay", 1.6)
        self.mg.edge.append(new_edge)
        self.add_items_table([new_edge])
        return new_edge

    def delete_vertex(self, vertex: VertexObj):
        list_edge = []
        for edge in self.mg.edge:
            if edge.get_attribute("source") == vertex.get_attribute("id") or edge.get_attribute("target") == vertex.get_attribute("id"):
                list_edge.append(edge)
        for edge in list_edge:
            self.delete_edge(edge)
        self.tk_frame.canvas.delete(self.items_table[vertex])
        self.items_table.pop(vertex)
        self.mg.vertex.remove(vertex)
        self.delete_vertex_text_weight(vertex)
        return vertex

    def delete_edge(self, edge: EdgeObj):
        self.tk_frame.canvas.delete(self.items_table[edge])
        self.items_table.pop(edge)
        self.mg.edge.remove(edge)
        return edge
