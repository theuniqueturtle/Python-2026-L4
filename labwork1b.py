def number_of_student():
    """Enter number of students"""
    return int(input("Enter number of students: "))


def info_of_student(n):
    """Enter information of each student"""
    students = []
    for i in range(n):
        print(f"Enter information of student {i + 1}")
        student_id = input("Enter ID of the student: ").strip()
        student_name = input("Enter student name: ").strip()
        student_dob = input("Enter student DoB: ").strip()
        students.append({
            "id": student_id,
            "name": student_name,
            "DoB": student_dob
        })
    return students


def number_of_course():
    """Enter the number of courses"""
    return int(input("Enter the number of courses: "))


def info_of_course(n):
    """Enter the information of each course"""
    courses = []
    for i in range(n):
        print(f"Enter information of course {i + 1}")
        course_id = input("Enter ID of the course: ").strip()
        course_name = input("Enter name of the course: ").strip()
        courses.append({
            "ID_course": course_id,
            "Name_course": course_name
        })
    return courses


def input_marks_for_student_in_course(courses, students, marks):
    """Enter marks for all students in a chosen course"""
    if not courses:
        print("The courses are unavailable")
        return
    if not students:
        print("Cannot find any student")
        return

    for course in courses:
        print(f"Course ID: {course['ID_course']} | Course name: {course['Name_course']}")

    course_id = input("Enter the course ID you want to input marks for: ").strip()

    course_exists = any(c['ID_course'] == course_id for c in courses)
    if not course_exists:
        print(f"Cannot find course ID {course_id}")
        return

    if course_id not in marks:
        marks[course_id] = {}

    print(f"Enter marks for course ID: {course_id}")

    for student in students:
        mark = float(input(f"Enter the mark of student ID: {student['id']}, name: {student['name']}: "))
        marks[course_id][student['id']] = mark
    print("Success")


def list_course(courses):
    if not courses:
        print("There are no courses")
        return
    for c in courses:
        print(f"Course name: {c['Name_course']}, course ID: {c['ID_course']}")


def list_student(students):
    if not students:
        print("There are no students")
        return
    for s in students:
        print(f"Student name: {s['name']}, student ID: {s['id']}, DoB: {s['DoB']}")


def show_student_mark(courses, students, marks):
    if not courses:
        print("No course found")
        return
    if not students:
        print("Cannot find any student")
        return

    course_id = input("Choose the course you want to view: ").strip()
    if course_id not in marks:
        print("No marks have been entered for this course")
        return

    for s in students:
        s_id = s['id']
        if s_id in marks[course_id]:
            print(f"ID: {s_id}, Name: {s['name']}, Mark: {marks[course_id][s_id]}")


def main():
    students = []
    courses = []
    marks = {}
    while True:
        print("\n" + "=" * 40)
        print("     STUDENT MARK MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Enter number and information of students")
        print("2. Enter number and information of courses")
        print("3. Enter student marks for a course")
        print("4. View the list of courses")
        print("5. View the list of students")
        print("6. View marks by course")
        print("0. Exit")
        print("=" * 40)
        choice = input("Your choice (0-6): ").strip()
        if choice == '1':
            num = number_of_student()
            students = info_of_student(num)
        elif choice == '2':
            num = number_of_course()
            courses = info_of_course(num)
        elif choice == '3':
            input_marks_for_student_in_course(courses, students, marks)
        elif choice == '4':
            list_course(courses)
        elif choice == '5':
            list_student(students)
        elif choice == '6':
            show_student_mark(courses, students, marks)
        elif choice == '0':
            print("\nProgram exited.")
            break
        else:
            print("\nInvalid choice, please try again!")

if __name__ == "__main__":
    main()