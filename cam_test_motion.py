from time import sleep
import socket
import time
from datetime import datetime as dt
import cv2
import pickle
import struct
import cv2
from gpiozero import MotionSensor

cam = cv2.VideoCapture(0)
pir = MotionSensor(4)

while True:
    ret, frame = cam.read()
    ret, image = cam.read()
    cv2.imshow('Video Test', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        break
    if pir.wait_for_motion():
        cv2.imwrite('/home/pi/' + dt.now().strftime("%m_%d_%Y-%I:%M:%S_%p") + '.png', image)
        print('Movement Detected')
    elif pir.wait_for_no_motion():
        continue
    else:
        pir.wait_for_no_motion()
        