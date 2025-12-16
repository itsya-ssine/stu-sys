import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime
from .functions import (
    Students_data, id_search, check_float, get_student_absences,
    add_student_absence, get_absence_count, init_managers, absence_manager
)

class AbsenceNotes(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        init_managers()
        self.selected_student_id = None
        self.absences_data = []
        
        ctk.CTkLabel(
            self, 
            text="Absence Notes Management", 
            font=("Montserrat", 48, "bold"), 
            text_color="#3b8ed0"
        ).pack(pady=26, padx=16)
        
        top_frame = ctk.CTkFrame(self, corner_radius=26)
        top_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(
            top_frame, 
            text="Student ID:", 
            font=("Gill Sans Nova", 12)
        ).pack(side="left", padx=10, pady=10)
        
        self.id_entry = ctk.CTkEntry(
            top_frame, 
            width=200, 
            height=35, 
            border_width=0, 
            corner_radius=16, 
            placeholder_text="Enter Student ID"
        )
        self.id_entry.pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(
            top_frame,
            text="Search",
            font=("Gill Sans Nova", 14, "bold"),
            height=35,
            cursor="hand2",
            corner_radius=16,
            command=self.search_student
        ).pack(side="left", padx=10, pady=10)
        
        self.student_info = ctk.CTkLabel(
            self,
            text="",
            font=("Gill Sans Nova", 12),
            text_color="green"
        )
        self.student_info.pack(padx=10, pady=5)
        
        form_frame = ctk.CTkFrame(self, corner_radius=26)
        form_frame.pack(padx=10, pady=10, fill="x")
        
        ctk.CTkLabel(
            form_frame,
            text="Add Absence",
            font=("Montserrat", 24, "bold"),
            text_color="#3b8ed0"
        ).pack(pady=10)
        
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(
            date_frame,
            text="Date of Absence:",
            font=("Gill Sans Nova", 12)
        ).pack(side="left", padx=10)
        
        self.date_entry = DateEntry(
            date_frame,
            width=25,
            background='#3b8ed0',
            foreground='white',
            borderwidth=2,
            font=("Gill Sans Nova", 10)
        )
        self.date_entry.pack(side="left", padx=10)
        
        reason_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        reason_frame.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(
            reason_frame,
            text="Reason:",
            font=("Gill Sans Nova", 12)
        ).pack(side="left", padx=10)
        
        self.reason_entry = ctk.CTkEntry(
            reason_frame,
            width=400,
            height=35,
            border_width=0,
            corner_radius=16,
            placeholder_text="Absence reason"
        )
        self.reason_entry.pack(side="left", padx=10)
        
        checkbox_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        checkbox_frame.pack(padx=10, pady=5, fill="x")
        
        self.justified_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            checkbox_frame,
            text="Justified Absence",
            font=("Gill Sans Nova", 12),
            variable=self.justified_var
        ).pack(side="left", padx=10)
    
        desc_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        desc_frame.pack(padx=10, pady=5, fill="x")
        
        ctk.CTkLabel(
            desc_frame,
            text="Description:",
            font=("Gill Sans Nova", 12)
        ).pack(side="left", padx=10)
        
        self.description_entry = ctk.CTkEntry(
            desc_frame,
            width=400,
            height=80,
            border_width=0,
            corner_radius=16,
            placeholder_text="Additional notes"
        )
        self.description_entry.pack(side="left", padx=10)
        
        ctk.CTkButton(
            form_frame,
            text="Add Absence",
            font=("Gill Sans Nova", 14, "bold"),
            height=40,
            cursor="hand2",
            corner_radius=16,
            command=self.add_absence
        ).pack(padx=10, pady=10, fill="x")
        
        self.message = ctk.CTkLabel(
            self,
            text="",
            font=("Gill Sans Nova", 12),
            text_color="red"
        )
        self.message.pack(padx=10, pady=5)
        
        display_frame = ctk.CTkFrame(self, corner_radius=26)
        display_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(
            display_frame,
            text="Student Absences",
            font=("Montserrat", 20, "bold"),
            text_color="#3b8ed0"
        ).pack(pady=10)
        
        self.absences_frame = ctk.CTkScrollableFrame(
            display_frame,
            corner_radius=16
        )
        self.absences_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    def search_student(self):
        self.message.configure(text="", text_color="red")
        student_id = check_float(self.id_entry.get())
        
        if student_id == -1 or student_id < 99999:
            self.message.configure(text="Invalid Student ID!", text_color="red")
            return
        
        index = id_search(str(student_id))
        if index == -1:
            self.message.configure(text="Student not found!", text_color="red")
            return
        
        self.selected_student_id = student_id
        student = Students_data[index]
        
        self.student_info.configure(
            text=f"Selected: {student.first_name} {student.last_name} (ID: {student.id})",
            text_color="green"
        )
        
        self.refresh_absences()
    
    def add_absence(self):
        if not self.selected_student_id:
            self.message.configure(text="Please select a student first!", text_color="red")
            return
        
        date_absence = self.date_entry.get_date()
        reason = self.reason_entry.get().strip()
        justified = self.justified_var.get()
        description = self.description_entry.get().strip()
        
        if not reason:
            self.message.configure(text="Please enter a reason!", text_color="red")
            return
        
        success = add_student_absence(
            self.selected_student_id,
            date_absence,
            reason,
            justified,
            description
        )
        
        if success:
            self.message.configure(text="Absence added successfully!", text_color="green")
            self.reason_entry.delete(0, ctk.END)
            self.description_entry.delete(0, ctk.END)
            self.justified_var.set(False)
            self.refresh_absences()
        else:
            self.message.configure(text="Error adding absence!", text_color="red")
    
    def refresh_absences(self):
        for widget in self.absences_frame.winfo_children():
            widget.destroy()
        
        if not self.selected_student_id:
            ctk.CTkLabel(
                self.absences_frame,
                text="No student selected",
                font=("Gill Sans Nova", 12)
            ).pack(pady=10)
            return
        
        absences = get_student_absences(self.selected_student_id)
        count = get_absence_count(self.selected_student_id)
        
        ctk.CTkLabel(
            self.absences_frame,
            text=f"Total Absences: {count}",
            font=("Gill Sans Nova", 14, "bold"),
            text_color="#3b8ed0"
        ).pack(pady=10)
        
        if not absences:
            ctk.CTkLabel(
                self.absences_frame,
                text="No absences recorded",
                font=("Gill Sans Nova", 12)
            ).pack(pady=10)
            return
        
        for absence in absences:
            absence_card = ctk.CTkFrame(
                self.absences_frame,
                corner_radius=12,
                fg_color="#f0f0f0"
            )
            absence_card.pack(padx=10, pady=5, fill="x")
            
            date_str = str(absence['date_absence'])
            justified_str = "✓ Justified" if absence['justified'] else "✗ Not Justified"
            justified_color = "green" if absence['justified'] else "red"
            
            ctk.CTkLabel(
                absence_card,
                text=f"Date: {date_str}",
                font=("Gill Sans Nova", 11, "bold")
            ).pack(anchor="w", padx=10, pady=5)
            
            ctk.CTkLabel(
                absence_card,
                text=f"Reason: {absence['reason']}",
                font=("Gill Sans Nova", 11)
            ).pack(anchor="w", padx=10, pady=2)
            
            ctk.CTkLabel(
                absence_card,
                text=justified_str,
                font=("Gill Sans Nova", 11, "bold"),
                text_color=justified_color
            ).pack(anchor="w", padx=10, pady=2)
            
            if absence['note_description']:
                ctk.CTkLabel(
                    absence_card,
                    text=f"Notes: {absence['note_description']}",
                    font=("Gill Sans Nova", 10),
                    text_color="gray"
                ).pack(anchor="w", padx=10, pady=2)
