import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="hhhhhh",
                database="student_management"
            )
            self.cursor = self.connection.cursor(dictionary=True)
            self._create_tables()
        except Error as e:
            print(f"Database connection error: {e}")
            exit(1)

    def _create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    sexe CHAR(1),
                    major VARCHAR(100)
                )
            """)
            
            # Notes table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    subject VARCHAR(100) NOT NULL,
                    grade FLOAT NOT NULL,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
                )
            """)
            
            # Absence notes table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS absence_notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    date_absence DATE NOT NULL,
                    reason VARCHAR(255),
                    justified BOOLEAN DEFAULT FALSE,
                    note_description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
                )
            """)
            
            self.connection.commit()
        except Error as e:
            print(f"Table creation error: {e}")

    def close(self):
        self.cursor.close()
        self.connection.close()


class StudentManager(Database):
    def create_student(self, student_id, first_name, last_name, email, sexe, major):
        query = """
            INSERT INTO students (id, first_name, last_name, email, sexe, major)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (student_id, first_name, last_name, email, sexe, major))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error creating student: {e}")
            return False

    def get_all_students(self):
        try:
            self.cursor.execute("SELECT * FROM students")
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching students: {e}")
            return []

    def get_student_by_id(self, student_id):
        try:
            self.cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching student: {e}")
            return None

    def update_student(self, student_id, first_name, last_name, email, sexe, major):
        query = """
            UPDATE students
            SET first_name=%s, last_name=%s, email=%s, sexe=%s, major=%s
            WHERE id=%s
        """
        try:
            self.cursor.execute(query, (first_name, last_name, email, sexe, major, student_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating student: {e}")
            return False

    def delete_student(self, student_id):
        try:
            self.cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error deleting student: {e}")
            return False

    def student_exists(self, student_id):
        try:
            self.cursor.execute("SELECT id FROM students WHERE id = %s", (student_id,))
            return self.cursor.fetchone() is not None
        except Error as e:
            print(f"Error checking student: {e}")
            return False


class NotesManager(Database):
    def add_note(self, student_id, subject, grade):
        query = """
            INSERT INTO notes (student_id, subject, grade)
            VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(query, (student_id, subject, grade))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error adding note: {e}")
            return False

    def get_notes_by_student(self, student_id):
        query = """
            SELECT id, subject, grade, date_added FROM notes
            WHERE student_id = %s
            ORDER BY date_added DESC
        """
        try:
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching notes: {e}")
            return []

    def get_average_grade(self, student_id):
        query = """
            SELECT AVG(grade) as average FROM notes
            WHERE student_id = %s
        """
        try:
            self.cursor.execute(query, (student_id,))
            result = self.cursor.fetchone()
            return result['average'] if result['average'] else 0
        except Error as e:
            print(f"Error calculating average: {e}")
            return 0

    def update_note(self, note_id, subject, grade):
        query = """
            UPDATE notes SET subject=%s, grade=%s WHERE id=%s
        """
        try:
            self.cursor.execute(query, (subject, grade, note_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating note: {e}")
            return False

    def delete_note(self, note_id):
        try:
            self.cursor.execute("DELETE FROM notes WHERE id=%s", (note_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error deleting note: {e}")
            return False

    def get_all_notes(self):
        query = "SELECT * FROM notes ORDER BY date_added DESC"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching all notes: {e}")
            return []


class AbsenceNotesManager(Database):
    def add_absence(self, student_id, date_absence, reason="", justified=False, note_description=""):
        query = """
            INSERT INTO absence_notes (student_id, date_absence, reason, justified, note_description)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (student_id, date_absence, reason, justified, note_description))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error adding absence: {e}")
            return False

    def get_absences_by_student(self, student_id):
        query = """
            SELECT id, date_absence, reason, justified, note_description, created_at
            FROM absence_notes
            WHERE student_id = %s
            ORDER BY date_absence DESC
        """
        try:
            self.cursor.execute(query, (student_id,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching absences: {e}")
            return []

    def get_absence_count(self, student_id):
        query = "SELECT COUNT(*) as count FROM absence_notes WHERE student_id = %s"
        try:
            self.cursor.execute(query, (student_id,))
            result = self.cursor.fetchone()
            return result['count'] if result else 0
        except Error as e:
            print(f"Error counting absences: {e}")
            return 0

    def get_justified_absence_count(self, student_id):
        query = "SELECT COUNT(*) as count FROM absence_notes WHERE student_id = %s AND justified = TRUE"
        try:
            self.cursor.execute(query, (student_id,))
            result = self.cursor.fetchone()
            return result['count'] if result else 0
        except Error as e:
            print(f"Error counting justified absences: {e}")
            return 0

    def update_absence(self, absence_id, reason="", justified=False, note_description=""):
        query = """
            UPDATE absence_notes
            SET reason=%s, justified=%s, note_description=%s
            WHERE id=%s
        """
        try:
            self.cursor.execute(query, (reason, justified, note_description, absence_id))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error updating absence: {e}")
            return False

    def delete_absence(self, absence_id):
        try:
            self.cursor.execute("DELETE FROM absence_notes WHERE id=%s", (absence_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error deleting absence: {e}")
            return False

    def get_all_absences(self):
        query = """
            SELECT a.id, a.student_id, s.first_name, s.last_name, a.date_absence,
                   a.reason, a.justified, a.note_description, a.created_at
            FROM absence_notes a
            JOIN students s ON a.student_id = s.id
            ORDER BY a.date_absence DESC
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching all absences: {e}")
            return []

    def get_class_absence_summary(self):
        query = """
            SELECT s.id, s.first_name, s.last_name,
                   COUNT(a.id) as total_absences,
                   SUM(CASE WHEN a.justified = TRUE THEN 1 ELSE 0 END) as justified_absences,
                   SUM(CASE WHEN a.justified = FALSE THEN 1 ELSE 0 END) as unjustified_absences
            FROM students s
            LEFT JOIN absence_notes a ON s.id = a.student_id
            GROUP BY s.id, s.first_name, s.last_name
            ORDER BY total_absences DESC
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching class summary: {e}")
            return []
