# Face Recognition Attendance System

I built this project as part of my B.Tech CSE coursework at SKIT Jaipur. It is a real-time face recognition based attendance system that automatically detects and recognises students using a webcam and marks their attendance in a local database.

## What It Does
- Detects faces in real-time using a webcam
- Recognises registered students automatically
- Marks attendance with timestamp in a SQLite3 database
- Displays student information on screen when recognised
- Prevents duplicate attendance within 30 seconds

## Tech Stack
- Python 3.10
- OpenCV — video capture and image processing
- face_recognition — face detection and encoding
- dlib — underlying face recognition model
- cvzone — UI overlays
- SQLite3 — local database (no external server required)

## How It Works
1. Student photos are stored in the Images folder named by student ID
2. Encoding.py converts photos into face encodings and saves them
3. connectDatabase.py initialises the SQLite3 database with student records
4. main.py runs the live webcam feed, matches faces against encodings, and updates attendance

## Challenges I Faced
- Replacing MongoDB with SQLite3 required rewriting the entire database layer
- dlib and face_recognition only work with Python 3.10, not newer versions
- Managing frame counter logic to avoid duplicate attendance entries

## Setup Instructions
1. Install Python 3.10 from python.org
2. Install dependencies:
3. Add student photos to the Images folder named as StudentID.jpeg
4. Run in this order:
py -3.10 Encoding.py
py -3.10 connectDatabase.py
py -3.10 main.py
## Project By
Akshat Pandey
B.Tech CSE, SKIT Jaipur
