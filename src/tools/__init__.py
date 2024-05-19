from . import widgets

import json
import tkinter as tk
from tkinter import ttk

from structs import stk

class FiftyPercent(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.iconbitmap("assets/icon.ico")
        self.title("50% Rule")
        self.resizable(False, False)

        self.__toolbar = stk.ToolBar(self, tearoff=0)
        self.__toolbar.add_cascade("file", menukw={"tearoff": 0}, cascadekw={"label": "File"})
        self.__toolbar.file.add_command(label="Close", command=lambda: self.destroy()) # type: ignore
        self.__toolbar.file.add_command(label="Exit", command=lambda: exit()) # type: ignore
        self.config(menu=self.__toolbar)

        with open("zombieHealth.json", "r") as file:
            jsondict = json.load(file)

        ttk.Label(self, text="Zombies").grid(row=0, column=0)

        self.__selector = widgets.ZombieSelector(self, options=list(jsondict.keys()), max=8)
        self.__selector.grid(row=1, rowspan=10, column=0, padx="2p", pady="2p", ipadx="1p", ipady="1p")

        ttk.Label(self, text="Peas").grid(row=0, column=1)
        ttk.Entry(self).grid(row=1, column=1)
        ttk.Label(self, text="True Damage").grid(row=2, column=1)
        ttk.Entry(self).grid(row=3, column=1)
        ttk.Button(self, text="Calculate").grid(row=4, column=1)
        ttk.Entry(self, state="disabled").grid(row=5, column=1)

        self.mainloop()