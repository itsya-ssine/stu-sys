import customtkinter as ctk
from .add import Add
from .modify import Modify
from .remove import Remove


class ManageStudents(ctk.CTkFrame):
    def __init__(self, master, students_frame=None):
        super().__init__(master)
        self.students_frame = students_frame

        ctk.CTkLabel(self, text="Manage Students", font=("Montserrat", 28, "bold"), text_color="#3b8ed0").pack(pady=12)

        tabview = ctk.CTkTabview(self, width=800)
        tabview.pack(padx=10, pady=10, fill="both", expand=True)

        tabview.add("Add")
        tabview.add("Modify")
        tabview.add("Remove")

        add_container = tabview.tab("Add")
        modify_container = tabview.tab("Modify")
        remove_container = tabview.tab("Remove")

        try:
            self.add_frame = Add(add_container, self.students_frame)
        except TypeError:
            self.add_frame = Add(add_container, self.students_frame)

        self.modify_frame = Modify(modify_container, self.students_frame)
        self.remove_frame = Remove(remove_container, self.students_frame)

        self.add_frame.pack(fill="both", expand=True)
        self.modify_frame.pack(fill="both", expand=True)
        self.remove_frame.pack(fill="both", expand=True)
