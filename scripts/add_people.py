import tkinter as tk

from assassins_cred import logger
from assassins_cred.filter.gui import PeopleGUI, set_middle
from assassins_cred.io import IO
from assassins_cred.util.school import assign_codes

io = IO(init=True)

ppl = io.init_read()

root = tk.Tk()
gui = PeopleGUI(root, ppl)
gui.pack()

set_middle(root)

root.mainloop()
school = assign_codes(gui.school)

io.write_people(school=school)

logger.info(f"Added {len(school.students)} people")
