import curses

import output
import storage
from domains import Student, Course


def ask(win, text):
    win.addstr(text, curses.color_pair(2))
    curses.echo()
    curses.curs_set(1)
    value = win.getstr().decode("utf-8").strip()
    curses.noecho()
    curses.curs_set(0)
    return value


def ask_int(win, text):
    while True:
        try:
            return int(ask(win, text))
        except ValueError:
            output.show_error(win, "Please enter a whole number.")


def ask_float(win, text):
    while True:
        try:
            return float(ask(win, text))
        except ValueError:
            output.show_error(win, "Please enter a number.")


def menu_key(win, selected, n_items):
    key = win.getch()
    if key == curses.KEY_UP:
        return (selected - 1) % n_items, False
    if key == curses.KEY_DOWN:
        return (selected + 1) % n_items, False
    if ord("1") <= key <= ord(str(n_items)):
        return key - ord("1"), True
    if key in (10, 13, curses.KEY_ENTER):
        return selected, True
    return selected, False


def read_students(win):
    n = ask_int(win, "Enter number of students: ")
    students = []
    for i in range(n):
        output.say(win, f"\nStudent {i + 1}", bold=True)
        students.append(Student(
            ask(win, "  ID: "),
            ask(win, "  Name: "),
            ask(win, "  DoB: "),
        ))
    storage.write_rows(storage.STUDENTS_FILE, [[s.id, s.name, s.dob] for s in students])
    output.show_saved(win, "students.txt")
    return students


def read_courses(win):
    n = ask_int(win, "Enter number of courses: ")
    courses = []
    for i in range(n):
        output.say(win, f"\nCourse {i + 1}", bold=True)
        courses.append(Course(
            ask(win, "  ID: "),
            ask(win, "  Name: "),
            ask_int(win, "  Credits: "),
        ))
    storage.write_rows(storage.COURSES_FILE, [[c.id, c.name, c.credits] for c in courses])
    output.show_saved(win, "courses.txt")
    return courses


def read_course_id(win):
    return ask(win, "\nEnter the course ID: ")


def read_student_id(win):
    return ask(win, "Enter student ID: ")


def read_marks(win, school, course_id):
    output.say(win)
    for s in school.students:
        mark = ask_float(win, f"Mark of {s.id} - {s.name}: ")
        school.set_mark(course_id, s.id, mark)

    rows = [
        [cid, sid, f"{mark:.1f}"]
        for cid, course_marks in school.marks.items()
        for sid, mark in course_marks.items()
    ]
    storage.write_rows(storage.MARKS_FILE, rows)
    output.show_saved(win, "marks.txt")
