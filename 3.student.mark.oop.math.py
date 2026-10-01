import math
import curses
import numpy as np

def floor_mark(mark):
    """Round DOWN a mark to 1 decimal digit using math.floor (8.79 -> 8.7)."""
    return math.floor(round(mark * 10, 6)) / 10

def calculate_gpa(student_id, courses, marks):
    """Weighted average of marks by credits for one student (numpy arrays)."""
    credits, scores = [], []
    for c in courses:
        cid = c["ID_course"]
        if cid in marks and student_id in marks[cid]:
            credits.append(c["credits"])
            scores.append(marks[cid][student_id])
    if not credits:
        return 0.0
    credits = np.array(credits, dtype=float)
    scores = np.array(scores, dtype=float)
    return float(np.sum(credits * scores) / np.sum(credits))

def sort_students_by_gpa(students, courses, marks):
    """Return list of (student, gpa) sorted by GPA descending."""
    gpas = np.array([calculate_gpa(s["id"], courses, marks) for s in students])
    order = np.argsort(-gpas, kind="stable")
    return [(students[i], float(gpas[i])) for i in order]

def title(win, text):
    """Clear the screen and draw a title bar."""
    win.clear()
    _, w = win.getmaxyx()
    win.addstr(0, 0, text.center(w - 1), curses.color_pair(1) | curses.A_BOLD)
    win.move(2, 0)

def say(win, text="", pair=0, bold=False):
    attr = curses.color_pair(pair) | (curses.A_BOLD if bold else 0)
    win.addstr(text + "\n", attr)

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
            say(win, "Please enter a whole number.", 3)

def ask_float(win, text):
    while True:
        try:
            return float(ask(win, text))
        except ValueError:
            say(win, "Please enter a number.", 3)

def pause(win):
    say(win)
    say(win, "Press any key to go back to the menu...", 4)
    win.getch()

def input_students(win):
    title(win, "ENTER STUDENTS")
    n = ask_int(win, "Enter number of students: ")
    students = []
    for i in range(n):
        say(win, f"\nStudent {i + 1}", bold=True)
        students.append({
            "id": ask(win, "  ID: "),
            "name": ask(win, "  Name: "),
            "DoB": ask(win, "  DoB: "),
        })
    say(win, "\nSuccess", 2)
    pause(win)
    return students


def input_courses(win):
    title(win, "ENTER COURSES")
    n = ask_int(win, "Enter number of courses: ")
    courses = []
    for i in range(n):
        say(win, f"\nCourse {i + 1}", bold=True)
        courses.append({
            "ID_course": ask(win, "  ID: "),
            "Name_course": ask(win, "  Name: "),
            "credits": ask_int(win, "  Credits: "),
        })
    say(win, "\nSuccess", 2)
    pause(win)
    return courses


def input_marks(win, courses, students, marks):
    title(win, "ENTER MARKS")
    if not courses:
        say(win, "The courses are unavailable", 3)
        return pause(win)
    if not students:
        say(win, "Cannot find any student", 3)
        return pause(win)

    for c in courses:
        say(win, f"Course ID: {c['ID_course']} | Name: {c['Name_course']} | Credits: {c['credits']}")
    course_id = ask(win, "\nEnter the course ID: ")
    if not any(c["ID_course"] == course_id for c in courses):
        say(win, f"Cannot find course ID {course_id}", 3)
        return pause(win)

    marks.setdefault(course_id, {})
    say(win)
    for s in students:
        raw = ask_float(win, f"Mark of {s['id']} - {s['name']}: ")
        marks[course_id][s["id"]] = floor_mark(raw)   
    say(win, "\nSuccess", 2)
    pause(win)


def list_courses(win, courses):
    title(win, "COURSES")
    if not courses:
        say(win, "There are no courses", 3)
    else:
        say(win, f"{'ID':<12}{'Name':<30}{'Credits':>7}", bold=True)
        for c in courses:
            say(win, f"{c['ID_course']:<12}{c['Name_course']:<30}{c['credits']:>7}")
    pause(win)


def list_students(win, students):
    title(win, "STUDENTS")
    if not students:
        say(win, "There are no students", 3)
    else:
        say(win, f"{'ID':<12}{'Name':<30}{'DoB':<12}", bold=True)
        for s in students:
            say(win, f"{s['id']:<12}{s['name']:<30}{s['DoB']:<12}")
    pause(win)


def show_marks(win, courses, students, marks):
    title(win, "MARKS BY COURSE")
    if not courses:
        say(win, "No course found", 3)
        return pause(win)
    if not students:
        say(win, "Cannot find any student", 3)
        return pause(win)

    course_id = ask(win, "Choose the course ID: ")
    if course_id not in marks:
        say(win, "No marks have been entered for this course", 3)
        return pause(win)

    say(win)
    say(win, f"{'ID':<12}{'Name':<30}{'Mark':>6}", bold=True)
    for s in students:
        if s["id"] in marks[course_id]:
            say(win, f"{s['id']:<12}{s['name']:<30}{marks[course_id][s['id']]:>6.1f}")
    pause(win)


def show_gpa(win, courses, students, marks):
    title(win, "GPA OF A STUDENT")
    if not students:
        say(win, "Cannot find any student", 3)
        return pause(win)

    sid = ask(win, "Enter student ID: ")
    student = next((s for s in students if s["id"] == sid), None)
    if student is None:
        say(win, f"Cannot find student ID {sid}", 3)
    else:
        gpa = calculate_gpa(sid, courses, marks)
        say(win, f"\nStudent: {student['name']}")
        say(win, f"GPA: {gpa:.2f}", 2, bold=True)
    pause(win)


def show_sorted_by_gpa(win, courses, students, marks):
    title(win, "STUDENTS SORTED BY GPA (DESCENDING)")
    if not students:
        say(win, "Cannot find any student", 3)
        return pause(win)

    ranked = sort_students_by_gpa(students, courses, marks)
    students[:] = [s for s, _ in ranked]          
    say(win, f"{'Rank':<6}{'ID':<12}{'Name':<30}{'GPA':>6}", bold=True)
    for i, (s, gpa) in enumerate(ranked, 1):
        say(win, f"{i:<6}{s['id']:<12}{s['name']:<30}{gpa:>6.2f}")
    pause(win)

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


def draw_menu(win, selected):
    title(win, "STUDENT MARK MANAGEMENT SYSTEM")
    for i, item in enumerate(MENU):
        label = f" {i + 1}. {item} "
        if i == selected:
            win.addstr(label + "\n", curses.color_pair(1) | curses.A_BOLD)
        else:
            win.addstr(label + "\n")
    win.addstr("\nUse UP/DOWN + Enter, or press a number key.", curses.color_pair(4))


def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)   
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   
    stdscr.keypad(True)
    stdscr.scrollok(True)
    curses.curs_set(0)

    students, courses, marks = [], [], {}
    selected = 0

    while True:
        draw_menu(stdscr, selected)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(MENU)
            continue
        if key == curses.KEY_DOWN:
            selected = (selected + 1) % len(MENU)
            continue
        if ord("1") <= key <= ord(str(len(MENU))):
            selected = key - ord("1")
        elif key not in (10, 13, curses.KEY_ENTER):
            continue

        if selected == 0:
            students = input_students(stdscr)
        elif selected == 1:
            courses = input_courses(stdscr)
        elif selected == 2:
            input_marks(stdscr, courses, students, marks)
        elif selected == 3:
            list_courses(stdscr, courses)
        elif selected == 4:
            list_students(stdscr, students)
        elif selected == 5:
            show_marks(stdscr, courses, students, marks)
        elif selected == 6:
            show_gpa(stdscr, courses, students, marks)
        elif selected == 7:
            show_sorted_by_gpa(stdscr, courses, students, marks)
        elif selected == 8:
            break


if __name__ == "__main__":
    curses.wrapper(main)
