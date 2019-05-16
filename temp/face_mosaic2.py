# import the necessary packages
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy as np
import os.path as osp
import serial
import math
from hpd import HPD


default_servoAngle = 90
default_xAngle = 60
delimiter = "/"
RESIZE_RATIO = 1.4 #프레임 작게하기
SKIP_FRAMES = 3 #프레임 건너뛰기


def main(args):
    filename = args["input_file"]

    if filename is None:
        isVideo = False

        # created a *threaded *video stream, allow the camera sensor to warmup,
        # and start the FPS counter
        print("[INFO] sampling THREADED frames from `picamera` module...")
        vs = PiVideoStream().start()
        time.sleep(2.0)
        fps = FPS().start()

    else:
        isVideo = True
        cap = cv2.VideoCapture(filename)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        name, ext = osp.splitext(filename)
        out = cv2.VideoWriter(args["output_file"], fourcc, fps, (width, height))

    # Initialize head pose detection
    hpd = HPD(args["landmark_type"], args["landmark_predictor"])

    xy_arduino = serial.Serial('/dev/ttyUSB0', 9600)
    servo_arduino = serial.Serial('/dev/ttyACM1',9600)
    z_arduino = serial.Serial('/dev/ttyACM0', 9600)

    # servo motor default angle
    servo_angle = default_servoAngle
    tempAngle = str(servo_angle)
    tempAngle = tempAngle.encode('utf-8')
    #servo_arduino.write(tempAngle)

    #count = 0

    cv2.namedWindow('frame2', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame2', 320, 240)


    while(vs.stopped == False):
        # Capture frame-by-frame
        print('\rframe: %d' % fps._numFrames, end='')
        frame = vs.read()

        h, w, c = frame.shape
        new_h = (int)(h / RESIZE_RATIO)
        new_w = (int)(w / RESIZE_RATIO)
        frame_small = cv2.resize(frame, (new_w, new_h))
        frame_small2 = cv2.flip(frame_small, 1) # 좌우반전: 카메라 거울상
        frame_small3 = cv2.flip(frame_small, 0) # 상하반전


        if isVideo:

            if frame is None:
                break
            else:
                out.write(frame)

        else:

            if (fps._numFrames % SKIP_FRAMES == 0):
                frameOut, angles, tvec = hpd.processImage(frame_small3)
                if tvec==None:
                    print('\rframe2: %d' % fps._numFrames, end='')
                    print(" There is no face detected\n")

                    fps.update()
                    #count += 1
                    continue

                else:
                    tx, ty, tz = tvec[:, 0]
                    rx, ry, rz = angles



                    th = math.radians(servo_angle)
                    # xy angle
                    # tz: : x angle, tx: y angle
                    temp_z = int(tz) + default_xAngle   #temp_z: x angle

                    x_angle = math.sin(th)*temp_z + math.cos(th)*tx
                    y_angle = math.cos(th)*temp_z + math.sin(th)*tx

                    temp_y = int(ty)
                    z_angle = str(temp_y)

                    z_angle = z_angle.encode('utf-8')
                    ry = int(ry)

                    if (abs(ry) <=15):
                        ry=0

                    th1 = math.radians(ry)
                    y_angle += int(math.tan(th1)* tz)

                    xy_angle = str(int(x_angle)) + delimiter + str(int(y_angle))
                    xy_angle = xy_angle.encode('utf-8')
                    print("\n\n\nstr_tx: ", xy_angle)
                    servo_angle = servo_angle + ry
                    tempAngle = str(servo_angle)
                    tempAngle = tempAngle.encode('utf-8')

                    print("\ntx: ",tx, "\nty: ", ty,"\ntz: ", tz)


                    print("\n\n\nry: ", ry)

                    # write XY angle
                    xy_arduino.write(xy_angle)

                    # write Z angle
                    z_arduino.write(z_angle)
                    servo_arduino.write(tempAngle)
                    time.sleep(3)

            else:
                pass


            # Display the resulting frame

            cv2.imshow('frame2',frameOut)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

##        count += 1
        fps.update()

    # When everything done, release the capture
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    vs.stop()
    if isVideo: out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', metavar='FILE', dest='input_file', default=None, help='Input video. If not given, web camera will be used.')
    parser.add_argument('-o', metavar='FILE', dest='output_file', default=None, help='Output video.')
    parser.add_argument('-lt', metavar='N', dest='landmark_type', type=int, default=1, help='Landmark type.')
    parser.add_argument('-lp', metavar='FILE', dest='landmark_predictor',
                        default='model/shape_predictor_68_face_landmarks.dat', help="Landmark predictor data file.")
    parser.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
    parser.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
    args = vars(parser.parse_args())
    main(args)
