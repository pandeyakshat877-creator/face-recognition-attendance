# Attendance Management System - Akshat Pandey
# Database module using SQLite3 (replaces MongoDB)

import sqlite3
import os

DB_PATH = "attendance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT,
            major TEXT,
            starting_year INTEGER,
            total_attendance INTEGER,
            standing TEXT,
            year INTEGER,
            last_attendance_time TEXT
        )
    ''')

    students = [
        ("127", "himanshu", "Economics", 2021, 12, "B", 1, "2022-12-11 00:54:34"),
        ("Akshat", "Akshat Pandey", "Computer Science", 2023, 0, "G", 3, "2022-12-11 00:54:34"),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO students 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', students)

    conn.commit()
    conn.close()
    print("Database initialised successfully")

def get_student(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (str(student_id),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0], "name": row[1], "major": row[2],
            "starting_year": row[3], "total_attendance": row[4],
            "standing": row[5], "year": row[6], "last_attendance_time": row[7]
        }
    return None

def update_attendance(student_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE students 
        SET total_attendance = total_attendance + 1,
            last_attendance_time = datetime('now', 'localtime')
        WHERE id=?
    ''', (str(student_id),))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()