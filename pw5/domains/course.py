class Course:
    """A course with an ID, a name and a number of credits."""

    def __init__(self, course_id, name, credits):
        self.id = course_id
        self.name = name
        self.credits = credits

    def __str__(self):
        return f"{self.id} - {self.name} ({self.credits} credits)"