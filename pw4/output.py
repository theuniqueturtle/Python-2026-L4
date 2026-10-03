"""Output module: everything that is drawn on screen with curses."""
import curses


def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)    # title / highlight
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # prompts
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # errors
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   # hints / success


def title(win, text):
    """Clear the screen and draw a title bar."""
    win.clear()
    _, w = win.getmaxyx()
    win.addstr(0, 0, text.center(w - 1), curses.color_pair(1) | curses.A_BOLD)
    win.move(2, 0)


def say(win, text="", pair=0, bold=False):
    attr = curses.color_pair(pair) | (curses.A_BOLD if bold else 0)
    win.addstr(text + "\n", attr)


def pause(win):
    say(win)
    say(win, "Press any key to go back to the menu...", 4)
    win.getch()


def draw_menu(win, items, selected):
    title(win, "STUDENT MARK MANAGEMENT SYSTEM")
    for i, item in enumerate(items):
        label = f" {i + 1}. {item} "
        if i == selected:
            win.addstr(label + "\n", curses.color_pair(1) | curses.A_BOLD)
        else:
            win.addstr(label + "\n")
    win.addstr("\nUse UP/DOWN + Enter, or press a number key.", curses.color_pair(4))


def show_error(win, text):
    say(win, text, 3)


def show_success(win):
    say(win, "\nSuccess", 2)


def show_courses(win, courses):
    if not courses:
        return show_error(win, "There are no courses")
    say(win, f"{'ID':<12}{'Name':<30}{'Credits':>7}", bold=True)
    for c in courses:
        say(win, f"{c.id:<12}{c.name:<30}{c.credits:>7}")


def show_students(win, students):
    if not students:
        return show_error(win, "There are no students")
    say(win, f"{'ID':<12}{'Name':<30}{'DoB':<12}", bold=True)
    for s in students:
        say(win, f"{s.id:<12}{s.name:<30}{s.dob:<12}")


def show_course_marks(win, students, course_marks):
    say(win, f"{'ID':<12}{'Name':<30}{'Mark':>6}", bold=True)
    for s in students:
        if s.id in course_marks:
            say(win, f"{s.id:<12}{s.name:<30}{course_marks[s.id]:>6.1f}")


def show_gpa(win, student, gpa):
    say(win, f"\nStudent: {student.name}")
    say(win, f"GPA: {gpa:.2f}", 2, bold=True)


def show_ranking(win, ranking):
    say(win, f"{'Rank':<6}{'ID':<12}{'Name':<30}{'GPA':>6}", bold=True)
    for i, (s, gpa) in enumerate(ranking, 1):
        say(win, f"{i:<6}{s.id:<12}{s.name:<30}{gpa:>6.2f}")