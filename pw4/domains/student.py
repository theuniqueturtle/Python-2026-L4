class Student:
    """A student with an ID, a name and a date of birth."""

    def __init__(self, student_id, name, dob):
        self.id = student_id
        self.name = name
        self.dob = dob

    def __str__(self):
        return f"{self.id} - {self.name} ({self.dob})"