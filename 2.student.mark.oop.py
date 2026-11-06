from abc import ABC, abstractmethod

def read_text(prompt):
    return input(prompt).strip()


def read_int(prompt, minimum=None):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"The number must be at least {minimum}.")
            continue
        return value


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number.")

class Entity(ABC):
    """Base class: anything with an ID and a name that can be typed in and listed.

    Encapsulation: the attributes are protected (_id, _name) and only exposed
    through read-only properties.
    Polymorphism: every subclass must provide its own input() and list().
    """

    def __init__(self, entity_id="", name=""):
        self._id = entity_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @abstractmethod
    def input(self):
        """Ask the user for the data of this object."""

    @abstractmethod
    def list(self):
        """Print this object."""

class Student(Entity):
    def __init__(self, student_id="", name="", dob=""):
        super().__init__(student_id, name)
        self._dob = dob

    @property
    def dob(self):
        return self._dob

    def input(self):
        self._id = read_text("  ID of the student: ")
        self._name = read_text("  Name of the student: ")
        self._dob = read_text("  DoB of the student: ")

    def list(self):
        print(f"Student ID: {self._id} | Name: {self._name} | DoB: {self._dob}")


class Course(Entity):
    """A course. It owns the marks of its students (private to the course)."""

    def __init__(self, course_id="", name=""):
        super().__init__(course_id, name)
        self.__marks = {}          # {student_id: mark}, private

    def input(self):
        self._id = read_text("  ID of the course: ")
        self._name = read_text("  Name of the course: ")

    def list(self):
        print(f"Course ID: {self._id} | Name: {self._name}")

    # ---- marks ----
    def set_mark(self, student_id, mark):
        self.__marks[student_id] = mark

    def get_mark(self, student_id):
        return self.__marks.get(student_id)

    def has_marks(self):
        return bool(self.__marks)

    def list_marks(self, students):
        for s in students:
            mark = self.get_mark(s.id)
            if mark is not None:
                print(f"ID: {s.id} | Name: {s.name} | Mark: {mark}")


class School:
    """Holds the students and courses and runs the menu."""

    def __init__(self):
        self.__students = []
        self.__courses = []

   
    @staticmethod
    def __create(entity_class, label):
        n = read_int(f"Enter number of {label}s: ", minimum=1)
        items = []
        for i in range(n):
            print(f"\nEnter information of {label} {i + 1}")
            item = entity_class()
            item.input()                 
            items.append(item)
        return items

    @staticmethod
    def __show(items, empty_message):
        if not items:
            print(empty_message)
            return
        for item in items:
            item.list()                 

    @staticmethod
    def __find(items, entity_id):
        return next((i for i in items if i.id == entity_id), None)

   
    def input_students(self):
        self.__students = self.__create(Student, "student")

    def input_courses(self):
        self.__courses = self.__create(Course, "course")

    def input_marks(self):
        if not self.__courses:
            print("The courses are unavailable")
            return
        if not self.__students:
            print("Cannot find any student")
            return

        self.__show(self.__courses, "")
        course = self.__find(self.__courses, read_text("Enter the course ID: "))
        if course is None:
            print("Cannot find this course")
            return

        print(f"Enter marks for course {course.name}")
        for s in self.__students:
            mark = read_float(f"Mark of {s.id} - {s.name}: ")
            course.set_mark(s.id, mark)
        print("Success")

    def list_courses(self):
        self.__show(self.__courses, "There are no courses")

    def list_students(self):
        self.__show(self.__students, "There are no students")

    def show_marks(self):
        if not self.__courses:
            print("No course found")
            return
        if not self.__students:
            print("Cannot find any student")
            return

        course = self.__find(self.__courses, read_text("Choose the course ID: "))
        if course is None:
            print("Cannot find this course")
        elif not course.has_marks():
            print("No marks have been entered for this course")
        else:
            course.list_marks(self.__students)

    # ---- menu ----
    def run(self):
        actions = {
            "1": self.input_students,
            "2": self.input_courses,
            "3": self.input_marks,
            "4": self.list_courses,
            "5": self.list_students,
            "6": self.show_marks,
        }
        while True:
            print("\n" + "=" * 40)
            print("     STUDENT MARK MANAGEMENT SYSTEM")
            print("=" * 40)
            print("1. Enter number and information of students")
            print("2. Enter number and information of courses")
            print("3. Enter student marks for a course")
            print("4. List courses")
            print("5. List students")
            print("6. Show marks by course")
            print("0. Exit")
            print("=" * 40)
            choice = read_text("Your choice (0-6): ")
            if choice == "0":
                print("\nProgram exited.")
                break
            action = actions.get(choice)
            if action is None:
                print("\nInvalid choice, please try again!")
            else:
                action()


if __name__ == "__main__":
    School().run()
