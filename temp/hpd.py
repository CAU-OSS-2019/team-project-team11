
import os
import os.path as osp
import argparse
import cv2
import numpy as np
import dlib
import time
from timer import Timer
#from draw import Draw


t = Timer()

# HeadPoseDetection
class HPD():

    # 3D facial model coordinates
    landmarks_3d_list = [
        np.array([
            [ 0.000,  0.000,   0.000],    # Nose tip
            [ 0.000, -8.250,  -1.625],    # Chin
            [-5.625,  4.250,  -3.375],    # Left eye left corner
            [ 5.625,  4.250,  -3.375],    # Right eye right corner
            [-3.750, -3.750,  -3.125],    # Left Mouth corner
            [ 3.750, -3.750,  -3.125]     # Right mouth corner
        ], dtype=np.double),
        np.array([
            [ 0.000000,  0.000000,  6.763430],   # 52 nose bottom edge
            [ 6.825897,  6.760612,  4.402142],   # 33 left brow left corner
            [ 1.330353,  7.122144,  6.903745],   # 29 left brow right corner
            [-1.330353,  7.122144,  6.903745],   # 34 right brow left corner
            [-6.825897,  6.760612,  4.402142],   # 38 right brow right corner
            [ 5.311432,  5.485328,  3.987654],   # 13 left eye left corner
            [ 1.789930,  5.393625,  4.413414],   # 17 left eye right corner
            [-1.789930,  5.393625,  4.413414],   # 25 right eye left corner
            [-5.311432,  5.485328,  3.987654],   # 21 right eye right corner
            [ 2.005628,  1.409845,  6.165652],   # 55 nose left corner
            [-2.005628,  1.409845,  6.165652],   # 49 nose right corner
            [ 2.774015, -2.080775,  5.048531],   # 43 mouth left corner
            [-2.774015, -2.080775,  5.048531],   # 39 mouth right corner
            [ 0.000000, -3.116408,  6.097667],   # 45 mouth central bottom corner
            [ 0.000000, -7.415691,  4.070434]    # 6 chin corner
        ], dtype=np.double),
        np.array([
            [ 0.000000,  0.000000,  6.763430],   # 52 nose bottom edge
            [ 5.311432,  5.485328,  3.987654],   # 13 left eye left corner
            [ 1.789930,  5.393625,  4.413414],   # 17 left eye right corner
            [-1.789930,  5.393625,  4.413414],   # 25 right eye left corner
            [-5.311432,  5.485328,  3.987654]    # 21 right eye right corner
        ], dtype=np.double)
    ]

    # 2d facial landmark list
    lm_2d_index_list = [
        [30, 8, 36, 45, 48, 54],
        [33, 17, 21, 22, 26, 36, 39, 42, 45, 31, 35, 48, 54, 57, 8], # 14 points
        [33, 36, 39, 42, 45] # 5 points
    ]

    def __init__(self, lm_type=1, predictor="model/shape_predictor_68_face_landmarks.dat", verbose=True):
        self.bbox_detector = dlib.get_frontal_face_detector()
##        self.bbox_detector = cv2.CascadeClassifier()
        self.landmark_predictor = dlib.shape_predictor(predictor)

        self.lm_2d_index = self.lm_2d_index_list[lm_type]
        self.landmarks_3d = self.landmarks_3d_list[lm_type]

        self.v = verbose


    def class2np(self, landmarks):
        coords = []
        for i in self.lm_2d_index:
            coords += [[landmarks.part(i).x, landmarks.part(i).y]]
        return np.array(coords).astype(np.int)


    def getLandmark(self, im):
        # Detect bounding boxes of faces
        t.tic()
        if im is not None:
            rects = self.bbox_detector(im, 1)
        else:
            rects = []
        if self.v: print(', bb: %.2f' % t.toc(), end='ms')

        if len(rects) > 0:
            # Detect landmark of first face
            t.tic()
            landmarks_2d = self.landmark_predictor(im, rects[0])

            # Choose specific landmarks corresponding to 3D facial model
            landmarks_2d = self.class2np(landmarks_2d)
            if self.v: print(', lm: %.2f' % t.toc(), end='ms')

            return landmarks_2d.astype(np.double), rects[0]

        else:
            return None, None


    def getHeadpose(self, im, landmarks_2d, verbose=False):
        h, w, c = im.shape
        f = w # column size = x axis length (focal length)
        u0, v0 = w / 2, h / 2 # center of image plane
        camera_matrix = np.array(
            [[f, 0, u0],
             [0, f, v0],
             [0, 0, 1]], dtype = np.double
         )

        # Assuming no lens distortion
        dist_coeffs = np.zeros((4,1))

        # Find rotation, translation
        (success, rotation_vector, translation_vector) = cv2.solvePnP(self.landmarks_3d, landmarks_2d, camera_matrix, dist_coeffs)

        if (verbose==False):
            print("Camera Matrix:\n {0}".format(camera_matrix))
            print("Distortion Coefficients:\n {0}".format(dist_coeffs))
            print("Rotation Vector:\n {0}".format(rotation_vector))
            print("Translation Vector:\n {0}".format(translation_vector))

        return rotation_vector, translation_vector, camera_matrix, dist_coeffs


    # rotation vector to euler angles
    def getAngles(self, rvec, tvec):
        rmat = cv2.Rodrigues(rvec)[0]
        P = np.hstack((rmat, tvec)) # projection matrix [R | t]
        degrees = -cv2.decomposeProjectionMatrix(P)[6]
        print("\ndegrees:\n {0}".format(degrees))
        rx, ry, rz = degrees[:, 0]
        return [rx, ry, rz]


    # return image and angles
    #def processImage(self, im, draw=True):
    def processImage(self, im):
        # landmark Detection
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        landmarks_2d, bbox = self.getLandmark(im_gray)

        # if no face deteced, return original image
        if landmarks_2d is None:
            return im, None, None

        # Headpose Detection
        t.tic()
        rvec, tvec, cm, dc = self.getHeadpose(im, landmarks_2d)
##        print("\ntvec:\n {0}".format(tvec))
##        tx, ty, tz = tvec[:, 0]
##        print('getTvec tx: %s' % tx)
##        print('getTvec ty: %s' % ty)
##        print('getTvec tz: %s' % tz)
        if self.v: print(', hp: %.2f' % t.toc(), end='ms')

        t.tic()
        angles = self.getAngles(rvec, tvec)
        rx, ry, rz = angles


        if self.v: print(', ga: %.2f' % t.toc(), end='ms')

        # if draw:
        #     t.tic()
        #     draw = Draw(im, angles, bbox, landmarks_2d, rvec, tvec, cm, dc, b=10.0)
        #     im = draw.drawAll()
        #     if self.v: print(', draw: %.2f' % t.toc(), end='ms' + ' ' * 10)

        return im, angles, tvec


def main(args):
    in_dir = args["input_dir"]
    out_dir = args["output_dir"]

    # Initialize head pose detection
    hpd = HPD(args["landmark_type"], args["landmark_predictor"])

    arduino = serial.Serial('/dev/ttyUSB0', 9600)

    for filename in os.listdir(in_dir):
        name, ext = osp.splitext(filename)
        if ext in ['.jpg', '.png', '.gif', '.jpeg']:
            print("> image:", filename, end='')
            image = cv2.imread(in_dir + filename)
            res, angles, tvec = hpd.processImage(image)
            tx, ty, tz = tvec[:, 0]
            rx, ry, rz = angles

            cv2.imwrite(out_dir + name + '_out.png', res)
        else:
            print("> skip:", filename, end='')
        print('')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', metavar='DIR', dest='input_dir', default='images/')
    parser.add_argument('-o', metavar='DIR', dest='output_dir', default='res/')
    parser.add_argument('-lt', metavar='N', dest='landmark_type', type=int, default=1, help='Landmark type.')
    parser.add_argument('-lp', metavar='FILE', dest='landmark_predictor',
                        default='model/shape_predictor_68_face_landmarks.dat', help="Landmark predictor data file.")
    args = vars(parser.parse_args())

    if not osp.exists(args["output_dir"]): os.mkdir(args["output_dir"])
    if args["output_dir"][-1] != '/': args["output_dir"] += '/'
    if args["input_dir"][-1] != '/': args["input_dir"] += '/'
    main(args)
