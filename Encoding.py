# Attendance Management System - Akshat Pandey
# Face encoding generator

import cv2
import face_recognition
import pickle
import os

folderPath = 'Images'
pathList = os.listdir(folderPath)
print(f"Images found: {pathList}")

imgList = []
studentIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

print(f"Student IDs detected: {studentIds}")

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding started...")
known_face_encodings = findEncodings(imgList)
encodeListKnownWithIds = [known_face_encodings, studentIds]
print("Encoding complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")