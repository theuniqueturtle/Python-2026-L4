import math
import numpy as np

from .student import Student
from .course import Course


class School:

    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = {}

    @staticmethod
    def floor_mark(mark):
        return math.floor(round(mark * 10, 6)) / 10

    def calculate_gpa(self, student_id):
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
        gpas = np.array([self.calculate_gpa(s.id) for s in self.students])
        order = np.argsort(-gpas, kind="stable")
        self.students = [self.students[i] for i in order]
        return [(self.students[k], float(gpas[i])) for k, i in enumerate(order)]

    def find_student(self, student_id):
        return next((s for s in self.students if s.id == student_id), None)

    def find_course(self, course_id):
        return next((c for c in self.courses if c.id == course_id), None)

    def set_mark(self, course_id, student_id, mark):
        self.marks.setdefault(course_id, {})[student_id] = self.floor_mark(mark)

    def get_marks(self, course_id):
        return self.marks.get(course_id)
