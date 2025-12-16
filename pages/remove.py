import customtkinter as ctk
from .student import Student
from .functions import id_search, check_float, remove_student, Students_data

class Remove(ctk.CTkFrame):
    def __init__(self, master, students_frame=None):
        super().__init__(master)
        # store reference to the students frame (UI list) so we can refresh it after removal
        self.students_frame = students_frame
        
        ctk.CTkLabel(
            self, 
            text="Remove Student", 
            font=("Montserrat", 48, "bold"), 
            text_color="#3b8ed0"
        ).pack(pady=26, padx=16)

        
        frame = ctk.CTkFrame(self, corner_radius=26)
        frame.pack(padx=10, pady=10)

        ctk.CTkLabel(frame, text="Enter the ID of the student:", font=("Gill Sans Nova", 12)).pack(padx=10, pady=10)

        self.id_entry = ctk.CTkEntry(frame, width=300, height=35, border_width=0, corner_radius=16, placeholder_text="ID")
        self.id_entry.pack(padx=10)

        
        ctk.CTkButton(
            frame,
            text="Remove",
            font=("Gill Sans Nova", 18, "bold"),
            height=36,
            cursor="hand2",
            corner_radius=16,
            command=self.remove
        ).pack(padx=10, pady=10, fill="x", expand=True)

        self.incorrect = ctk.CTkLabel(self, text="", font=("Gill Sans Nova", 12), text_color="red")
        self.incorrect.pack(padx=10, pady=8)

    def remove(self):
        student_id = check_float(self.id_entry.get())

        if student_id == -1 or student_id <= 99999:
            self.incorrect.configure(text="ID incorrect!", text_color="red")
            return

        index = id_search(str(student_id))
        if index == -1:
            self.incorrect.configure(text="ID not found!", text_color="red")
            return
        success = remove_student(index)

        if not success:
            self.incorrect.configure(text="Error removing student!", text_color="red")
            return

        Student.Num_students -= 1

        students_frame = self.students_frame
        if students_frame is None:
            root = self.master
            found = False
            while root is not None:
                if hasattr(root, 'home_frame'):
                    students_frame = getattr(root.home_frame, 'students', None)
                    found = True
                    break
                root = getattr(root, 'master', None)
            if not found and students_frame is None:
                self.incorrect.configure(text="Student removed, but cannot refresh UI (students frame missing)", text_color="orange")
                self.id_entry.delete(0, ctk.END)
                return

        if students_frame:
            for widget in students_frame.student_frame.winfo_children():
                widget.destroy()

            titles = ["ID", "1st name", "2nd name", "Email", "Major", "Sexe"]
            for i, title in enumerate(titles):
                ctk.CTkLabel(
                    students_frame.student_frame,
                    text=title,
                    font=("Helvetica", 24, "bold"),
                    fg_color="#3b8ed0",
                    corner_radius=16,
                    text_color="white",
                    height=35,
                    anchor="w"
                ).grid(row=0, column=i, padx=10, pady=10)

            for r, stud in enumerate(Students_data):
                items = str(stud).split(',')
                for c, item in enumerate(items):
                    ctk.CTkLabel(
                        students_frame.student_frame,
                        text=" " + item.strip(),
                        font=("Helvetica", 16),
                        anchor="w"
                    ).grid(row=r+1, column=c, padx=10, pady=8)

        self.incorrect.configure(text="Student removed successfully", text_color="green")
        self.id_entry.delete(0, ctk.END)
