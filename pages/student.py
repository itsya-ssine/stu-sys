class Student:
    Num_students = 0 
    def __init__(self, first_name, last_name, id, sexe, email, magor):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.magor = magor
        self.sexe = sexe

        Student.Num_students += 1

    def __str__(self):
        return f"{self.id}, {self.first_name}, {self.last_name}, {self.email}, {self.magor}, {self.sexe}" 

    def __eq__(self, s2): 
        return self.id == s2.id

    def is_male(self):
        return self.sexe.strip() == 'M' 