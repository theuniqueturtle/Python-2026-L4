"""Storage module: text files, pickle + compression (students.dat), CSV export.

students.dat  = the data (students, courses, marks) serialised with `pickle`
                and compressed with zlib (DEFLATE).
*.txt         = written by the input functions (see input.py).
*.csv         = exported with pandas, loaded back into DataFrames for queries.
"""
import csv
import os
import pickle
import zlib

import pandas as pd

from domains import Student, Course

# Everything is stored next to this script, whatever the current directory is.
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
COURSES_FILE = os.path.join(DATA_DIR, "courses.txt")
MARKS_FILE = os.path.join(DATA_DIR, "marks.txt")
DAT_FILE = os.path.join(DATA_DIR, "students.dat")
STUDENTS_CSV = os.path.join(DATA_DIR, "students.csv")
COURSES_CSV = os.path.join(DATA_DIR, "courses.csv")
MARKS_CSV = os.path.join(DATA_DIR, "marks.csv")


class StorageError(Exception):
    """students.dat exists but cannot be read."""


def write_rows(path, rows):
    """Write rows (lists of values) to a text file, one row per line."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


# ---- pickle + compression -------------------------------------------

def save_data(school):
    """Before closing: pickle the data, compress it, write students.dat."""
    if not (school.students or school.courses or school.marks):
        return False                       # nothing to save
    data = {
        "students": school.students,
        "courses": school.courses,
        "marks": school.marks,
    }
    raw = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    with open(DAT_FILE, "wb") as f:
        f.write(zlib.compress(raw, 9))
    return True


def load_data(school):
    """On start: if students.dat exists, decompress + unpickle it into the school.
    Returns True if data was loaded. (Only load .dat files you created yourself:
    unpickling untrusted data is unsafe.)"""
    if not os.path.exists(DAT_FILE):
        return False
    try:
        with open(DAT_FILE, "rb") as f:
            data = pickle.loads(zlib.decompress(f.read()))
        school.students = data["students"]
        school.courses = data["courses"]
        school.marks = data["marks"]
    except (zlib.error, pickle.UnpicklingError, EOFError, KeyError,
            AttributeError, ValueError, TypeError) as e:
        raise StorageError(str(e)) from e
    return True


# ---- CSV export + pandas DataFrames ---------------------------------

def export_csv(school):
    """Export students.csv, courses.csv and marks.csv (with headers) using pandas."""
    pd.DataFrame(
        [(s.id, s.name, s.dob) for s in school.students],
        columns=["id", "name", "dob"],
    ).to_csv(STUDENTS_CSV, index=False)

    pd.DataFrame(
        [(c.id, c.name, c.credits) for c in school.courses],
        columns=["id", "name", "credits"],
    ).to_csv(COURSES_CSV, index=False)

    pd.DataFrame(
        [(cid, sid, mark)
         for cid, course_marks in school.marks.items()
         for sid, mark in course_marks.items()],
        columns=["course_id", "student_id", "mark"],
    ).to_csv(MARKS_CSV, index=False)


def load_frames():
    """Load the three CSV files into pandas DataFrames: (students, courses, marks)."""
    students = pd.read_csv(STUDENTS_CSV, dtype=str, keep_default_na=False)
    courses = pd.read_csv(COURSES_CSV, dtype=str, keep_default_na=False)
    courses["credits"] = courses["credits"].astype(int)
    marks = pd.read_csv(MARKS_CSV, dtype=str, keep_default_na=False)
    marks["mark"] = marks["mark"].astype(float)
    return students, courses, marks
