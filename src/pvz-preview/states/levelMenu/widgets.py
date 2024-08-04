import pandas as pd

import tkinter as tk
from tkinter import ttk

class PreviewFilter(tk.LabelFrame):
    def __init__(self, master, frame: pd.DataFrame, cnf: dict={}, **kwargs):
        kwargs = cnf or kwargs

        self.__label = ttk.Label(master, text="Filter")

        super().__init__(master, labelwidget=self.__label, **kwargs)

        self.__headings: list[ttk.Label] = []

        columns = frame.columns.values.tolist()
        mid = len(columns)//2
        zombs = columns[:mid:]
        previews = columns[mid::]

        [self.__headings.append(ttk.Label(self, text=col)) for col in zombs]

        self.__groups: list[list[tuple[ttk.Checkbutton, tk.BooleanVar]]] = [[] for _ in range(len(self.__headings))]

        byPreviews = frame.groupby(previews)
        self.__byPreviewsGroups = byPreviews.groups.keys()

        print(zombs, previews)

        options = {z: set() for z in zombs}
        for grp in self.__byPreviewsGroups:
            for i in range(len(previews)):
                options[zombs[i]].add(grp[i])
        
        for c, key in enumerate(options.keys()):
            options[key] = sorted(list(options[key])) # type: ignore
            for d, num in enumerate(options[key]):
                self.__groups[c].append((ttk.Checkbutton(self, text=str(int(num)), command=self.__updateCheckbuttons), tk.BooleanVar()))
                self.__groups[c][d][0].config(variable=self.__groups[c][d][1])

        for i, wgt in enumerate(self.__headings):
            wgt.grid(row=0, column=i)
        
        for e, col in enumerate(self.__groups):
            for f, tup in enumerate(col, 1):
                tup[0].grid(row=f, column=e)

        print(self.__groups)
    
    def __updateCheckbuttons(self):
        for _, col in enumerate(self.__groups):
            for _, tup in enumerate(col, 1):
                tup[0].grid_forget()
        
        checked: list = [-1 for _ in range(4)]

        for i, col in enumerate(self.__groups):
            for _, tup in enumerate(col, 1):
                if tup[1].get():
                    checked[i] = int(tup[0].cget("text"))
        
        # checked = [-1, 1, -1, 2]
        # self.__byPreviewsGroups = [[2, 1, 3, 2], [1, 2, 2, 2]]

        for i, col in enumerate(self.__groups):
            for e, tup in enumerate(col, 1):
                pass