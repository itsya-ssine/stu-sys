import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Naoki1337@012",
                database="student_management"
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except:
            exit(1)

    def close(self):
        self.cursor.close()
        self.connection.close()


class StudentManager(Database):

    def create_student(self, first_name, last_name, email, sexe, major):
        query = """
            INSERT INTO students (first_name, last_name, email, sexe, major)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (first_name, last_name, email, sexe, major))
        self.connection.commit()

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def get_student_by_id(self, student_id):
        self.cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        return self.cursor.fetchone()

    def update_student(self, student_id, first_name, last_name, email, sexe, major):
        query = """
            UPDATE students
            SET first_name=%s, last_name=%s, email=%s, sexe=%s, major=%s
            WHERE id=%s
        """
        self.cursor.execute(query, (first_name, last_name, email, sexe, major, student_id))
        self.connection.commit()

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
        self.connection.commit()


class NotesManager(Database):

    def add_note(self, student_id, subject, grade):
        query = """
            INSERT INTO notes (student_id, subject, grade)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (student_id, subject, grade))
        self.connection.commit()

    def get_notes_by_student(self, student_id):
        query = """
            SELECT subject, grade FROM notes
            WHERE student_id = %s
        """
        self.cursor.execute(query, (student_id,))
        return self.cursor.fetchall()

    def update_note(self, note_id, subject, grade):
        query = """
            UPDATE notes SET subject=%s, grade=%s WHERE id=%s
        """
        self.cursor.execute(query, (subject, grade, note_id))
        self.connection.commit()

    def delete_note(self, note_id):
        self.cursor.execute("DELETE FROM notes WHERE id=%s", (note_id,))
        self.connection.commit()



if __name__ == "__main__":
    students = StudentManager()
    notes = NotesManager()

    students.create_student("John", "Doe", "john.doe@email.com", "Male", "Computer Science")

    all_students = students.get_all_students()
    print(all_students)

    student_id = all_students[0]["id"]

    notes.add_note(student_id, "Math", 15.5)
    notes.add_note(student_id, "Physics", 14)

    print(notes.get_notes_by_student(student_id))

    students.close()
    notes.close()
