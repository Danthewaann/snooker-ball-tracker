import tkinter as tk
import tkinter.ttk as ttk
from collections import OrderedDict

class Navbar(ttk.Frame):
    def __init__(self, master=None):
        # super().__init__(master, bg="light gray", padx=20, pady=20)
        super().__init__(master, style="DB.TFrame", padding="20p")
        self.btns_frame = tk.Frame(master=self)
        self.btns = OrderedDict([
            ('select_file', tk.Button(
                self.btns_frame, text="Select File", command=self.master.select_file_onclick, height=1, width=15,
                font=self.master.fonts["h4"], cursor="hand2"
            )),
            ('quit', tk.Button(
                self.btns_frame, text="Quit", command=self.master.on_close, height=1, width=15,
                font=self.master.fonts["h4"], cursor="hand2"
            ))
        ])

        for btn in self.btns:
            self.btns[btn].pack(side="left")

        self.btns_frame.pack(anchor="center")
        self.pack(side="bottom", fill="x", anchor="s")