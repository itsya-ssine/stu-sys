import customtkinter as ctk
from .functions import get_student_notes, add_student_note, delete_student_note, check_float, id_search, Students_data, init_managers


class Notes(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        init_managers()

        ctk.CTkLabel(self, text="Notes Management", font=("Montserrat", 28, "bold"), text_color="#3b8ed0").pack(pady=12)

        top = ctk.CTkFrame(self)
        top.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(top, text="Student ID:", width=100).pack(side="left", padx=(8,4))
        self.id_entry = ctk.CTkEntry(top, width=150, placeholder_text="Student ID")
        self.id_entry.pack(side="left", padx=4)
        ctk.CTkButton(top, text="Search", command=self.search_student).pack(side="left", padx=8)

        self.student_info = ctk.CTkLabel(self, text="", text_color="green")
        self.student_info.pack(padx=10)

        form = ctk.CTkFrame(self)
        form.pack(padx=10, pady=6, fill="x")

        ctk.CTkLabel(form, text="Subject:", width=80).grid(row=0, column=0, padx=8, pady=6)
        self.subject_entry = ctk.CTkEntry(form, width=300)
        self.subject_entry.grid(row=0, column=1, padx=8, pady=6)

        ctk.CTkLabel(form, text="Grade:", width=80).grid(row=1, column=0, padx=8, pady=6)
        self.grade_entry = ctk.CTkEntry(form, width=100)
        self.grade_entry.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        ctk.CTkButton(form, text="Add Note", command=self.add_note).grid(row=2, column=0, columnspan=2, pady=8)

        self.msg = ctk.CTkLabel(self, text="", text_color="red")
        self.msg.pack(padx=10, pady=6)

        self.notes_frame = ctk.CTkScrollableFrame(self)
        self.notes_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.selected_student_id = None

    def search_student(self):
        self.msg.configure(text="")
        sid = check_float(self.id_entry.get())
        if sid == -1 or sid < 1:
            self.msg.configure(text="Invalid ID")
            return
        idx = id_search(str(sid))
        if idx == -1:
            self.msg.configure(text="Student not found")
            return
        student = Students_data[idx]
        self.selected_student_id = sid
        self.student_info.configure(text=f"Selected: {student.first_name} {student.last_name} (ID: {student.id})")
        self.refresh_notes()

    def add_note(self):
        if not self.selected_student_id:
            self.msg.configure(text="Select a student first")
            return
        subject = self.subject_entry.get().strip()
        try:
            grade = float(self.grade_entry.get())
        except Exception:
            self.msg.configure(text="Grade must be a number")
            return
        if subject == "":
            self.msg.configure(text="Enter subject")
            return
        if grade < 0 or grade > 20:
            self.msg.configure(text="Grade must be between 0 and 20")
            return
        success = add_student_note(self.selected_student_id, subject, grade)
        if success:
            self.msg.configure(text="Note added", text_color="green")
            self.subject_entry.delete(0, ctk.END)
            self.grade_entry.delete(0, ctk.END)
            self.refresh_notes()
        else:
            self.msg.configure(text="Error adding note")

    def refresh_notes(self):
        for w in self.notes_frame.winfo_children():
            w.destroy()
        if not self.selected_student_id:
            return
        notes = get_student_notes(self.selected_student_id)
        if not notes:
            ctk.CTkLabel(self.notes_frame, text="No notes recorded").pack(pady=8)
            return
        for n in notes:
            f = ctk.CTkFrame(self.notes_frame, corner_radius=8)
            f.pack(fill="x", padx=8, pady=6)
            ctk.CTkLabel(f, text=f"{n.get('subject')} - {n.get('grade')}").pack(side="left", padx=8)
            btn = ctk.CTkButton(f, text="Delete", width=80, command=lambda nid=n.get('id'): self.delete_note(nid))
            btn.pack(side="right", padx=8)

    def delete_note(self, note_id):
        success = delete_student_note(note_id)
        if success:
            self.msg.configure(text="Note deleted", text_color="green")
            self.refresh_notes()
        else:
            self.msg.configure(text="Error deleting note")
