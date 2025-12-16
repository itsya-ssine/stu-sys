import customtkinter as ctk
from PIL import Image
from .functions import Buttons 
import os

class Login(ctk.CTkFrame):
    def __init__(self, master, home): 
        super().__init__(master)
        self.home_frame = home 
        self.count = 0 
        self.username = "naoki"
        self.PWD = "naoki1234"

        try:
            light_img = Image.open(os.path.join("Images", "link.png"))
            dark_img = Image.open(os.path.join("Images", "link.png"))
            title_image = ctk.CTkImage(light_image=light_img, dark_image=dark_img, size=(300, 300)) 
            ctk.CTkLabel(self, text="", image=title_image).pack(padx=16) 
        except FileNotFoundError:
            ctk.CTkLabel(self, text="WELCOME", font=("Lostar", 100), text_color="#0c93ff").pack(padx=16) 

        ctk.CTkLabel(self, text="username & password please:", font=("Gill Sans Nova", 12)).pack(padx=10) 

        username_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Username", 
            width=400, 
            height=45,
            border_width=0, 
            font=("Gill Sans Nova", 14), 
            corner_radius=16)
        username_entry.pack(padx=16, pady=8)

        password_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Password", 
            width=400, 
            height=45, 
            show='•',
            border_width=0, 
            font=("Gill Sans Nova", 14), 
            corner_radius=16)
        password_entry.pack(padx=16)

        ctk.CTkButton(
            self, 
            text="Log In", 
            width=400, 
            height=45, 
            corner_radius=16, 
            cursor="hand2",
            font=("Gill Sans Nova", 18, "bold"),
            command=lambda: self.log_in(incorrect, username_entry, password_entry)
        ).pack(padx=16, pady=8) 

        incorrect = ctk.CTkLabel(self, 
                                 text="Username or Password incorrect!", 
                                 font=("Gill Sans Nova", 12), 
                                 text_color="red") 

    def log_in(self, incorrect, username_entry, password_entry):
        if self.count >= 3:
            incorrect.configure(text="Try again later!", text_color="red") 
            return

        if username_entry.get() == self.username and password_entry.get() == self.PWD: 
            self.valid_login()
        else:
            password_entry.delete(0, ctk.END)   
            incorrect.pack(padx=16, pady=4)
            self.count += 1

    def valid_login(self):
        from .functions import init_managers
        init_managers()
        
        for button in Buttons:
            button.configure(state="normal") 

        self.pack_forget() 
        self.home_frame.pack(padx=10, pady=10, fill="both", expand=True, side='left')


