import tkinter as tk
from tkinter import ttk

class About(tk.Toplevel):
    def __init__(self, cnf: dict={}, **kwargs) -> None:
        kwargs = cnf or kwargs
        super().__init__(**kwargs)

        ttk.Button(self, text="License", command=lambda: License()).pack()

        self.mainloop()

class License(tk.Toplevel):
    def __init__(self, cnf: dict={}, **kwargs) -> None:
        kwargs = cnf or kwargs
        super().__init__(**kwargs)

        self.mainloop()