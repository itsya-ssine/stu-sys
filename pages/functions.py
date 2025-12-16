from .student import Student
from DB.db_manager import StudentManager, NotesManager, AbsenceNotesManager
import mysql.connector
from mysql.connector import Error

Buttons = []
Students_data = []

student_manager = None
notes_manager = None
absence_manager = None

def init_managers():
    global student_manager, notes_manager, absence_manager
    try:
        student_manager = StudentManager()
        notes_manager = NotesManager()
        absence_manager = AbsenceNotesManager()
    except Exception as e:
        print(f"Error initializing managers: {e}")


def read_file():
    Students_data.clear()
    try:
        if not student_manager:
            init_managers()
        
        students = student_manager.get_all_students()
        for row in students:
            stud = Student(
                row['first_name'],
                row['last_name'],
                row['id'],
                row['sexe'],
                row['email'],
                row['major']
            )
            Students_data.append(stud)
    except Error as e:
        print(f"Database error: {e}")


def add_stud_file(stud):
    try:
        if not student_manager:
            init_managers()
        
        success = student_manager.create_student(
            stud.id,
            stud.first_name,
            stud.last_name,
            stud.email,
            stud.sexe,
            stud.major
        )
        
        if success:
            Students_data.append(stud)
        return success

    except Error as e:
        print(f"Insert error: {e}")
        return False


def edit_file():
    try:
        if not student_manager:
            init_managers()
        
        for stud in Students_data:
            student_manager.update_student(
                stud.id,
                stud.first_name,
                stud.last_name,
                stud.email,
                stud.sexe,
                stud.major
            )

    except Error as e:
        print(f"Update error: {e}")


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
        if not student_manager:
            init_managers()
        
        stud = Students_data[index]
        success = student_manager.delete_student(stud.id)
        
        if success:
            del Students_data[index]
        
        return success

    except (IndexError, Error) as e:
        print(f"Delete error: {e}")
        return False


def get_student_notes(student_id):
    if not notes_manager:
        init_managers()
    return notes_manager.get_notes_by_student(student_id)


def add_student_note(student_id, subject, grade):
    if not notes_manager:
        init_managers()
    return notes_manager.add_note(student_id, subject, grade)


def delete_student_note(note_id):
    if not notes_manager:
        init_managers()
    return notes_manager.delete_note(note_id)


def get_student_average_grade(student_id):
    if not notes_manager:
        init_managers()
    return notes_manager.get_average_grade(student_id)


def get_student_absences(student_id):
    if not absence_manager:
        init_managers()
    return absence_manager.get_absences_by_student(student_id)


def add_student_absence(student_id, date_absence, reason="", justified=False, note_description=""):
    if not absence_manager:
        init_managers()
    return absence_manager.add_absence(student_id, date_absence, reason, justified, note_description)


def get_absence_count(student_id):
    if not absence_manager:
        init_managers()
    return absence_manager.get_absence_count(student_id)


def get_justified_absence_count(student_id):
    if not absence_manager:
        init_managers()
    return absence_manager.get_justified_absence_count(student_id)


def get_class_absence_summary():
    if not absence_manager:
        init_managers()
    return absence_manager.get_class_absence_summary()


def generate_class_report():
    if not student_manager or not absence_manager or not notes_manager:
        init_managers()
    
    report = {
        'total_students': len(Students_data),
        'males': sum(1 for s in Students_data if s.is_male()),
        'females': len(Students_data) - sum(1 for s in Students_data if s.is_male()),
        'absence_summary': absence_manager.get_class_absence_summary(),
        'all_notes': notes_manager.get_all_notes(),
        'all_absences': absence_manager.get_all_absences()
    }
    return report
