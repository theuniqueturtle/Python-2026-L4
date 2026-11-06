import copy
import csv
import os
import pickle
import queue
import threading
import time
import zlib

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
COURSES_FILE = os.path.join(DATA_DIR, "courses.txt")
MARKS_FILE = os.path.join(DATA_DIR, "marks.txt")
DAT_FILE = os.path.join(DATA_DIR, "students.dat")

_STOP = object()


class StorageError(Exception):
    pass


def write_rows(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def load_data(school):
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


class BackgroundSaver:

    def __init__(self):
        self._queue = queue.Queue()
        self._lock = threading.Lock()
        self._pending = 0
        self._last_saved = None
        self._error = None
        self._thread = threading.Thread(
            target=self._worker, name="pickle-saver", daemon=True)
        self._thread.start()

    def save(self, school):
        if not (school.students or school.courses or school.marks):
            return
        snapshot = copy.deepcopy({
            "students": school.students,
            "courses": school.courses,
            "marks": school.marks,
        })
        with self._lock:
            self._pending += 1
        self._queue.put(snapshot)

    def close(self):
        self._queue.put(_STOP)
        self._thread.join()

    def status(self):
        with self._lock:
            if self._error:
                return f"Autosave ERROR: {self._error}"
            if self._pending:
                return "Autosave: saving in the background..."
            if self._last_saved:
                return f"Autosave: saved at {self._last_saved}"
        return ""

    def _worker(self):
        stop = False
        while not stop:
            item = self._queue.get()
            newest, skipped = None, 0
            while True:
                if item is _STOP:
                    stop = True
                else:
                    if newest is not None:
                        skipped += 1
                    newest = item
                try:
                    item = self._queue.get_nowait()
                except queue.Empty:
                    break
            if newest is not None:
                self._write(newest, skipped)

    def _write(self, snapshot, skipped):
        try:
            raw = pickle.dumps(snapshot, protocol=pickle.HIGHEST_PROTOCOL)
            packed = zlib.compress(raw, 9)
            tmp = DAT_FILE + ".tmp"
            with open(tmp, "wb") as f:
                f.write(packed)
            os.replace(tmp, DAT_FILE)
            with self._lock:
                self._last_saved = time.strftime("%H:%M:%S")
                self._error = None
        except Exception as e:
            with self._lock:
                self._error = str(e)
        finally:
            with self._lock:
                self._pending -= 1 + skipped


_saver = None


def start_saver():
    global _saver
    if _saver is None:
        _saver = BackgroundSaver()


def save_async(school):
    if _saver is not None:
        _saver.save(school)


def stop_saver():
    global _saver
    if _saver is not None:
        _saver.close()
        _saver = None


def save_status():
    return _saver.status() if _saver is not None else ""
