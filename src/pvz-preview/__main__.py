from . import tools
from . import about

import structs
from structs import stk

import pathlib
import json
import functools
import math

import tkinter as tk
from tkinter import ttk

class Main(tk.Tk):
    def __init__(self, cnf: dict={}, **kwargs) -> None:
        kwargs = cnf or kwargs
        super().__init__(**kwargs)

        self.currentState = structs.Stack()

        self.iconbitmap("assets/icon.ico")
        self.geometry("600x600")
        self.title("PvZ Preview")

        self.__toolbar = stk.ToolBar(self, tearoff=0)
        self.__toolbar.add_cascade("file", menukw={"tearoff": 0}, cascadekw={"label": "File"})
        self.__toolbar.file.add_command(label="Open", command=lambda: ...) # type: ignore
        self.__toolbar.file.add_command(label="Open recent", command=lambda: ...) # type: ignore
        self.__toolbar.file.add_separator() # type: ignore
        self.__toolbar.file.add_command(label="Save as", command=lambda: ...) # type: ignore
        self.__toolbar.file.add_separator() # type: ignore
        self.__toolbar.file.add_command(label="Close", command=lambda: ...) # type: ignore
        self.__toolbar.file.add_command(label="Exit", command=lambda: exit()) # type: ignore
        self.__toolbar.add_cascade("tools", menukw={"tearoff": 0}, cascadekw={"label": "Tools"})
        self.__toolbar.tools.add_cascade("calculators", menukw={"tearoff": 0}, cascadekw={"label": "Calculators"}) # type: ignore
        self.__toolbar.tools.calculators.add_command(label="50% Rule", command=lambda: tools.FiftyPercent()) # type: ignore
        self.__toolbar.add_cascade("help", menukw={"tearoff": 0}, cascadekw={"label": "Help"})
        self.__toolbar.help.add_command(label="About", command=lambda: about.About()) # type: ignore
        self.config(menu=self.__toolbar)

class State:
    def __init__(self) -> None:
        self.frame = tk.Frame(root)
        self.frame.pack()
    
    def _switchBack(self) -> None:
        self.frame.destroy()
        root.currentState.pop()
        root.currentState.peek().frame.pack()

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

        self.__quitBtn = ttk.Button(self.frame, text="Exit", command=root.destroy)
        self.__quitBtn.grid(column=0, row=len(self.__adventureBtns)+1)
    
    def __switchAdventureMenu(self, filename):
        self.frame.pack_forget()
        root.currentState.push(AdventureMenu(filename))

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
        root.currentState.push(WorldMenu(world))

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
        root.currentState.push(LevelMenu(level))

class LevelMenu(State):
    def __init__(self, level: dict) -> None:
        super().__init__()

        self.__title = ttk.Label(self.frame, text=level["name"])
        self.__title.pack()

        self.__iterations = ttk.Spinbox(self.frame, from_=1, to=math.inf, increment=1)
        self.__iterations.pack()

        self.__startBtn = ttk.Button(self.frame, text="Start", command=self.__runSim)
        self.__startBtn.pack()

        self.__backBtn = ttk.Button(self.frame, text="Back", command=self._switchBack)
        self.__backBtn.pack()
    
    def __runSim(self) -> None:
        print(self.__iterations.get())

if __name__ == "__main__":
    root = Main()
    root.currentState.push(MainMenu())
    root.mainloop()