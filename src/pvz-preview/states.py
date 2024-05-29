from . import globals

import pathlib
import json
import functools
import math

import tkinter as tk
from tkinter import ttk

class State:
    def __init__(self) -> None:
        self.frame = tk.Frame(globals.root)
        self.frame.pack()

    def _switchBack(self) -> None:
        self.frame.destroy()
        globals.root.currentState.pop()
        globals.root.currentState.peek().frame.pack()

class MainMenu(State):
    def __init__(self) -> None:
        super().__init__()

        self.__title = ttk.Label(self.frame, text="PvZ Preview")
        self.__title.grid(column=0, row=0)

        adventures = [f.stem for f in pathlib.Path("adventures/").glob("*.json")]

        self.__adventureBtns = []

        for i, path in enumerate(adventures):
            with open(f"adventures/{path}.json", "r") as file: name = json.load(file)["name"]
            self.__adventureBtns.append(ttk.Button(self.frame, text=name, command=functools.partial(self.__switchAdventureMenu, f"{path}.json")))
            self.__adventureBtns[i].grid(column=0, row=i+1)

        self.__quitBtn = ttk.Button(self.frame, text="Exit", command=globals.root.destroy)
        self.__quitBtn.grid(column=0, row=len(self.__adventureBtns)+1)

    def __switchAdventureMenu(self, filename):
        self.frame.pack_forget()
        globals.root.currentState.push(AdventureMenu(filename))

class AdventureMenu(State):
    def __init__(self, filename: str) -> None:
        super().__init__()

        self.__worldBtns = []

        with open(f"adventures/{filename}", "r") as file:
            jsondict = json.load(file)

            self.__title = ttk.Label(self.frame, text=jsondict["name"])
            self.__title.grid(column=0, row=0)

            jsondict.pop("name")
            jsondict.pop("zombieIDs")

        for i, world in enumerate(jsondict.values()):
            self.__worldBtns.append(ttk.Button(self.frame, text=world["name"], command=functools.partial(self.__switchWorldMenu, world)))
            self.__worldBtns[i].grid(column=0, row=i+1)

        self.__backBtn = ttk.Button(self.frame, text="Back", command=self._switchBack)
        self.__backBtn.grid(column=0, row=len(self.__worldBtns)+1)

    def __switchWorldMenu(self, world: dict) -> None:
        self.frame.pack_forget()
        globals.root.currentState.push(WorldMenu(world))

class WorldMenu(State):
    def __init__(self, world: dict) -> None:
        super().__init__()

        self.__title = ttk.Label(self.frame, text=world["name"])
        self.__title.grid(column=0, row=0)

        self.__levelBtns = []

        for i, (key, level) in enumerate(world.items()):
            if key == "name":
                continue
            self.__levelBtns.append(ttk.Button(self.frame, text=level["name"], command=functools.partial(self.__switchLevelMenu, level)))
            self.__levelBtns[i-1].grid(column=0, row=i)

        self.__backBtn = ttk.Button(self.frame, text="Back", command=self._switchBack)
        self.__backBtn.grid(column=0, row=len(self.__levelBtns)+1)

    def __switchLevelMenu(self, level: dict) -> None:
        self.frame.pack_forget()
        globals.root.currentState.push(LevelMenu(level))

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