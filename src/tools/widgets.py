import tkinter as tk
from tkinter import ttk

class ZombieSelector(tk.LabelFrame):
    def __init__(self,
                 master,
                 options: list=[],
                 max: int=10,
                 cnf={},
                 **kwargs) -> None:
        kwargs = cnf or kwargs

        self.__max = max

        self.__dropDown = ttk.Combobox(master, state="readonly", values=options, width=15)
        self.__dropDown.bind("<<ComboboxSelected>>", self.__addZombie)

        super().__init__(master, labelwidget=self.__dropDown, width=184, height=max*20+42, **kwargs)

        self.grid_propagate(False)
        self.columnconfigure(1, minsize=37)
        self.columnconfigure(2, minsize=37)

        ttk.Label(self, text="Type", width=15, anchor="center").grid(row=0, column=0)
        ttk.Label(self, text="Alive").grid(row=0, column=1)
        ttk.Label(self, text="Dead").grid(row=0, column=2)

        self.__records = [[] for _ in range(max)]
        self.__free = 0

        self.__cancelIcon = tk.PhotoImage(file="assets/close.png").subsample(4, 4)
    
    def __addZombie(self, event) -> None:
        if self.__free >= self.__max:
            return
        
        new = self.__dropDown.get()

        if new in map(lambda x: x["text"], [r[0] for r in self.__records if len(r) > 0]):
            return
        
        self.__records[self.__free].append(ttk.Label(self, text=new))
        for _ in range(2):
            self.__records[self.__free].append(ttk.Spinbox(self,
                                                         from_=0,
                                                         to=99,
                                                         increment=1,
                                                         width=3))
        self.__records[self.__free].append(tk.Button(self,
                                                   image=self.__cancelIcon,
                                                   relief="flat",
                                                   overrelief="flat",
                                                   bd=0,
                                                   width=10))
        for col in range(4):
            self.__records[self.__free][col].grid(row=self.__free+1, column=col)

        print(self.__records)

        self.__free += 1

    def __removeZombie(self, row: int) -> None:
        pass

    def __getRecords(self):
        pass