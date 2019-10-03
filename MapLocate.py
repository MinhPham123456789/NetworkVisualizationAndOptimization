import tkinter
from tkinter import *
import webbrowser

import folium
from geopy.geocoders import Nominatim

import imageio
import matplotlib.pyplot as plt
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ObjectTk.ObjectManager import ObjManager
from ObjectTk.ObjectTkinter import *


class MapLocate:
    def __init__(self, vertexObj: VertexObj):
        self.vObj = vertexObj
        self.long = None
        self.lat = None
        self.x = None

    def get_mapimg(self):
        print("----MapLocate func open_map()----")
        self.long = self.vObj.get_attribute("Longitude")
        print(self.long)
        self.lat = self.vObj.get_attribute("Latitude")
        print(self.lat)
        self.x = self.vObj.get_attribute("x")
        print(self.x)

        url = "https://api.tomtom.com/map/1/staticimage?layer=basic&style=main&format=png&bbox=" \
              + str(self.long - 0.085) + "%2C" + str(self.lat - 0.085) + "%2C" + str(self.long + 0.085) + "%2C" + str(
            self.lat + 0.085) + \
              "&view=Unified&key=SJWHArGqdGBVv2e8illMpaY3ZMslTvqw"

        r = requests.get(url)
        print(r)
        im = imageio.imread(r.content)
        print(type(im))
        # self.open_imgwindow(im, mg)

    def open_imgwindow(self, im):
        window = Tk()
        window.wm_title("Map Location")
        fig = plt.figure(figsize=(50, 50))
        plt.imshow(im, extent=(self.long - 0.085, self.long + 0.085, self.lat - 0.085, self.lat + 0.085))
        plt.scatter(self.long, self.lat)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        mainloop()

    def get_map(self):
        print("----MapLocate func get_map()----")
        self.long = self.vObj.get_attribute("Longitude")
        print(self.long)
        self.lat = self.vObj.get_attribute("Latitude")
        print(self.lat)

        LDN_COORDINATES = [self.lat, self.long]
        myMap = folium.Map(location=LDN_COORDINATES, zoom_start=16, max_zoom=19)
        print(myMap)
        geolocator = Nominatim(timeout=10)
        s = str(self.lat) + "," + str(self.long)
        location = geolocator.reverse(s)
        address = location.address
        print(address)

        tooltip = 'View address!'
        address_html = '<i style="font-size:15px;">' + address + '</i>'
        folium.Marker([self.lat, self.long], popup=address_html, tooltip=tooltip).add_to(myMap)

        myMap.save('map.html')
        webbrowser.open('map.html')

        print("//----MapLocate func get_map()----")
