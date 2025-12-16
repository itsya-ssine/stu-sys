import customtkinter as ctk 
import os 

from pages.side_bar import Sidebar
from pages.log_in import Login
from pages.home import Home

class App(ctk.CTk): 
    def __init__(self):
        super().__init__()

        self.title("Students System") 
        self.geometry("1200x600")
        
        try:
            self.iconbitmap(os.path.join("Icons", "app_icon.ico")) 
        except:
            pass

        ctk.set_appearance_mode("light") 
        ctk.set_default_color_theme("blue") 
        
        self.home_frame = Home(self) 
        self.home_frame.pack_forget() 

        self.side_frame = Sidebar(self, self.home_frame)
        self.side_frame.pack(padx=10, pady=10, fill="y", side='left') 

        self.login_form = Login(self, self.home_frame) 
        self.login_form.pack(padx=10, pady=10, fill="both", expand=True, side='left') 

if __name__ == "__main__":
    app = App() 
    app.mainloop() 
