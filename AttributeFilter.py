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
        if "edge_width" in self.att_list:
            self.att_list.remove("edge_width")
        if "key" in self.att_list:
            self.att_list.remove("key")
        if "zorder" in self.att_list:
            self.att_list.remove("zorder")
        if "color" in self.att_list:
            self.att_list.remove("color")
        if "width" in self.att_list:
            self.att_list.remove("width")

    def filter_search(self):
        if self.is_vertex:
            self.vertex_filter()
            self.att_list.append("id")
        else:
            self.edge_filter()
            if "weight" in self.att_list:
                self.att_list.remove("weight")
        return self.att_list

    def filter_textbox(self):
        if self.is_vertex:
            if "color" in self.att_list:
                self.att_list.remove("color")
            if "vertex_size" in self.att_list:
                self.att_list.remove("vertex_size")
        else:
            pass
        return self.att_list

    def filter_width(self):
        if self.is_vertex:
            pass
        else:
            self.filter()
            if "LinkType" in self.att_list:
                self.att_list.remove("LinkType")
            if "LinkNote" in self.att_list:
                self.att_list.remove("LinkNote")
            if "LinkSpeedUnits" in self.att_list:
                self.att_list.remove("LinkSpeedUnits")
            if "label" in self.att_list:
                self.att_list.remove("label")
            if "LinkLabel" in self.att_list:
                self.att_list.remove("LinkLabel")
            if "source" in self.att_list:
                self.att_list.remove("source")
            if "target" in self.att_list:
                self.att_list.remove("target")
        return self.att_list

    def filter_statistic(self):
        if self.is_vertex:
            pass
        else:
            self.stat_filter()
        return self.att_list

    def stat_filter(self):
        if "weight" in self.att_list:
            self.att_list.remove("weight")
        if "LinkSpeedRaw" in self.att_list:
            self.att_list.remove("LinkSpeedRaw")
        if "bufferDelay" in self.att_list:
            self.att_list.remove("bufferDelay")
        if "tranmissionDelay" in self.att_list:
            self.att_list.remove("tranmissionDelay")
        if "propagationDelay" in self.att_list:
            self.att_list.remove("propagationDelay")
        if "source" in self.att_list:
            self.att_list.remove("source")
        if "target" in self.att_list:
            self.att_list.remove("target")
        if "edge_color" in self.att_list:
            self.att_list.remove("edge_color")
        if "edge_width" in self.att_list:
            self.att_list.remove("edge_width")
        if "key" in self.att_list:
            self.att_list.remove("key")
        if "zorder" in self.att_list:
            self.att_list.remove("zorder")
        if "color" in self.att_list:
            self.att_list.remove("color")
