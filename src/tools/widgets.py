import tkinter as tk
from tkinter import ttk

class ZombieSelector(tk.LabelFrame):
    def __init__(self,
                 master,
                 options: list=[],
                 max: int=10,
                 *args,
                 **kwargs) -> None:
        dropDown = ttk.Combobox(master, state="readonly", values=options, width=15)
        dropDown.bind("<<ComboboxSelected>>", self.__addZombie)

        super().__init__(master, labelwidget=dropDown)

        ttk.Label(self, text="Type").grid(row=0, column=0)
        ttk.Label(self, text="Alive").grid(row=0, column=1)
        ttk.Label(self, text="Dead").grid(row=0, column=2)
    
    def __addZombie(self, event):
        pass

    def __removeZombie(self):
        pass

    def __getRecords(self):
        pass