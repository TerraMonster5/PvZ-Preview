from .. import globals

import tkinter as tk

class State:
    def __init__(self) -> None:
        self.frame = tk.Frame(globals.root)
        self.frame.pack()

    def _switchBack(self) -> None:
        self.frame.destroy()
        globals.root.currentState.pop()
        globals.root.currentState.peek().frame.pack()

from .menus import *