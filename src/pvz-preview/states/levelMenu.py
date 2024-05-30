from ..states import State

import math

from tkinter import ttk

class LevelMenu(State):
    def __init__(self, level: dict) -> None:
        super().__init__()

        self.__title = ttk.Label(self.frame, text=level["name"])
        self.__title.grid(column=0, row=0, columnspan=2)

        self.__iterations = ttk.Spinbox(self.frame, from_=1, to=math.inf, increment=1)
        self.__iterations.grid(column=0, row=1)

        self.__startBtn = ttk.Button(self.frame, text="Start", command=self.__runSim)
        self.__startBtn.grid(column=1, row=1)

        self.__backBtn = ttk.Button(self.frame, text="Back", command=self._switchBack)
        self.__backBtn.grid(column=0, row=2, columnspan=2)

    def __runSim(self) -> None:
        print(self.__iterations.get())