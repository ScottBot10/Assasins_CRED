from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gui import PeopleGUI
from ...school import Student, Class


class ClassFrame(tk.Frame):

    def __init__(self, root: PeopleGUI, clazz: Class, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.root = root
        self.clazz = clazz

        c = tk.Label(self, text='             Class: {}'.format(self.clazz.name), font=("device", 16))
        c.grid(row=0, column=0)
        self.total_selected = tk.Label(self, text='Total Selected: ' + str(self.root.total_selected))
        self.total_selected.grid(row=1, column=1, sticky='w')
        tk.Button(self, text="Delete and Restart", command=self.root.restart).grid(row=1, column=0, sticky='w')
        select_label = tk.Label(self, text='Select All')
        select_label.grid(sticky='w')

        lbl_info = select_label.grid_info()
        self.select_var = tk.IntVar()
        tk.Checkbutton(self, variable=self.select_var, command=self.select_all) \
            .grid(row=lbl_info["row"], column=lbl_info["column"] + 2, sticky='e')

        self.f = tk.Frame(self, height=1, width=self.root.width - 20, bg="black")
        self.f.grid(row=3, columnspan=3)

        for name, student in clazz.student_dict.items():
            self.root.button_dict[student] = tk.IntVar()

            student_name = tk.Label(self, text=student.full_name)
            student_name.grid(sticky='w')
            info = student_name.grid_info()

            student_checkbtn = tk.Checkbutton(self, variable=root.button_dict[student],
                                              command=lambda student=student: self.update_one(student))
            student_checkbtn.grid(row=info["row"], column=info["column"] + 2, sticky='e')

    def update_total(self):
        self.total_selected["text"] = 'Total Selected: ' + str(self.root.total_selected)

    def select_all(self):
        val = self.select_var.get()
        for name, student in self.clazz.student_dict.items():
            student_var = self.root.button_dict[student]
            student_val = student_var.get()
            if val:
                if not student_val:
                    self.root.total_selected += 1
            else:
                if student_val:
                    self.root.total_selected -= 1
            student_var.set(val)
        self.update_total()

    def update_one(self, student: Student):
        val = self.root.button_dict[student].get()
        if val:
            self.root.total_selected += 1
        else:
            self.root.total_selected -= 1
        self.update_total()
