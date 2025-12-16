import customtkinter as ctk
from PIL import Image
import os

from .functions import Buttons
from .students import Students
from .manage_students import ManageStudents
from .absence_notes import AbsenceNotes
from .notes import Notes
from .report_generator import ReportGenerator


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, home):
        super().__init__(master)

        self.mode = "light"
        self.students = Students(master)
        self.manage_frame = ManageStudents(master, self.students)
        self.absence_notes_frame = AbsenceNotes(master)
        self.notes_frame = Notes(master)
        self.report_frame = ReportGenerator(master)

        self.students.pack_forget()
        self.manage_frame.pack_forget()
        self.absence_notes_frame.pack_forget()
        self.notes_frame.pack_forget()
        self.report_frame.pack_forget()

        self.pages = [
            home,
            self.students,
            self.manage_frame,
            self.absence_notes_frame,
            self.notes_frame,
            self.report_frame
        ] 

        try: 
            img_d = Image.open(os.path.join("Images", "User_light.png"))
            img_l = Image.open(os.path.join("Images", "User_dark.png"))

            logo_img = ctk.CTkImage( 
                light_image=img_l,
                dark_image=img_d,
                size=(150, 150)
            )

            ctk.CTkLabel(self, text="", image=logo_img).pack(padx=16, pady=8)  

        except:
            ctk.CTkLabel(self, text="Logo here").pack(padx=16, pady=16)
        ctk.CTkLabel(
            self,
            text="STUDENTS\nMANAGEMENT\nSYSTEM",
            font=("Blackpast", 18)
        ).pack(padx=16, pady=8)
        
        menu = ["Home", "Students", "Manage Students", "Absence Notes", "Notes", "Class Report"] 

        for i, m in enumerate(menu): 
            button = ctk.CTkButton(
                self,
                text=m,
                width=200,
                height=35,
                corner_radius=8,
                cursor="hand2",
                fg_color=("#939ba2", "#343638"),
                anchor='w',
                font=("Gill Sans Nova", 12, "bold"),
                command=lambda i=i: self.button_click(i), 
                state="disabled" 
            )
            button.pack(padx=8, pady=((i+1)%2) * 8) 
            Buttons.append(button)

        Buttons[0].configure(fg_color="#3b8ed0") 
       
        ctk.CTkSwitch(
            self,
            text="Dark Mode",
            border_width=0,
            font=("Montserrat", 12, "bold"),
            command=self.switch_dark_light_mode 
        ).pack(padx=16, pady=8, side="bottom")
    
    def button_click(self, index): 
        for button, page in zip(Buttons, self.pages): 
            button.configure(fg_color=("#939ba2", "#343638"))                                           
            page.pack_forget()  

        Buttons[index].configure(fg_color="#3b8ed0") 
        self.pages[index].pack(padx=10, pady=10, fill="both", expand=True, side='left') 

    def switch_dark_light_mode(self): 
        self.mode = "dark" if self.mode == "light" else "light" 
        ctk.set_appearance_mode(self.mode) 


