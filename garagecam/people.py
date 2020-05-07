from imutils.object_detection import non_max_suppression
import numpy as np
import imutils
import cv2
import time
import argparse
import time
from client import alert, build
import random
import socket
import requests

'''
Usage:
python peopleCounter.py -i PATH_TO_IMAGE  # Reads and detect people in a single local stored image
python peopleCounter.py -c  # Attempts to detect people using webcam
IMPORTANT: This example is given AS IT IS without any warranty
Made by: Jose Garcia
'''

# Opencv pre-trained SVM with HOG people features
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

LAST_TIME = 0


def detector(image):
    '''
    @image is a numpy array
    '''

    clone = image.copy()

    (rects, weights) = HOGCV.detectMultiScale(image, winStride=(4, 4),
                                              padding=(8, 8), scale=1.05)

    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Applies non-max suppression from imutils package to kick-off overlapped
    # boxes
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    result = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    return result


def args_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", default=None,
                    help="path to image test file directory")
    ap.add_argument("--camera", action='store_true', default=False,
                    help="Set as true if you wish to use the camera")
    ap.add_argument("--host-name", "-hn", required=False, type=str)
    ap.add_argument("--port", "-p", required=False, type=int)
    ap.add_argument("--host-ip", "-hip", required=False, type=str)
    args = vars(ap.parse_args())

    return args


def local_detect(image_path):
    result = []
    image = cv2.imread(image_path)
    image = imutils.resize(image, width=min(400, image.shape[1]))
    clone = image.copy()
    if len(image) <= 0:
        print("[ERROR] could not read your local image")
        return result
    print("[INFO] Detecting people")
    result = detector(image)

    # shows the result
    for (xA, yA, xB, yB) in result:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

    cv2.imshow("result", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("result.png", np.hstack((clone, image)))
    return result, image


def cameraDetect(args):
    global LAST_TIME
    cap = cv2.VideoCapture(0)
    ret = True
    i_cnt = 0

    while ret:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=min(400, frame.shape[1]))
        result = detector(frame.copy())

        # shows the result

        for (xA, yA, xB, yB) in result:
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

        cv2.putText(frame, time.ctime(), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        ct = time.time()
        if ct - LAST_TIME > random.randint(20, 120) and len(result) > 0:
            LAST_TIME = ct
            alert(host_ip=args['host_ip'], hostname=args['host_name'], port=args['port'])

        cv2.imshow('frame', frame)
        fn = './imgs/' + str(i_cnt) + '.jpg'
        cv2.imwrite(fn, frame)
        print('[INFO] Image saved to {}'.format(fn))
        send_img(args, fn)
        if i_cnt > 10:
            i_cnt = 0
        else:
            i_cnt += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def send_img(args, path):
    url = 'http://' + args['host_ip'] + ':' + str(args['port']) + '/security/camera/upload'
    files = {'file': open(path, 'rb')}
    try:
        requests.post(url, files=files)
    except ConnectionError as e:
        print('[ERROR] Unable to connect to server')


def detect_people(args):
    print("[INFO] detectPeople(args)")
    image_path = args["image"]
    camera = args['camera']

    # Routine to read local image
    if image_path is not None and not camera:
        print("[INFO] Image path provided, attempting to read image")
        (result, image) = local_detect(image_path)

    # Routine to read images from webcam
    if camera:
        print("[INFO] reading camera images")
        cameraDetect(args)


def main():
    args = args_parser()
    print("[INFO] starting with {}".format(args))
    detect_people(args)


if __name__ == '__main__':
    main()
