import customtkinter as ctk
from .functions import Students_data

class Students(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        titles = ["Student ID", "First Name", "Last Name", "Email", "Major", "Gender"] 
        self.student_frame = ctk.CTkFrame(self, corner_radius=16)
        self.student_frame.pack(padx=10, pady=8, fill='both', expand=True)

        for i in range(6): 
            self.student_frame.grid_columnconfigure(i, weight=1)

        for i, title in enumerate(titles): 
            ctk.CTkLabel(
                self.student_frame, 
                text=title, 
                font=("Helvetica", 24, "bold"), 
                anchor="w",
                width=self.winfo_screenwidth() // 10,
                fg_color='#3b8ed0',
                corner_radius=16,
                text_color="white",
                height=35
            ).grid(row=0, column=i, padx=10, pady=10) 

        for num, stud in enumerate(Students_data): 
            items = str(stud).split(',') 

            for i, item in enumerate(items): 
                item = item.strip() 
                ctk.CTkLabel(
                    self.student_frame, 
                    text=" " + item,
                    font=("Helvetica", 16), 
                    anchor="w",
                    width=self.winfo_screenwidth() // 10
                ).grid(row=num + 1, column=i, padx=10, pady=8) 