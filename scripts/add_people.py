import tkinter as tk

from assassins_cred.filter.gui.gui import PeopleGUI
from assassins_cred.io.init_read import from_csv
from assassins_cred.io.write import write_people
from assassins_cred.shuffle import shuffle_school_grade
from assassins_cred.util.school import assign_codes

# forms = Forms('1UwOiJyvJr-REvUnRVir2_6E97BGk321-tb06BhGJEQ8')
#
# people_dict = forms.ReadToDict()
# write = Write()
# write.CSVfromDict(people_dict)

ppl = from_csv("../test_resources/grade 8.csv")

root = tk.Tk()

gui = PeopleGUI(root, ppl)
gui.pack()

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)
root.geometry("+{}+{}".format(positionRight - 130, positionDown - 370))

root.mainloop()
school = assign_codes(gui.school)
school = shuffle_school_grade(school)
write_people(school, "../test_resources/people.csv")
