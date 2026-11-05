
import csv
import os
import zipfile

from domains import Student, Course

# Everything is stored next to this script, whatever the current directory is.
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
COURSES_FILE = os.path.join(DATA_DIR, "courses.txt")
MARKS_FILE = os.path.join(DATA_DIR, "marks.txt")
DAT_FILE = os.path.join(DATA_DIR, "students.dat")

DATA_FILES = [STUDENTS_FILE, COURSES_FILE, MARKS_FILE]
COMPRESSION = zipfile.ZIP_DEFLATED   # the selected compression method


def write_rows(path, rows):
    """Write rows (lists of values) to a text file, one row per line."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def read_rows(path):
    """Read a text file written by write_rows. Missing file -> no rows."""
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [row for row in csv.reader(f) if row]


def compress_data():
    """Compress students.txt, courses.txt and marks.txt into students.dat."""
    existing = [p for p in DATA_FILES if os.path.exists(p)]
    if not existing:
        return False                      # nothing to save
    with zipfile.ZipFile(DAT_FILE, "w", compression=COMPRESSION, compresslevel=9) as zf:
        for path in existing:
            zf.write(path, arcname=os.path.basename(path))
    return True


def decompress_data():
    """If students.dat exists, restore the text files from it."""
    if not os.path.exists(DAT_FILE):
        return False
    with zipfile.ZipFile(DAT_FILE) as zf:
        names = set(zf.namelist())
        for path in DATA_FILES:
            name = os.path.basename(path)
            if name in names:
                with open(path, "wb") as f:
                    f.write(zf.read(name))
            elif os.path.exists(path):
                os.remove(path)           # stale file that is not in the archive
    return True


def load_data(school):
    """Decompress students.dat (if it exists) and load it into the school.
    Returns True if data was loaded."""
    if not decompress_data():
        return False
    school.students = [Student(r[0], r[1], r[2]) for r in read_rows(STUDENTS_FILE)]
    school.courses = [Course(r[0], r[1], int(r[2])) for r in read_rows(COURSES_FILE)]
    for course_id, student_id, mark in read_rows(MARKS_FILE):
        school.set_mark(course_id, student_id, float(mark))
    return True