import tkinter as tk

from assassins_cred import logger
from assassins_cred.filter.gui.gui import PeopleGUI
from assassins_cred.io.files import from_csv, write_people
from assassins_cred.util.school import unpack_students

# forms = Forms('1UwOiJyvJr-REvUnRVir2_6E97BGk321-tb06BhGJEQ8')


ppl = from_csv("../test_resources/grade 8.csv")
# ppl = from_txt("../test_resources/people_cp1.txt")

root = tk.Tk()

gui = PeopleGUI(root, ppl)
gui.pack()

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
root.geometry("+{}+{}".format(positionRight - 130, positionDown - 370))

root.mainloop()
school = gui.school
# school = assign_codes(school)
# school = shuffle_school_grade(school)
write_people(school, "../test_resources/people.csv")

logger.info(f"Added {len(unpack_students(school.grades))} people")
