import pandas as pd

import tkinter as tk
from tkinter import ttk

class PreviewFilter(tk.LabelFrame):
    def __init__(self, master, frame: pd.DataFrame, cnf: dict={}, **kwargs):
        kwargs = cnf or kwargs

        self.__label = ttk.Label(master, text="Filter")

        super().__init__(master, labelwidget=self.__label, **kwargs)

        self.grid_propagate(False)

        self.__headings: list[ttk.Label] = []
        self.__groups: list[list[ttk.Checkbutton | None]] = [[] for _ in range(len(self.__headings))]

        columns = frame.columns.values.tolist()
        [self.__headings.append(ttk.Label(self, text=col)) for col in columns[:len(columns)//2:]]

        for i, wgt in enumerate(self.__headings):
            wgt.grid(row=0, column=i)