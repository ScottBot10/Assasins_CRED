import tkinter as tk
import tkinter.ttk as ttk
import typing as t

from assassins_cred.school import Student, School, Class


def set_middle(root):
    positionRight = int(root.winfo_screenwidth() / 2 - root.winfo_reqheight() / 2)
    positionDown = int(root.winfo_screenheight() / 2 - root.winfo_reqwidth() / 2)
    root.geometry("+{}+{}".format(positionRight - 130, positionDown - 370))


class ClassFrame(tk.Frame):
    def __init__(self, root: 'PeopleGUI', clazz: Class, *args, **kwargs):
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
