"""Main script: coordinates input, output and the domain classes."""
import curses

import input as inp
import output as out
from domains import School

MENU = [
    "Enter students",
    "Enter courses",
    "Enter marks for a course",
    "List courses",
    "List students",
    "Show marks by course",
    "Show GPA of a student",
    "Sort students by GPA (descending)",
    "Exit",
]


def enter_students(win, school):
    out.title(win, "ENTER STUDENTS")
    school.students = inp.read_students(win)
    out.show_success(win)
    out.pause(win)


def enter_courses(win, school):
    out.title(win, "ENTER COURSES")
    school.courses = inp.read_courses(win)
    out.show_success(win)
    out.pause(win)


def enter_marks(win, school):
    out.title(win, "ENTER MARKS")
    if not school.courses:
        out.show_error(win, "The courses are unavailable")
    elif not school.students:
        out.show_error(win, "Cannot find any student")
    else:
        out.show_courses(win, school.courses)
        course_id = inp.read_course_id(win)
        if school.find_course(course_id) is None:
            out.show_error(win, f"Cannot find course ID {course_id}")
        else:
            for student, mark in inp.read_marks(win, school.students):
                school.set_mark(course_id, student.id, mark)
            out.show_success(win)
    out.pause(win)


def list_courses(win, school):
    out.title(win, "COURSES")
    out.show_courses(win, school.courses)
    out.pause(win)


def list_students(win, school):
    out.title(win, "STUDENTS")
    out.show_students(win, school.students)
    out.pause(win)


def show_marks(win, school):
    out.title(win, "MARKS BY COURSE")
    if not school.courses:
        out.show_error(win, "No course found")
    elif not school.students:
        out.show_error(win, "Cannot find any student")
    else:
        course_id = inp.read_course_id(win)
        course_marks = school.get_marks(course_id)
        if course_marks is None:
            out.show_error(win, "No marks have been entered for this course")
        else:
            out.say(win)
            out.show_course_marks(win, school.students, course_marks)
    out.pause(win)


def show_gpa(win, school):
    out.title(win, "GPA OF A STUDENT")
    if not school.students:
        out.show_error(win, "Cannot find any student")
    else:
        sid = inp.read_student_id(win)
        student = school.find_student(sid)
        if student is None:
            out.show_error(win, f"Cannot find student ID {sid}")
        else:
            out.show_gpa(win, student, school.calculate_gpa(sid))
    out.pause(win)


def show_ranking(win, school):
    out.title(win, "STUDENTS SORTED BY GPA (DESCENDING)")
    if not school.students:
        out.show_error(win, "Cannot find any student")
    else:
        out.show_ranking(win, school.sort_students_by_gpa())
    out.pause(win)


ACTIONS = [
    enter_students, enter_courses, enter_marks, list_courses,
    list_students, show_marks, show_gpa, show_ranking,
]


def main(stdscr):
    out.init_colors()
    stdscr.keypad(True)
    stdscr.scrollok(True)
    curses.curs_set(0)

    school = School()
    selected = 0
    while True:
        out.draw_menu(stdscr, MENU, selected)
        selected, confirmed = inp.menu_key(stdscr, selected, len(MENU))
        if not confirmed:
            continue
        if selected == len(MENU) - 1:   # Exit
            break
        ACTIONS[selected](stdscr, school)


if __name__ == "__main__":
    curses.wrapper(main)