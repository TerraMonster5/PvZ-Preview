from . import widgets

import math
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from structs import stk

class FiftyPercent(tk.Toplevel):
    def __init__(self, cnf={}, **kwargs):
        kwargs = cnf or kwargs
        super().__init__(**kwargs)

        self.iconbitmap("assets/icon.ico")
        self.title("50% Rule")
        self.resizable(False, False)

        self.__toolbar = stk.ToolBar(self, tearoff=0)
        self.__toolbar.add_cascade("file", menukw={"tearoff": 0}, cascadekw={"label": "File"})
        self.__toolbar.file.add_command(label="Close", command=lambda: self.destroy()) # type: ignore
        self.__toolbar.file.add_command(label="Exit", command=lambda: exit()) # type: ignore
        self.config(menu=self.__toolbar)

        with open("zombieHealth.json", "r") as file:
            self.__healthDict = json.load(file)

        ttk.Label(self, text="Zombies").grid(row=0, column=0)

        self.__selector = widgets.ZombieSelector(self, options=list(self.__healthDict.keys()), max=8)
        self.__selector.bind("<<SelectedChanged>>", self.__lockFields)
        self.__selector.grid(row=1, rowspan=10, column=0, padx="2p", pady="2p", ipadx="1p", ipady="1p", sticky=tk.N)

        ttk.Label(self, text="Peas").grid(row=0, column=1)
        self.__peasDmgEntry = ttk.Entry(self)
        self.__peasDmgEntry.bind("<KeyRelease>", self.__lockFields)
        self.__peasDmgEntry.grid(row=1, column=1, pady="2p")

        ttk.Label(self, text="True Damage").grid(row=2, column=1)
        self.__trueDmgEntry = ttk.Entry(self)
        self.__trueDmgEntry.bind("<KeyRelease>", self.__lockFields)
        self.__trueDmgEntry.grid(row=3, column=1, pady="2p")

        ttk.Button(self, text="Calculate", command=lambda: self.__calculate()).grid(row=4, column=1)

        ttk.Label(self, text="True Damage needed for a chance to activate 50% rule:", width=30, wraplength=184, justify="center").grid(row=5, column=1)
        self.__lowerVar = tk.StringVar()
        self.__lowerOutput = ttk.Entry(self, state="readonly", textvariable=self.__lowerVar)
        self.__lowerOutput.grid(row=6, column=1, pady="2p")

        ttk.Label(self, text="True Damage needed to guarantee activation of 50% rule:", width=30, wraplength=184, justify="center").grid(row=7, column=1)
        self.__upperVar = tk.StringVar()
        self.__upperOutput = ttk.Entry(self, state="readonly", textvariable=self.__upperVar)
        self.__upperOutput.grid(row=8, column=1, pady="2p")

        ttk.Label(self, text="Chance of 50% rule activating:", width=30).grid(row=9, column=1)
        self.__chanceVar = tk.StringVar()
        self.__chanceOutput = ttk.Entry(self, state="readonly", textvariable=self.__chanceVar)
        self.__chanceOutput.grid(row=10, column=1, pady="2p")

        self.mainloop()
    
    def __calculate(self) -> None:
        if self.__peasDmgEntry["state"] == self.__trueDmgEntry["state"] == "disabled":
            messagebox.showerror("Error", "")

        selected = self.__selector.getRecords()
        if selected is None:
            return
        
        trueDmg = int(self.__peasDmgEntry.get())*20
        
        #trueDmg = int(self.__trueDmgEntry.get())
        deadHealth = sum((sum(self.__healthDict[key][x] for x in range(0, 3, 2))+self.__healthDict[key][1]*0.2)*value[1] for key, value in selected.items())
        totalHealth = sum((sum(self.__healthDict[key][x] for x in range(0, 3, 2))+self.__healthDict[key][1]*0.2)*sum(value) for key, value in selected.items())

        percentage = (trueDmg + deadHealth) / totalHealth

        self.__lowerVar.set(str(math.ceil(totalHealth*0.35)))
        self.__upperVar.set(str(math.ceil(totalHealth*0.5)))

        if percentage<0.35:
            self.__chanceVar.set("0%")
        elif percentage>0.5:
            self.__chanceVar.set("100%")
        else:
            self.__chanceVar.set(str(round(((percentage-0.35)/0.15)*100, 2))+"%")
    
    def __lockFields(self, event):
        selected = self.__selector.getSelected()

        if self.__peasDmgEntry.get() and any(zombie in selected for zombie in ("Newspaper", "Screen-Door", "Ladder")):
            self.__trueDmgEntry.config(state="enabled")
        elif self.__peasDmgEntry.get():
            self.__trueDmgEntry.config(state="disabled")
        else:
            self.__trueDmgEntry.config(state="enabled")


        if self.__trueDmgEntry.get() or any(zombie in selected for zombie in ("Newspaper", "Screen-Door", "Ladder")):
            self.__peasDmgEntry.config(state="disabled")
        else:
            self.__peasDmgEntry.config(state="enabled")