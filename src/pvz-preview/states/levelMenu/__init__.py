from . import widgets
from ... import globals as glbls
from ...states import State

import math
import pandas as pd
import threading

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class LevelMenu(State):
    def __init__(self, level: dict) -> None:
        super().__init__()

        self.__level = level

        for x in range(6):
            self.frame.columnconfigure(x, minsize=100)

        self.__title = ttk.Label(self.frame, text=level["name"])
        self.__title.grid(column=0, row=0, columnspan=6)

        self.__iterations = ttk.Spinbox(self.frame, from_=1, to=math.inf, increment=1)
        self.__iterations.grid(column=0, row=1, columnspan=2, sticky=tk.E)

        self.__untilFound = tk.BooleanVar()
        self.__untilFoundCheck = ttk.Checkbutton(self.frame, text="Repeat Until Found", variable=self.__untilFound, command=self.__untilFoundToggle)
        self.__untilFoundCheck.grid(column=2, row=1, columnspan=2)

        self.__startBtn = ttk.Button(self.frame, text="Start", command=self.__runSim)
        self.__startBtn.grid(column=4, row=1, columnspan=2, sticky=tk.W)

        self.__pastBtn = ttk.Button(self.frame, text="View Past Results")
        self.__pastBtn.grid(column=3, row=3, columnspan=2)

        self.__backBtn = ttk.Button(self.frame, text="Back", command=self._switchBack)
        self.__backBtn.grid(column=0, row=6, columnspan=6)

        self.__clearBtn = ttk.Button(self.frame, text="Clear Results", command=self.__clearResults)
    
    def __untilFoundToggle(self) -> None:
        if self.__untilFound.get():
            self.__iterations.state(["disabled"])
        else:
            self.__iterations.state(["!disabled"])

    def __runSim(self) -> None:
        self.__startBtn.state(["disabled"])
        self.__clearBtn.grid_forget()

        try:
            self.__filter.destroy()
        except AttributeError:
            pass

        self.__simThread = threading.Thread(target=self.__simulation, daemon=True)
        self.__simThread.start()

    def __simulation(self) -> None:
        import pvz

        name = self.__level["name"]

        levelID = (int(name.split("-")[0])-1)*10+int(name.split("-")[1])

        iterations = int(self.__iterations.get())
        IDs = self.__level["zombies"]
        waves = self.__level["waves"]
        zombieNames = [glbls.root.zombieIDs[i] for i in IDs]
        previewNames = list(map(lambda x: "Preview "+x, zombieNames))

        self.__previews = pd.DataFrame(index=range(iterations),
                                       columns=list(zombieNames+previewNames),
                                       dtype=float)

        pvz.WriteMemory("int", levelID, 0x6a9ec0, 0x82c, 0x24)

        for i in range(iterations):
            # if cancel: break

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
                self.__previews.loc[i, zombieNames[l]] = zombies.count(val)

            preview = []
            zombiesCountMax = pvz.ReadMemory("unsigned int", 0x6a9ec0, 0x768, 0x94)
            zombiesOffset = pvz.ReadMemory("unsigned int", 0x6a9ec0, 0x768, 0x90)

            for m in range(zombiesCountMax): # type: ignore
                zombieDead = pvz.ReadMemory("bool", zombiesOffset + 0xec + m * 0x15c) # type: ignore
                if not zombieDead:
                    zombieType = pvz.ReadMemory("int", zombiesOffset + 0x24 + m * 0x15c) # type: ignore
                    preview.append(zombieType) # type: ignore

            for n, val in enumerate(IDs):
                self.__previews.loc[i, previewNames[n]] = preview.count(val)

        self.__groupedPreviews = self.__previews.groupby(previewNames)
        print(self.__groupedPreviews.size())
        print(self.__groupedPreviews.aggregate("mean"))

        columns = self.__previews.columns.values.tolist()
        previews = columns[len(columns)//2::]

        self.__filter = widgets.PreviewFilter(self.frame, label="Filter", columns=columns,
                                              groupedValues=self.__previews.groupby(previews).groups.keys())
        self.__filter.grid(row=2, column=0, columnspan=6)

        self.__clearBtn.grid(column=0, row=5, columnspan=6)
        self.__startBtn.state(["!disabled"])
    
    def __clearResults(self) -> None:
        if messagebox.askokcancel("Continue?", message="Do you wish to continue? (Results will be deleted permanently!)"):
            self.__filter.destroy()
            self.__clearBtn.grid_forget()
    
    def _switchBack(self) -> None:
        if hasattr(self, "_LevelMenu__simThread") and self.__simThread.is_alive():
            messagebox.showwarning(message="Please wait for simulation to conclude!")
            return
        super()._switchBack()