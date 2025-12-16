import customtkinter as ctk
from .functions import check_float, Students_data, id_search, init_managers
from . import functions

class Modify(ctk.CTkFrame):  
    def __init__(self, master, students_frame=None):
        super().__init__(master)
        
        self.students_frame = students_frame

        ctk.CTkLabel(
            self, text="Modify Student", font=("Montserrat", 48, "bold"), text_color="#3b8ed0"
        ).pack(pady=26, padx=16)

        self.index = None  

        
        self.frame = ctk.CTkFrame(self, corner_radius=26)
        self.frame.pack(padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Enter the ID of the student:", font=("Gill Sans Nova", 12)).pack(padx=10, pady=10)
        self.id_entry = ctk.CTkEntry(self.frame, width=300, height=35, border_width=0, corner_radius=16, placeholder_text="ID")
        self.id_entry.pack(padx=10)

        ctk.CTkButton(
            self.frame,
            text="Search",
            font=("Gill Sans Nova", 18, "bold"),
            height=36,
            cursor="hand2",
            corner_radius=16,
            command=self.search
        ).pack(padx=10, pady=10, fill="x", expand=True)

        self.incorrect = ctk.CTkLabel(self, text="", font=("Gill Sans Nova", 12), text_color="red")
        self.incorrect.pack(padx=10)

        
        labels = ["  ID :", "  1st name :", "  2nd name :", "  Email :", "  Major :", "  Sexe :"]
        self.rows = len(labels)
        self.entries = []

        self.forme_frame = ctk.CTkFrame(self, corner_radius=26)
        self.forme_frame.pack_forget()

        self.forme_frame.grid_columnconfigure(0, weight=1)
        self.forme_frame.grid_columnconfigure(1, weight=2)

        for i, l in enumerate(labels):
            ctk.CTkLabel(
                self.forme_frame,
                text=l,
                font=("Gill Sans Nova", 14, "bold"),
                anchor='w',
                width=120
            ).grid(row=i, column=0, padx=10, pady=((i+1)%2)*10)

        for i in range(len(labels)-1):
            entry = ctk.CTkEntry(
                self.forme_frame,
                font=("Gill Sans Nova", 14),
                width=300,
                height=36,
                corner_radius=16,
                border_width=0
            )
            entry.grid(row=i, column=1, padx=10, pady=((i+1)%2)*10)
            self.entries.append(entry)

        male_female_frame = ctk.CTkFrame(self.forme_frame, fg_color="transparent")
        male_female_frame.grid(row=self.rows-1, column=1, padx=10, pady=10)
        self.male_female = ctk.StringVar(value='other')

        ctk.CTkRadioButton(male_female_frame, text="Male", font=("Gill Sans Nova", 14, "bold"), value='M', variable=self.male_female).pack(side="left")
        ctk.CTkRadioButton(male_female_frame, text="Female", font=("Gill Sans Nova", 14, "bold"), value='F', variable=self.male_female).pack(side="left")

        ctk.CTkButton(
            self.forme_frame,
            text="Modify",
            font=("Gill Sans Nova", 18, "bold"),
            height=40,
            cursor="hand2",
            corner_radius=16,
            command=self.modify_student
        ).grid(row=self.rows, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.incorr = ctk.CTkLabel(self, text="", font=("Gill Sans Nova", 12), text_color="red")
        self.incorr.pack_forget()

    
    def search(self):
        self.incorrect.configure(text="", text_color="red")
        student_id = check_float(self.id_entry.get())
        if student_id != -1 and student_id > 99999:
            self.index = id_search(str(student_id))
            if self.index != -1:
                infos = str(Students_data[self.index]).split(',')
                for i, info in enumerate(infos[:-1]):
                    self.entries[i].delete(0, ctk.END)
                    self.entries[i].insert(0, info.strip())
                self.male_female.set(infos[-1].strip())

                self.frame.pack_forget()
                self.forme_frame.pack(padx=10, pady=10)
                self.incorr.pack(padx=10, pady=8)
                return
        self.incorrect.configure(text="ID incorrect!", text_color="red")

    
    def get_entries(self):
        self.incorr.configure(text_color="red")
        student_id = check_float(self.entries[0].get())
        if student_id == -1 or student_id < 99999:
            self.incorr.configure(text="ID incorrect!")
            return None

        name1 = self.entries[1].get().strip()
        if not name1:
            self.incorr.configure(text="Enter First name please!")
            return None
        name2 = self.entries[2].get().strip()
        if not name2:
            self.incorr.configure(text="Enter Second name please!")
            return None
        email = self.entries[3].get().strip()
        if not email or "@" not in email:
            self.incorr.configure(text="Email incorrect!")
            return None
        major = self.entries[4].get().strip()
        if not major:
            self.incorr.configure(text="Major cannot be empty!")
            return None
        sexe = self.male_female.get()
        if sexe == "other":
            self.incorr.configure(text="Enter sexe please!")
            return None
        return student_id, name1, name2, email, major, sexe

    
    def modify_student(self):
        entries = self.get_entries()
        if not entries:
            return

        student_id, name1, name2, email, major, sexe = entries

        if not functions.student_manager:
            functions.init_managers()

        success = functions.student_manager.update_student(student_id, name1, name2, email, sexe, major)
        
        if success:
            Students_data[self.index].first_name = name1
            Students_data[self.index].last_name = name2
            Students_data[self.index].email = email
            Students_data[self.index].major = major
            Students_data[self.index].sexe = sexe
            
            for entry in self.entries:
                entry.delete(0, ctk.END)
            self.male_female.set('other')

            self.forme_frame.pack_forget()
            self.incorr.pack_forget()
            self.frame.pack(padx=10, pady=10)

            self.id_entry.delete(0, ctk.END)
            self.incorrect.configure(text="Student modified successfully!", text_color="green")
            self.incorrect.pack(padx=10)

            sf = self.students_frame
            if sf is None:
                root = self.master
                while root is not None:
                    if hasattr(root, 'home_frame'):
                        sf = getattr(root.home_frame, 'students', None)
                        break
                    root = getattr(root, 'master', None)

            if sf:
                for widget in sf.student_frame.winfo_children():
                    widget.destroy()

                titles = ["ID", "1st name", "2nd name", "Email", "Major", "Sexe"]
                for i, title in enumerate(titles):
                    ctk.CTkLabel(
                        sf.student_frame,
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
                            sf.student_frame,
                            text=" " + item.strip(),
                            font=("Helvetica", 16),
                            anchor="w"
                        ).grid(row=r+1, column=c, padx=10, pady=8)
        else:
            self.incorr.configure(text="Error modifying student!", text_color="red")
