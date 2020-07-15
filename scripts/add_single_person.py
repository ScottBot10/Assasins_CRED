import tkinter as tk
from tkinter import simpledialog, messagebox

from assassins_cred.io.files import init_read
from assassins_cred.io.files.read import read_people
from assassins_cred.io.files.write import write_people
from assassins_cred.school import Student

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
    school = read_people("../test_resources/people.csv")
    clazz = school.grade_dict[groups[init_read.TXT_GRADE]].class_dict[groups[init_read.TXT_FULL_ClASS]]
    clazz.add_student(Student(groups[init_read.TXT_FIRST_NAME], groups[init_read.TXT_LAST_NAME]))
    write_people(school, "../test_resources/people.csv")
