import cv2
import numpy as np
import dlib

# Load the classifier and create a cascade object for face detection
face_cascade = cv2.CascadeClassifier('xmls/haarcascade_frontalface_alt2.xml')

cv2.moveWindow("base-image",0,100)
cv2.moveWindow("result-image",400,100)

cap = cv2.VideoCapture(0)

pre_detected_faces = []
while True:
    ret, frame = cap.read()
    base = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_faces = face_cascade.detectMultiScale(gray)

    # Drawing face area line
    # for (column, row, width, height) in detected_faces :
    #     cv2.rectangle(
    #         frame,
    #         (column, row),
    #         (column + height, row + height),
    #         (0, 255, 0),
    #         2
    #     )

    if len(detected_faces) == 0:
        detected_faces = pre_detected_faces

    # Mosaic detected face
    mosaic_rate = 20
    for (column, row, width, height) in detected_faces:
        print(row, column, height, width)
        face_img = frame[row:row + height, column:column + width]
        face_img = cv2.resize(face_img, (width//mosaic_rate, height//mosaic_rate))
        face_img = cv2.resize(face_img, (width, height), interpolation=cv2.INTER_AREA)
        frame[row:row + height, column:column + height] = face_img

    # pre_detected_faces = detected_faces
    cv2.imshow('frame', frame)
    cv2.imshow('base', base)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break

cap.release()
cv2.destroyAllWindows()