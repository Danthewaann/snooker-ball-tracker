from tkinter import *
from tkinter.ttk import *
from collections import OrderedDict

class Navbar(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, style="DB.TFrame", padding="10p")
        self.btns_frame = Frame(master=self)
        self.btns = OrderedDict([
            ('select_file', Button(
                self.btns_frame, text="Select File", command=self.master.master.select_file_onclick, cursor="hand2"
            )),
            ('quit', Button(
                self.btns_frame, text="Quit", command=self.master.master.on_close, cursor="hand2"
            ))
        ])

        for btn in self.btns:
            self.btns[btn].pack(side="left", fill="x", expand=True)

        self.btns_frame.pack(anchor="center")
