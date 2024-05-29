from . import globals
from . import states
from . import tools
from . import about

import structs
from structs import stk

import tkinter as tk
from tkinter import ttk

class Main(tk.Tk):
    def __init__(self, cnf: dict={}, **kwargs) -> None:
        kwargs = cnf or kwargs
        super().__init__(**kwargs)

        self.currentState = structs.Stack()

        self.iconbitmap("assets/icon.ico")
        self.geometry("600x600")
        self.resizable(False, False)
        self.title("PvZ Preview")

        self.__toolbar = stk.ToolBar(self, tearoff=0)
        self.__toolbar.add_cascade("file", menukw={"tearoff": 0}, cascadekw={"label": "File"})
        self.__toolbar.file.add_command(label="Open", state="disabled", command=lambda: ...) # type: ignore
        self.__toolbar.file.add_command(label="Open recent", state="disabled", command=lambda: ...) # type: ignore
        self.__toolbar.file.add_separator() # type: ignore
        self.__toolbar.file.add_command(label="Save as", state="disabled", command=lambda: ...) # type: ignore
        self.__toolbar.file.add_separator() # type: ignore
        self.__toolbar.file.add_command(label="Close", command=lambda: ...) # type: ignore
        self.__toolbar.file.add_command(label="Exit", command=lambda: exit()) # type: ignore
        self.__toolbar.add_cascade("tools", menukw={"tearoff": 0}, cascadekw={"label": "Tools"})
        self.__toolbar.tools.add_cascade("calculators", menukw={"tearoff": 0}, cascadekw={"label": "Calculators"}) # type: ignore
        self.__toolbar.tools.calculators.add_command(label="50% Rule", command=lambda: tools.FiftyPercent()) # type: ignore
        self.__toolbar.add_cascade("help", menukw={"tearoff": 0}, cascadekw={"label": "Help"})
        self.__toolbar.help.add_command(label="About", command=lambda: about.About.show()) # type: ignore
        self.config(menu=self.__toolbar)

if __name__ == "__main__":
    globals.root = Main()
    globals.root.currentState.push(states.MainMenu())
    globals.root.mainloop()