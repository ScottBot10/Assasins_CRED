import tkinter as tk
from tkinter import messagebox

from assassins_cred import logger
from assassins_cred.constants import TXT_FORMAT
from assassins_cred.io import IO
from assassins_cred.io import txt_file
from assassins_cred.school import Student
from assassins_cred.util.school import assign_code

root = tk.Tk()
root.withdraw()

io = IO()

# name = simpledialog.askstring("Name", "What is your name, surname and class?\ne.g. Name Surname 10B", parent=root)
name = "Seth Ravat 11A"
if not name:
    messagebox.showerror(message='You did not enter a name!')
    root.destroy()
else:
    match = TXT_FORMAT.match(name)
    if match is not None:
        groups = match.groupdict()
        school = io.read_people()
        clazz = school.grade_dict[groups[txt_file.INIT_TXT_GRADE]].class_dict[groups[txt_file.INIT_TXT_FULL_ClASS]]
        student = assign_code(school,
                              Student(groups[txt_file.INIT_TXT_FIRST_NAME], groups[txt_file.INIT_TXT_LAST_NAME]))
        clazz.add_student(student)
        io.write_people(school=school)
        logger.info(f"Added {name}")
