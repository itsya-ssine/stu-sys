import customtkinter as ctk
from .functions import read_file, num_students, init_managers
from PIL import Image 
import os

class Home(ctk.CTkFrame): 
    def __init__(self, master):
        super().__init__(master)

        init_managers()
        read_file() 

        ctk.CTkLabel(self, text="Number of students", font=("Montserrat", 48, "bold"), text_color="#3b8ed0").pack(pady=26, padx=16) 

        num, num_boys, num_girls = num_students() 
        frame = ctk.CTkFrame(self, corner_radius=26) 
        frame.pack(padx=26, pady=26)
        
        num_stud_frame = ctk.CTkFrame(frame, corner_radius=16)
        num_stud_frame.grid(row=0, column=1, padx=10, pady=10)
        
        num_boys_frame = ctk.CTkFrame(frame, corner_radius=16)
        num_boys_frame.grid(row=0, column=0, padx=10, pady=10)

        num_girls_frame = ctk.CTkFrame(frame, corner_radius=16)
        num_girls_frame.grid(row=0, column=2, padx=10, pady=10)

        try:
            img1 = Image.open(os.path.join("Images", "boy_girl.png"))
            img2 = Image.open(os.path.join("Images", "boy.png"))
            img3 = Image.open(os.path.join("Images", "girl.png"))
            
            boy_girl = ctk.CTkImage(light_image=img1, dark_image=img1, size=(200, 200))
            boy = ctk.CTkImage(light_image=img2, dark_image=img2, size=(200, 200))
            girl = ctk.CTkImage(light_image=img3, dark_image=img3, size=(200, 200))
            
            ctk.CTkLabel(num_stud_frame, text="", image=boy_girl).pack(padx=10)
            ctk.CTkLabel(num_boys_frame, text="", image=boy).pack(padx=10)
            ctk.CTkLabel(num_girls_frame, text="", image=girl).pack(padx=10)

        except: 
            ctk.CTkLabel(num_stud_frame, text="Number of\nstudents", font=("Montserrat", 24, "bold")).pack(padx=10, pady=10)
            ctk.CTkLabel(num_boys_frame, text="Number of\nboys", font=("Montserrat", 24, "bold")).pack(padx=10, pady=10)
            ctk.CTkLabel(num_girls_frame, text="Number of\ngirls", font=("Montserrat", 24, "bold")).pack(padx=10, pady=10)
       
        ctk.CTkLabel(num_stud_frame, text=f"{num}", font=("Montserrat", 24, "bold")).pack(padx=10, pady=10)
        ctk.CTkLabel(num_boys_frame, text=f"{num_boys}", font=("Montserrat", 24, "bold")).pack(padx=10, pady=10)
        ctk.CTkLabel(num_girls_frame, text=f"{num_girls}", font=("Montserrat", 24, "bold")).pack(padx=10, pady=10)





