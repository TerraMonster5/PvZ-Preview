import pathlib
import json
import functools

import structs

import tkinter as tk
from tkinter import ttk

class Main(tk.Tk):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)

        self.currentState = structs.SimpleStack()

        self.geometry("600x600")
        self.title("PvZ Preview")

class State:
    def __init__(self):
        self.frame = tk.Frame(root)
        self.frame.pack()

class MainMenu(State):
    def __init__(self):
        super().__init__()

        self.__title = ttk.Label(self.frame, text="PvZ Preview")
        self.__title.grid(column=0, row=0)

        worlds = [f.stem for f in pathlib.Path("adventures/").glob("*.json")]
        
        self.__worldBtns = []

        for i, path in enumerate(worlds):
            with open(f"adventures/{path}.json", "r") as file: name = json.load(file)["name"]
            self.__worldBtns.append(ttk.Button(self.frame, text=name, command=functools.partial(self.__switchAdventureMenu, f"{path}.json")))
            self.__worldBtns[i].grid(column=0, row=i+1)

        self.__quitBtn = ttk.Button(self.frame, text="Quit", command=root.destroy)
        self.__quitBtn.grid(column=0, row=len(self.__worldBtns)+1)
    
    def __switchAdventureMenu(self, filename):
        self.frame.pack_forget()
        root.currentState.push(AdventureMenu(filename))

class AdventureMenu(State):
    def __init__(self, filename):
        super().__init__()

        self._filename = filename

        self.__levelBtns = []

        with open(f"adventures/{filename}", "r") as file:
            jsondict = json.load(file)

            self.__title = ttk.Label(self.frame, text=jsondict["name"])
            self.__title.grid(column=0, row=0)

            jsondict.pop("name")
            jsondict.pop("zombieIDs")
        
        for i, world in enumerate(jsondict.values()):
            self.__levelBtns.append(ttk.Button(self.frame, text=world["name"], command=functools.partial(self.__switchWorldMenu, world)))
            self.__levelBtns[i].grid(column=0, row=i+1)

        self.__backBtn = ttk.Button(self.frame, text="Back", command=self.__switchMain)
        self.__backBtn.grid(column=0, row=len(self.__levelBtns)+1)
    
    def __switchMain(self):
        self.frame.destroy()
        root.currentState.pop()
        root.currentState.peek().frame.pack()
    
    def __switchWorldMenu(self, world):
        self.frame.pack_forget()
        root.currentState.push(WorldMenu(world))

class WorldMenu(State):
    def __init__(self, world):
        super().__init__()

        self.__title = ttk.Label(self.frame, text=world["name"])
        self.__title.grid(column=0, row=0)

        self.__backBtn = ttk.Button(self.frame, text="Back", command=self.__switchBack)
        self.__backBtn.grid(column=0, row=1)
    
    def __switchBack(self):
        self.frame.destroy()
        root.currentState.pop()
        root.currentState.peek().frame.pack()

root = Main()
root.currentState.push(MainMenu())
root.mainloop()