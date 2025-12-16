import customtkinter as ctk
from .student import Student
from .functions import Students_data, check_float, id_search, add_stud_file

class Add(ctk.CTkFrame):
    def __init__(self, master, students):
        super().__init__(master)
        self.students = students

        ctk.CTkLabel(
            self, text="Add Student", font=("Montserrat", 48, "bold"), text_color="#3b8ed0"
        ).pack(pady=26, padx=16)

        labels = ["  ID :", "  1st name :", "  2nd name :", "  Email :", "  CIN :", "  Sexe :"]
        self.rows = 6
        self.entries = []

        forme_frame = ctk.CTkFrame(self, corner_radius=26)
        forme_frame.pack(padx=16, pady=8)
        forme_frame.grid_columnconfigure(0, weight=1)
        forme_frame.grid_columnconfigure(1, weight=2)

        for i, l in enumerate(labels):
            ctk.CTkLabel(
                forme_frame, text=l, font=("Gill Sans Nova", 14, "bold"), anchor='w', width=120
            ).grid(row=i, column=0, padx=10, pady=((i+1)%2)*10)

        for i in range(len(labels) - 1):
            entry = ctk.CTkEntry(
                forme_frame, font=("Gill Sans Nova", 14), width=300, height=36, corner_radius=16, border_width=0
            )
            entry.grid(row=i, column=1, padx=10, pady=((i+1)%2)*10)
            self.entries.append(entry)

        male_female_frame = ctk.CTkFrame(forme_frame, fg_color="transparent")
        male_female_frame.grid(row=self.rows-1, column=1, padx=10, pady=10)
        self.male_female = ctk.StringVar(value='other')
        ctk.CTkRadioButton(male_female_frame, text="Male", font=("Gill Sans Nova", 14, "bold"),
                            value='M', variable=self.male_female).pack(side="left")
        ctk.CTkRadioButton(male_female_frame, text="Female", font=("Gill Sans Nova", 14, "bold"),
                            value='F', variable=self.male_female).pack(side="left")

        ctk.CTkButton(
            forme_frame, text="Add", font=("Gill Sans Nova", 18, "bold"), height=40, cursor="hand2",
            corner_radius=16, command=self.add_student
        ).grid(row=self.rows, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.incorrect = ctk.CTkLabel(self, text="", font=("Gill Sans Nova", 12), text_color="red")
        self.incorrect.pack(padx=10, pady=8)

    def get_entries(self):
        self.incorrect.configure(text_color="red")
        try:
            student_id = check_float(self.entries[0].get())
        except:
            self.incorrect.configure(text="ID must be a number!")
            return None

        if student_id == -1 or student_id < 99999:
            self.incorrect.configure(text="ID incorrect!")
            return None

        if id_search(str(student_id)) != -1:
            self.incorrect.configure(text="ID exists!")
            return None

        name1 = self.entries[1].get().strip()
        name2 = self.entries[2].get().strip()
        phone = self.entries[3].get().strip()
        cin = self.entries[4].get().strip()
        sexe = self.male_female.get()

        if not name1.isalpha() or name1 == "":
            self.incorrect.configure(text="First name must contain only letters!")
            return None
        if not name2.isalpha() or name2 == "":
            self.incorrect.configure(text="Second name must contain only letters!")
            return None
        if not phone.isdigit() or len(phone) < 8:
            self.incorrect.configure(text="Phone number must have at least 8 digits!")
            return None
        if cin == "" or not cin[0].isalpha():
            self.incorrect.configure(text="CIN must start with a letter!")
            return None
        if sexe == "other":
            self.incorrect.configure(text="Enter gender please!")
            return None

        return student_id, name1, name2, phone, cin, sexe

    def add_student(self):
        entries = self.get_entries()
        if not entries:
            return

        student_id, name1, name2, phone, cin, sexe = entries

        
        stud = Student(name1, name2, student_id, sexe, phone, cin)
        Students_data.append(stud)
        add_stud_file(stud)

       
        self.update_table()

        
        for entry in self.entries:
            entry.delete(0, ctk.END)
        self.male_female.set('other')

        
        self.incorrect.configure(text="Student added successfully!", text_color="green")

    def update_table(self):
        
        for widget in self.students.student_frame.winfo_children():
            widget.destroy()

        
        titles = ["ID", "1st name", "2nd name", "Phone", "CIN", "Sexe"]
        for i, title in enumerate(titles):
            ctk.CTkLabel(
                self.students.student_frame,
                text=title,
                font=("Helvetica", 24, "bold"),
                fg_color="#3b8ed0",
                corner_radius=16,
                text_color="white",
                height=35,
                anchor="w"
            ).grid(row=0, column=i, padx=10, pady=10)

        
        for r, s in enumerate(Students_data):
            items = str(s).split(',')
            for c, item in enumerate(items):
                ctk.CTkLabel(
                    self.students.student_frame,
                    text=" " + item.strip(),
                    font=("Helvetica", 16),
                    anchor="w",
                    width=self.winfo_screenwidth() // 10
                ).grid(row=r+1, column=c, padx=10, pady=8)
