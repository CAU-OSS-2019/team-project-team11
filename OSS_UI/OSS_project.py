import sys
from os import path
import os
import threading
import cv2
import numpy as np
import face_recognition
import dlib
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import datetime
# The deisred output width and height
OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600
MOSAIC_RATE = 10
BASE_SIZE_WIDTH = 320
BASE_SIZE_HEIGHT = 240

known_face_encodings = []
known_face_names = []
faces_locations = []
face_encodings = []
face_names = {}

# Load sample pictures and learn how to recognize it.
dirname = 'knowns'
files = os.listdir(dirname)
for filename in files:
    name, ext = os.path.splitext(filename)
    if ext == '.jpg':
        known_face_names.append(name)
        pathname = os.path.join(dirname, filename)
        img = face_recognition.load_image_file(pathname)
        face_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(face_encoding)
rectangleColor = (0, 165, 255)

# variables holding the current frame number and the current faceid
frameCounter = 0
currentFaceID = 0

# Variables holding the correlation trackers and the name per faceid
faceTrackers = {}
faceNames = {}

class Assign(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.take_picture = QtWidgets.QPushButton("take picture")
        layout.addWidget(self.take_picture)
        self.take_picture.clicked.connect(self.btn1)
        self.setLayout(layout)

    def btn1(self):
        dlg = Take_pic()
        dlg.exec_()

class Take_pic(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()
        self.image
    def save_clicked(self):
        QMessageBox.about(self, "message", "saved")
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        cv2.imwrite('Knowns/data'+suffix+'.jpg' ,self.image)
    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(640, 500)

        layout=QGridLayout()


        #create a label
        label = QLabel(self)
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                         QtGui.QImage.Format_RGB888)
        convertToQtFormat = QtGui.QPixmap.fromImage(convertToQtFormat)
        pixmap = QPixmap(convertToQtFormat)
        rgbImage=cv2.cvtColor(rgbImage, cv2.COLOR_RGB2BGR)
        cv2.resize(rgbImage, dsize =(640,480))
        resizeImage = pixmap.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
        QApplication.processEvents()
        label.setPixmap(resizeImage)
        self.image=rgbImage
        self.save_button = QPushButton("save")
        self.save_button.clicked.connect(self.save_clicked)
        layout.addWidget(label)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

def doRecognizePerson(faceNames, fid):
    time.sleep(2)
    faceNames[fid] = "Person " + str(fid)


class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)

        self.timer = QtCore.QBasicTimer()

    def start_recording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)


class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, haar_cascade_filepath, parent=None):
        super().__init__(parent)
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)

    def detect_faces(self, image: np.ndarray):
        # haarclassifiers work better in black and white
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image,
                                                 scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=self._min_size)

        return faces

    def image_data_slot(self, image_data):
        baseImage = cv2.resize(image_data, (BASE_SIZE_WIDTH, BASE_SIZE_HEIGHT))
        # Result image is the image we will show the user, which is a
        # combination of the original image from the webcam and the
        # overlayed rectangle for the largest face
        resultImage = baseImage.copy()
        mosaicImage = baseImage.copy()

        # STEPS:
        # * Update all trackers and remove the ones that are not
        #   relevant anymore
        # * Every 10 frames:
        #       + Use face detection on the current frame and look
        #         for faces.
        #       + For each found face, check if centerpoint is within
        #         existing tracked box. If so, nothing to do
        #       + If centerpoint is NOT in existing tracked box, then
        #         we add a new tracker with a new face-id

        # Increase the framecounter
        global frameCounter
        frameCounter += 1

        # Update all the trackers and remove the ones for which the update
        # indicated the quality was not good enough
        fidsToDelete = []
        for fid in faceTrackers.keys():
            trackingQuality = faceTrackers[fid].update(baseImage)

            # If the tracking quality is good enough, we must delete
            # this tracker
            if trackingQuality < 5:
                fidsToDelete.append(fid)

        for fid in fidsToDelete:
            print("Removing fid " + str(fid) + " from list of trackers")
            faceTrackers.pop(fid, None)
            face_names.pop(fid, None)

            # Every 10 frames, we will have to determine which faces
            # are present in the frame
        if (frameCounter % 5) == 0:

            # For the face detection, we need to make use of a gray
            # colored image so we will convert the baseImage to a
            # gray-based image
            # gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)
            # Now use the haar cascade detector to find all faces
            # in the image
            # faces = faceCascade.detectMultiScale(gray, 1.3, 5)

            faces = face_recognition.face_locations(baseImage)
            # face_encodings = face_recognition.face_encodings(baseImage, faces)

            # print(face_encodings)

            # Loop over all faces and check if the area for this
            # face is the largest so far
            # We need to convert it to int here because of the
            # requirement of the dlib tracker. If we omit the cast to
            # int here, you will get cast errors since the detector
            # returns numpy.int32 and the tracker requires an int
            for (top, right, bottom, left) in faces:
                x = int(left)
                y = int(top)
                w = int(right - left)
                h = int(bottom - top)

                # calculate the centerpoint
                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h

                # Variable holding information which faceid we
                # matched with
                matchedFid = None

                # Now loop over all the trackers and check if the
                # centerpoint of the face is within the box of a
                # tracker
                for fid in faceTrackers.keys():
                    tracked_position = faceTrackers[fid].get_position()

                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())

                    # calculate the centerpoint
                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h

                    # check if the centerpoint of the face is within the
                    # rectangleof a tracker region. Also, the centerpoint
                    # of the tracker region must be within the region
                    # detected as a face. If both of these conditions hold
                    # we have a match
                    if ((t_x <= x_bar <= (t_x + t_w)) and
                            (t_y <= y_bar <= (t_y + t_h)) and
                            (x <= t_x_bar <= (x + w)) and
                            (y <= t_y_bar <= (y + h))):
                        matchedFid = fid

                    # If no matched fid, then we have to create a new tracker
                global currentFaceID
                if matchedFid is None:

                    print("Creating new tracker " + str(currentFaceID))

                    # Create and store the tracker
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(baseImage,
                                        dlib.rectangle(x - 10,
                                                       y - 20,
                                                       x + w + 10,
                                                       y + h + 20))

                    faceTrackers[currentFaceID] = tracker
                    face_encodings = face_recognition.face_encodings(baseImage, [(top, right, bottom, left)])

                    distances = face_recognition.face_distance(known_face_encodings, face_encodings[0])
                    min_value = min(distances)

                    # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                    # 0.6 is typical best performance.
                    name = "Unknown"
                    if min_value < 0.4:
                        index = np.argmin(distances)
                        name = known_face_names[index]

                    face_names[currentFaceID] = name

                    print(face_names)

                    # Start a new thread that is used to simulate
                    # face recognition. This is not yet implemented in this
                    # version :)
                    t = threading.Thread(target=doRecognizePerson,
                                         args=(faceNames, currentFaceID))
                    t.start()

                    # Increase the currentFaceID counter
                    currentFaceID += 1

            # Now loop over all the trackers we have and draw the rectangle
            # around the detected faces. If we 'know' the name for this person
            # (i.e. the recognition thread is finished), we print the name
            # of the person, otherwise the message indicating we are detecting
            # the name of the person
        for fid in faceTrackers.keys():
            tracked_position = faceTrackers[fid].get_position()

            t_x = int(tracked_position.left())
            t_y = int(tracked_position.top())
            t_w = int(tracked_position.width())
            t_h = int(tracked_position.height())

            cv2.rectangle(resultImage, (t_x, t_y),
                          (t_x + t_w, t_y + t_h),
                          rectangleColor, 2)

            m_x = int(t_x > 0 and t_x or 0)
            m_y = int(t_y > 0 and t_y or 0)
            m_w = int(t_x + t_w < BASE_SIZE_WIDTH and t_w or BASE_SIZE_WIDTH - t_x)
            m_h = int(t_y + t_h < BASE_SIZE_HEIGHT and t_h or BASE_SIZE_HEIGHT - t_y)

            if (face_names[fid] == 'Unknown'):
                face_img = mosaicImage[m_y:m_y + m_h, m_x:m_x + m_w]
                face_img = cv2.resize(face_img, (m_w // MOSAIC_RATE, m_h // MOSAIC_RATE))
                face_img = cv2.resize(face_img, (m_w, m_h), interpolation=cv2.INTER_AREA)
                mosaicImage[m_y:m_y + m_h, m_x:m_x + m_w] = face_img

            if fid in faceNames.keys():
                cv2.putText(resultImage, face_names[fid],
                            (int(t_x + t_w / 2), int(t_y)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)
            else:
                cv2.putText(resultImage, "Detecting...",
                            (int(t_x + t_w / 2), int(t_y)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)

            # Since we want to show something larger on the screen than the
            # original BASE_SIZE_WIDTHxBASE_SIZE_HEIGHT, we resize the image again
            #
            # Note that it would also be possible to keep the large version
            # of the baseimage and make the result image a copy of this large
            # base image and use the scaling factor to draw the rectangle
            # at the right coordinates.
        largeResult = cv2.resize(resultImage,
                                 (OUTPUT_SIZE_WIDTH, OUTPUT_SIZE_HEIGHT))
        mosaicResult = cv2.resize(mosaicImage,
                                  (OUTPUT_SIZE_WIDTH, OUTPUT_SIZE_HEIGHT))

        self.image = self.get_qimage(mosaicResult)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()


class MainWidget(QtWidgets.QWidget):
    def __init__(self, haarcascade_filepath, parent=None):
        super().__init__(parent)
        fp = haarcascade_filepath
        self.face_detection_widget = FaceDetectionWidget(fp)

        # TODO: set video port
        self.record_video = RecordVideo()

        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()
        self.assign_button = QtWidgets.QPushButton("assign face")
        layout.addWidget(self.assign_button)
        self.assign_button.clicked.connect(self.btn1_clicked)

        layout.addWidget(self.face_detection_widget)
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)
        self.btn = QPushButton("NSFW")
        layout.addWidget(self.btn)
        self.le = QLabel("")

        layout.addWidget(self.le)
        self.btn.clicked.connect(self.getfile)
        self.run_button.clicked.connect(self.record_video.start_recording)
        self.setLayout(layout)

    def btn1_clicked(self):
        # QMessageBox.about(self, "message", "clicked")
        dlg = Assign()
        dlg.exec_()

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.gif)")
        self.le.setPixmap(QPixmap(fname[0]))


def main(haar_cascade_filepath):
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget(haar_cascade_filepath)
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    script_dir = path.dirname(path.realpath(__file__))
    cascade_filepath = path.join(script_dir,
                                 'data',
                                 'haarcascade_frontalface_default.xml')

    cascade_filepath = path.abspath(cascade_filepath)
    main(cascade_filepath)