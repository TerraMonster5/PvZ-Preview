from structs import abstracts

from typing import Any

import tkinter as tk
from tkinter import ttk

class About(tk.Toplevel, abstracts.Singleton):
    @classmethod
    def show(cls) -> Any:
        if cls.instance is None or not cls.instance.winfo_exists():
            cls.instance = cls()
        return cls.instance

    def __init__(self, cnf: dict={}, **kwargs) -> None:
        kwargs = cnf or kwargs
        super().__init__(**kwargs)

        self.iconbitmap("assets/icon.ico")
        self.title("About")
        self.resizable(False, False)

        ttk.Label(self, text="Version: 0.1.7").pack()
        ttk.Button(self, text="License", command=lambda: License.show(master=self)).pack()

class License(tk.Toplevel, abstracts.Singleton):
    @classmethod
    def show(cls, cnf: dict={}, **kwargs):
        kwargs = cnf or kwargs

        if cls.instance is None or not cls.instance.winfo_exists():
            cls.instance = cls(**kwargs)
        return cls.instance

    def __init__(self, cnf: dict={}, **kwargs) -> None:
        kwargs = cnf or kwargs
        super().__init__(**kwargs)

        self.iconbitmap("assets/icon.ico")
        self.title("GNU General Public License | Version 3")
        self.resizable(False, False)

        field = tk.Text(self, width=80)
        with open("assets/LICENSE", "r") as file:
            [field.insert(f"{i}.0", line) for i, line in enumerate(file, 1)]
        field.pack()

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=field.yview)
        field.config(yscrollcommand=scrollbar.set, state="disabled")
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)