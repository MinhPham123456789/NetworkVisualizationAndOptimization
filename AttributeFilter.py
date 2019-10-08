class AttFilter:
    def __init__(self, att_list: list, is_vertex: bool):
        self.att_list = att_list
        self.is_vertex = is_vertex

    def filter(self):
        if self.is_vertex:
            self.vertex_filter()
        else:
            self.edge_filter()
        return self.att_list

    def vertex_filter(self):
        print("-----AttributeFilter----")
        print(self.att_list)
        if "geocode_country" in self.att_list:
            self.att_list.remove("geocode_country")
        if "hyperedge" in self.att_list:
                self.att_list.remove("hyperedge")
        if "GeoLocation" in self.att_list:
                self.att_list.remove("GeoLocation")
        if "geocode_id" in self.att_list:
                self.att_list.remove("geocode_id")
        if "y" in self.att_list:
                self.att_list.remove("y")
        if "Longitude" in self.att_list:
                self.att_list.remove("Longitude")
        if "Latitude" in self.att_list:
                self.att_list.remove("Latitude")
        if "x" in self.att_list:
                self.att_list.remove("x")
        if "id" in self.att_list:
                self.att_list.remove("id")
        if "color" in self.att_list:
                self.att_list.remove("color")
        if "vertex_size" in self.att_list:
                self.att_list.remove("vertex_size")
        print(self.att_list)
        print("//-----AttributeFilter----")

    def edge_filter(self):
        if "edge_color" in self.att_list:
            self.att_list.remove("edge_color")
        if "LinkSpeedUnit" in self.att_list:
                self.att_list.remove("LinkSpeedUnit")
        if "edge_width" in self.att_list:
                self.att_list.remove("edge_width")
        if "key" in self.att_list:
                self.att_list.remove("key")
        if "zorder" in self.att_list:
                self.att_list.remove("zorder")
        if "color" in self.att_list:
                self.att_list.remove("color")