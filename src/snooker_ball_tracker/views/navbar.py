# from tkinter import *
# from tkinter.ttk import *
from collections import OrderedDict
from PyQt5.QtWidgets import *


class Navbar(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        

        # self.separator_hori = Separator(master=self, orient="horizontal")
        # self.btns_frame = Frame(master=self)
        # self.btns = OrderedDict([
        #     ('select_file', Button(
        #         self.btns_frame, text="Select File", command=self.master.master.select_file_onclick, cursor="hand2"
        #     )),
        #     ('load_settings', Button(
        #         self.btns_frame, text="Load Settings", command=self.master.master.load_settings, cursor="hand2"
        #     )),
        #     ('save_settings', Button(
        #         self.btns_frame, text="Save Settings", command=self.master.master.save_settings, cursor="hand2"
        #     )),
        #     ('quit', Button(
        #         self.btns_frame, text="Quit", command=self.master.master.on_close, cursor="hand2"
        #     ))
        # ])

        # for btn in self.btns:
        #     self.btns[btn].pack(side="left", fill="x", expand=True)

        # self.separator_hori.pack(side="top", fill="x", expand=True)
        # self.btns_frame.pack(anchor="center", padx=10, pady=10)
