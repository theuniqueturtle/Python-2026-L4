import math
import numpy as np

from .student import Student
from .course import Course


class School:
    """Holds students, courses and marks, and does the maths (floor, GPA, sorting)."""

    def __init__(self):
        self.students = []   # list[Student]
        self.courses = []    # list[Course]
        self.marks = {}      # {course_id: {student_id: mark}}

    # ---- maths -------------------------------------------------
    @staticmethod
    def floor_mark(mark):
        """Round DOWN a mark to 1 decimal digit with math.floor (8.79 -> 8.7)."""
        return math.floor(round(mark * 10, 6)) / 10

    def calculate_gpa(self, student_id):
        """Weighted average of marks by credits, using numpy arrays."""
        credits, scores = [], []
        for course in self.courses:
            course_marks = self.marks.get(course.id, {})
            if student_id in course_marks:
                credits.append(course.credits)
                scores.append(course_marks[student_id])
        if not credits:
            return 0.0
        credits = np.array(credits, dtype=float)
        scores = np.array(scores, dtype=float)
        return float(np.sum(credits * scores) / np.sum(credits))

    def sort_students_by_gpa(self):
        """Sort the student list by GPA descending; return list of (student, gpa)."""
        gpas = np.array([self.calculate_gpa(s.id) for s in self.students])
        order = np.argsort(-gpas, kind="stable")
        self.students = [self.students[i] for i in order]
        return [(self.students[k], float(gpas[i])) for k, i in enumerate(order)]

    # ---- data access -------------------------------------------
    def find_student(self, student_id):
        return next((s for s in self.students if s.id == student_id), None)

    def find_course(self, course_id):
        return next((c for c in self.courses if c.id == course_id), None)

    def set_mark(self, course_id, student_id, mark):
        """Store a mark (floored to 1 decimal) for a student in a course."""
        self.marks.setdefault(course_id, {})[student_id] = self.floor_mark(mark)

    def get_marks(self, course_id):
        return self.marks.get(course_id)