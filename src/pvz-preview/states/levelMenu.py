from .. import globals as glbls
from ..states import State

import math
import copy
import pandas as pd

from tkinter import ttk

class LevelMenu(State):
    def __init__(self, level: dict) -> None:
        super().__init__()

        self.__level = level

        self.__title = ttk.Label(self.frame, text=level["name"])
        self.__title.grid(column=0, row=0, columnspan=2)

        self.__iterations = ttk.Spinbox(self.frame, from_=1, to=math.inf, increment=1)
        self.__iterations.grid(column=0, row=1)

        self.__startBtn = ttk.Button(self.frame, text="Start", command=self.__runSim)
        self.__startBtn.grid(column=1, row=1)

        self.__backBtn = ttk.Button(self.frame, text="Back", command=self._switchBack)
        self.__backBtn.grid(column=0, row=2, columnspan=2)

    def __runSim(self) -> None:
        import pvz

        iterations = int(self.__iterations.get())
        IDs = self.__level["zombies"]
        waves = self.__level["waves"]
        zombieNames = [glbls.root.zombieIDs[i] for i in IDs]
        previewNames = list(map(lambda x: "Preview "+x, zombieNames))

        df = pd.DataFrame(index=range(iterations),
                          columns=list(zombieNames+previewNames),
                          dtype=float)

        for i in range(iterations):
            pvz.set_internal_spawn(copy.deepcopy(IDs))

            zombies = list(pvz.ReadMemory("int", 0x6a9ec0, 0x768, 0x6b4, array=waves*50))

            for k in range(waves):
                ignoreRest = False
                for j in range(50):
                    if (zombies[k * 50 + j] == -1):
                        ignoreRest = True
                        continue
                    if (ignoreRest):
                        zombies[k * 50 + j] = -1

            for k, val in enumerate(IDs):
                df.loc[i, zombieNames[k]] = zombies.count(val)

            preview = []
            zombiesCountMax = pvz.ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x94)
            zombiesOffset = pvz.ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x90)

            for k in range(zombiesCountMax): # type: ignore
                zombieDead = pvz.ReadMemory("bool", zombiesOffset + 0xec + j * 0x15c) # type: ignore
                if not zombieDead:
                    zombieType = pvz.ReadMemory("int", zombiesOffset + 0x24 + j * 0x15c) # type: ignore
                    preview.append((int)(zombieType)) # type: ignore

            for k, val in enumerate(IDs):
                df.loc[i, previewNames[k]] = preview.count(val)

        print(i)
        a = df.groupby(previewNames)
        print(a.size())
        print(a.aggregate("mean"))