# Attendance Management System - Akshat Pandey
# Built as part of B.Tech CSE project, SKIT Jaipur

import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
from datetime import datetime
from connectDatabase import init_db, get_student, update_attendance

# Initialise database
init_db()

# Initialise the camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Load mode images
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Load face encodings
print("Loading encoding file...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
known_face_encodings, studentIds = encodeListKnownWithIds
print(f"Encoding file loaded. Student IDs: {studentIds}")

display_mode = 0
frame_counter = 0
id = -1
imgStudent = []
studentInfo = None

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[display_mode]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(known_face_encodings, encodeFace)
            faceDis = face_recognition.face_distance(known_face_encodings, encodeFace)

            matchIndex = np.argmin(faceDis)
            print(f"Match index: {matchIndex}")

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                print(f"Student ID detected: {id}")
                if frame_counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    frame_counter = 1
                    display_mode = 1

        if frame_counter != 0:
            if frame_counter == 1:
                studentInfo = get_student(id)
                print(f"Student info retrieved: {studentInfo}")

                if studentInfo:
                    datetimeObject = datetime.strptime(
                        studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S"
                    )
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    if secondsElapsed > 30:
                        update_attendance(id)
                    else:
                        display_mode = 3
                        frame_counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[display_mode]
                else:
                    cvzone.putTextRect(imgBackground, "ID Not Found", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(2000)
                    frame_counter = 0
                    display_mode = 0

            if display_mode != 3:
                if 10 < frame_counter < 20:
                    display_mode = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[display_mode]

                if frame_counter <= 10:
                    if studentInfo:
                        cv2.putText(imgBackground, str(studentInfo['total_attendance']),
                                    (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['major']),
                                    (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(id),
                                    (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['standing']),
                                    (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['year']),
                                    (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']),
                                    (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        (w, h), _ = cv2.getTextSize(
                            studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1
                        )
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']),
                                    (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                frame_counter += 1

                if frame_counter >= 20:
                    frame_counter = 0
                    display_mode = 0
                    studentInfo = None
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[display_mode]
    else:
        display_mode = 0
        frame_counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)