import pathlib
import json

import tkinter as tk
from tkinter import ttk

class Main(tk.Tk):
    def __init__(self, *kwargs):
        super().__init__(*kwargs)

        self.currentState: State

        self.geometry("600x600")
        self.title("PvZ Preview")

class State:
    def __init__(self):
        self._frame = tk.Frame(root)
        self._frame.pack()

class MainMenu(State):
    def __init__(self):
        super().__init__()

        self.__title = ttk.Label(self._frame, text="PvZ Preview")
        self.__title.grid(column=0, row=0)

        worlds = [f.stem for f in pathlib.Path("adventures/").glob("*.json")]
        
        self.__worldBtns = []

        for i, path in enumerate(worlds):
            with open(f"adventures/{path}.json", "r") as file: name = json.load(file)["name"]
            self.__worldBtns.append(ttk.Button(self._frame, text=name))
            self.__worldBtns[i].grid(column=0, row=i+1)

        self.__quitBtn = ttk.Button(self._frame, text="Quit", command=root.destroy)
        self.__quitBtn.grid(column=0, row=len(self.__worldBtns)+1)

class WorldMenu(State):
    def __init__(self):
        super().__init__()

        self.__backBtn = ttk.Button(self._frame, text="Back", command=self.__switchMain)
        self.__backBtn.grid(column=0, row=0)
    
    def __switchMain(self):
        self._frame.destroy()
        root.currentState = MainMenu()

root = Main()
root.currentState = MainMenu()
root.mainloop()