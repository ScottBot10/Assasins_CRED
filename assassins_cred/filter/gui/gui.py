import tkinter as tk
import tkinter.ttk as ttk
import typing as t
from ...school import Student, School
from .frames import ClassFrame


class PeopleGUI(tk.Frame):
    def_width = 300
    def_height = 150

    def __init__(self, root, school: School):
        super().__init__(root, width=self.def_width, height=self.def_height)

        self.root = root
        self.school = school
        self.width = self.def_width
        self.height = self.def_height

        self.button_dict: t.Dict[Student, tk.IntVar] = {}
        self.total_selected = 0

        tk.Button(self, text="Confirm and Exit", command=self.finish).grid()

        self.nb_grades = ttk.Notebook(self)
        for grade_name, grade in self.school.grade_dict.items():
            nb_classses = ttk.Notebook(self)
            nb_classses.bind("<<NotebookTabChanged>>", lambda x, nb=nb_classses: self.on_change(nb))
            for clazz_name, clazz in grade.class_dict.items():
                frame = ClassFrame(self, clazz)
                nb_classses.add(frame, text=clazz_name)
            self.nb_grades.add(nb_classses, text=grade_name)
        self.nb_grades.bind("<<NotebookTabChanged>>", lambda x, nb=self.nb_grades: self.on_change(nb))
        self.nb_grades.grid()

    def on_change(self, notebook, event=None):
        tabName = notebook.select()
        if tabName:
            widget = notebook.nametowidget(tabName)
            if isinstance(widget, ClassFrame):
                widget.update_total()
            elif isinstance(widget, ttk.Notebook):
                self.on_change(notebook=widget)

    def finish(self) -> School:
        for grade in self.school.grades:
            for clazz in grade.classes:
                for student in clazz.students:
                    if not self.button_dict[student].get():
                        clazz.remove_student(student)
                if len(clazz.students) < 1:
                    grade.remove_class(clazz)
        self.root.destroy()
        return self.school

    def restart(self):
        for student, var in self.button_dict.items():
            var.set(0)
        self.total_selected = 0
        self.nb_grades.select(0)

        for tab in self.nb_grades.tabs():
            widget = self.nb_grades.nametowidget(tab)
            if isinstance(widget, ttk.Notebook):
                widget.select(0)
                for tab in widget.tabs():
                    widget = widget.nametowidget(tab)
                    if isinstance(widget, ClassFrame):
                        widget.select_var.set(0)
