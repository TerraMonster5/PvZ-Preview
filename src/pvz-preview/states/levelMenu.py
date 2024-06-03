from .. import globals as glbls
from ..states import State

import math
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

        name = self.__level["name"]

        levelID = (int(name.split("-")[0])-1)*10+int(name.split("-")[1])

        iterations = int(self.__iterations.get())
        IDs = self.__level["zombies"]
        waves = self.__level["waves"]
        zombieNames = [glbls.root.zombieIDs[i] for i in IDs]
        previewNames = list(map(lambda x: "Preview "+x, zombieNames))

        df = pd.DataFrame(index=range(iterations),
                          columns=list(zombieNames+previewNames),
                          dtype=float)
        
        pvz.WriteMemory("int", levelID, 0x6a9ec0, 0x82c, 0x24)

        for i in range(iterations):
            pvz.set_internal_spawn([z for z in IDs])
            pvz.Sleep(2)

            zombies = list(pvz.ReadMemory("int", 0x6a9ec0, 0x768, 0x6b4, array=waves*50))

            for j in range(waves):
                ignoreRest = False
                for k in range(50):
                    if zombies[j * 50 + k] == -1:
                        ignoreRest = True
                        continue
                    if ignoreRest:
                        zombies[j * 50 + k] = -1

            for l, val in enumerate(IDs):
                df.loc[i, zombieNames[l]] = zombies.count(val)

            preview = []
            zombiesCountMax = pvz.ReadMemory("unsigned int", 0x6a9ec0, 0x768, 0x94)
            zombiesOffset = pvz.ReadMemory("unsigned int", 0x6a9ec0, 0x768, 0x90)

            for m in range(zombiesCountMax): # type: ignore
                zombieDead = pvz.ReadMemory("bool", zombiesOffset + 0xec + m * 0x15c) # type: ignore
                if not zombieDead:
                    zombieType = pvz.ReadMemory("int", zombiesOffset + 0x24 + m * 0x15c) # type: ignore
                    preview.append(zombieType) # type: ignore

            for n, val in enumerate(IDs):
                df.loc[i, previewNames[n]] = preview.count(val)

        print(i)
        a = df.groupby(previewNames)
        print(a.size())
        print(a.aggregate("mean"))