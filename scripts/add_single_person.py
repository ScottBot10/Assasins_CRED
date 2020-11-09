import tkinter as tk
from tkinter import simpledialog, messagebox

from assassins_cred import logger
from assassins_cred.io import files
from assassins_cred.school import Student
from assassins_cred.constants import resource_file

root = tk.Tk()
root.withdraw()

name = simpledialog.askstring("Name", "What is your name, surname and class?\ne.g. Name Surname 10B", parent=root)
if not name:
    messagebox.showerror(message='You did not enter a name!')
    root.destroy()
    exit()

match = init_read.TXT_FORMAT.match(name)
if match is not None:
    groups = match.groups()
    school = files.read_people(f"../{resource_file}/people.csv")
    clazz = school.grade_dict[groups[files.INIT_TXT_GRADE]].class_dict[groups[files.INIT_TXT_FULL_ClASS]]
    clazz.add_student(Student(groups[files.INIT_TXT_FIRST_NAME], groups[files.INIT_TXT_LAST_NAME]))
    files.write_people(school, f"../{resource_file}/people.csv")
    logger.info(f"Added {name}")
