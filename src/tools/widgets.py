import tkinter as tk
from tkinter import ttk

class ZombieSelector(tk.LabelFrame):
    def __init__(self,
                 master,
                 options: list=[],
                 max: int=10,
                 cnf={},
                 **kwargs) -> None:
        kwargs = cnf or kwargs

        dropDown = ttk.Combobox(master, state="readonly", values=options, width=15)
        dropDown.bind("<<ComboboxSelected>>", self.__addZombie)

        super().__init__(master, labelwidget=dropDown, width=184, height=max*20+42, **kwargs)

        self.grid_propagate(False)
        self.columnconfigure(1, minsize=37)
        self.columnconfigure(2, minsize=37)

        ttk.Label(self, text="Type", width=15, anchor="center").grid(row=0, column=0)
        ttk.Label(self, text="Alive").grid(row=0, column=1)
        ttk.Label(self, text="Dead").grid(row=0, column=2)
    
    def __addZombie(self, event) -> None:
        pass

    def __removeZombie(self) -> None:
        pass

    def __getRecords(self):
        pass