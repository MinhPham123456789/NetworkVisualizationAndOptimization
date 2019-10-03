import tkinter as tk
from tkinter import Label


class Note():
    x = 1520
    y = 0
    def __init__(self, master,note_dict,title):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.check = 0
        self.dict = note_dict
        self.title = title
        self.generate()

    def generate(self):
        self.list_key = []
        self.list_value = []
        self.xkey = self.ykey = 0
        for child in self.frame.winfo_children():
            child.destroy()

        if self.title == "edge_color":
            for key in self.dict:
                key_label = Label(self.frame, text = "att < " + str(key) )
                key_label1 = Label(self.frame,text = "from")
                key_label2 = Label(self.frame, text = "to")
                key_entry1 = Label(self.frame, bg = self.dict[key][0],padx=5)
                key_entry2 = Label(self.frame,bg = self.dict[key][1],padx=5)
                key_label.place(x=self.xkey,y=self.ykey)
                key_label1.place(x=self.xkey+160,y=self.ykey)
                key_label2.place(x=self.xkey+220,y=self.ykey)
                key_entry1.place(x=self.xkey+200,y=self.ykey)
                key_entry2.place(x=self.xkey+250,y=self.ykey)
                self.ykey +=30
            self.frame.config(height=self.ykey+30,width=400)
            return
        if self.title == "edge_width":
            for key in self.dict:
                key_label = Label(self.frame,text ="att < "+ str(key))
                key_label1 = Label(self.frame,text = "line width = " + str(self.dict[key]))
                key_label.place(x=self.xkey, y=self.ykey)
                key_label1.place(x=self.xkey+160,y= self.ykey)
                self.ykey += 30
                self.list_key.append(key_label)
            self.frame.config(height=self.ykey+30,width=400)

    def regenerate(self,note_dict):
        self.dict = note_dict
        for key in self.list_key:
            key.destroy()
        self.generate()

    def display(self):
        self.frame.place(x=Note.x,y=Note.y)
        self.x = Note.x
        self.y = Note.y
        Note.y += (self.ykey + 30)
        print(Note.y)

    def hideframe(self):
       self.frame.destroy()
       Note.y -= (self.ykey + 30)
       print(Note.y)

