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

        self.__zombiesDropDown = ttk.Combobox(self, state="readonly", values=list(jsondict.keys()), width=15)
        self.__zombiesDropDown.bind("<<ComboboxSelected>>", self.__addZombie)
        self.__zombiesList = tk.LabelFrame(self, labelwidget=self.__zombiesDropDown)
        self.__zombiesList.grid(row=1, column=0, rowspan=10, padx="2p", pady="2p", ipadx="1p", ipady="1p")

        self.__free = 0

        ttk.Label(self.__zombiesList, text="Type").grid(row=0, column=0)
        ttk.Label(self.__zombiesList, text="Alive").grid(row=0, column=1)
        ttk.Label(self.__zombiesList, text="Dead").grid(row=0, column=2)

        self.__choices = [ttk.Label(self.__zombiesList, text=f"", width=15) for _ in range(8)]
        [x.grid(row=c+1, column=0) for c, x in enumerate(self.__choices)]

        self.__numFields = [[ttk.Spinbox(self.__zombiesList, from_=0, to=99, increment=1, width=3) for _ in range(2)] for _ in range(8)]
        [[wgt[c-1].grid(row=r+1, column=c) for c in range(1, 3)] for r, wgt in enumerate(self.__numFields)]

        # ttk.Label(self, text="Peas").grid(row=0, column=1)
        # ttk.Entry(self).grid(row=1, column=1)
        # ttk.Label(self, text="True Damage").grid(row=2, column=1)
        # ttk.Entry(self).grid(row=3, column=1)
        # ttk.Button(self, text="Calculate").grid(row=4, column=1)
        # ttk.Entry(self, state="disabled").grid(row=5, column=1)

        cancelIcon = tk.PhotoImage(file="assets/close.png").subsample(4, 4)

        temp = [tk.Button(self.__zombiesList, image=cancelIcon, relief="flat", overrelief="flat", bd=0, width=10) for r in range(8)]
        [wgt.grid(row=r+1, column=3) for r, wgt in enumerate(temp)]

        temp2 = widgets.ZombieSelector(self, options=list(jsondict.keys()), max=8)
        temp2.grid(row=1, column=1, padx="2p", pady="2p", ipadx="1p", ipady="1p")

        self.update()
        print(self.__numFields[0][0].winfo_width())

        self.mainloop()

    def __addZombie(self, event):
        if self.__free < len(self.__choices) and not self.__zombiesDropDown.get() in map(lambda x: x["text"], self.__choices):
            self.__choices[self.__free].config(text=self.__zombiesDropDown.get())
            self.__free += 1