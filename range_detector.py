# import the necessary packages

import numpy as np
import imutils
import cv2

minHVal = 0
minSVal = 0
minVVal = 0
maxHVal = 255
maxSVal = 255
maxVVal = 255

def callback(value):
    pass

cv2.namedWindow("Trackbars", 0)

cv2.createTrackbar('H (min)', "Trackbars", minHVal, 255, callback)
cv2.createTrackbar('S (min)', "Trackbars", minSVal, 255, callback)
cv2.createTrackbar('V (min)', "Trackbars", minVVal, 255, callback)

cv2.createTrackbar('H (max)', "Trackbars", maxHVal, 255, callback)
cv2.createTrackbar('S (max)', "Trackbars", maxSVal, 255, callback)
cv2.createTrackbar('V (max)', "Trackbars", maxVVal, 255, callback)

camera = cv2.VideoCapture('http://10.4.70.11/mjpg/video.mjpg')

while True:
    minHVal = cv2.getTrackbarPos('H (min)', "Trackbars")
    minSVal = cv2.getTrackbarPos('S (min)', "Trackbars")
    minVVal = cv2.getTrackbarPos('V (min)', "Trackbars")

    maxHVal = cv2.getTrackbarPos('H (max)', "Trackbars")
    maxSVal = cv2.getTrackbarPos('S (max)', "Trackbars")
    maxVVal = cv2.getTrackbarPos('V (max)', "Trackbars")

    (grabbed, frame) = camera.read()

    #resize the frame
    frame = imutils.resize(frame, width=600)
    
    #convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #construct a mask for the color, then perform
    #a series of dilations and erosions to remove any small
    #blobs left in the mask

    mask = cv2.inRange(hsv, (minHVal, minSVal, minVVal), (maxHVal, maxSVal, maxVVal))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

# cleanup the camera and close open windows
camera.release()
cv2.destroyAllWindows()
    
