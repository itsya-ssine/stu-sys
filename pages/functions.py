from .student import Student
import mysql.connector
from mysql.connector import Error

Buttons = []
Students_data = []


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Naoki1337@012",
        database="student_management"
    )

def read_file():
    Students_data.clear()
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, first_name, last_name, email, sexe, major FROM students")
        rows = cursor.fetchall()

        for row in rows:
            id, first_name, last_name, email, sexe, major = row
            stud = Student(first_name, last_name, id, sexe, email, major)
            Students_data.append(stud)

        cursor.close()
        conn.close()

    except Error as e:
        print("Database error:", e)


def add_stud_file(stud):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO students (id, first_name, last_name, email, sexe, major)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            stud.id,
            stud.first_name,
            stud.last_name,
            stud.email,
            stud.sexe,
            stud.magor
        ))

        conn.commit()
        cursor.close()
        conn.close()

        Students_data.append(stud)

    except Error as e:
        print("Insert error:", e)



def edit_file():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        for stud in Students_data:
            query = """
                UPDATE students
                SET first_name=%s, last_name=%s, email=%s, sexe=%s, major=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                stud.first_name,
                stud.last_name,
                stud.email,
                stud.sexe,
                stud.magor,
                stud.id
            ))

        conn.commit()
        cursor.close()
        conn.close()

    except Error as e:
        print("Update error:", e)



def check_float(value):
    try:
        return int(value)
    except ValueError:
        return -1


def num_students():
    total = len(Students_data)
    males = sum(1 for stud in Students_data if stud.is_male())
    females = total - males
    return total, males, females


def id_search(id):
    for i, stud in enumerate(Students_data):
        if str(stud.id).strip() == str(id):
            return i
    return -1


def name_search(name):
    for i, stud in enumerate(Students_data):
        if stud.first_name.strip().lower() == name.lower():
            return i
    return -1


def remove_student(index):
    try:
        stud = Students_data[index]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM students WHERE id = %s", (stud.id,))
        conn.commit()

        cursor.close()
        conn.close()

        del Students_data[index]

    except (IndexError, Error) as e:
        print("Delete error:", e)
