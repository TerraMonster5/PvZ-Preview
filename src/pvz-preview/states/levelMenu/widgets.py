import tkinter as tk
from tkinter import ttk

class PreviewSelector(ttk.Treeview):
    def __init__(self, master, cnf: dict={}, **kwargs):
        kwargs = cnf or kwargs

        super().__init__(master, **kwargs)