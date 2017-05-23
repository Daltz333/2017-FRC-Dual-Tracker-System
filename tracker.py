import numpy as np
import cv2
import logging
import constants
from networktables import NetworkTables
from imutils.video import WebcamVideoStream

#NOTES:
#TEST IF MAIN ROBOT.PY CAN SET THE NETWORKTABLE INFORMATION
#IF SO STATEMACHINE IS A SUCCESS
logging.basicConfig(level=logging.DEBUG)

#grab frames using multithreading
#and initialize the camera
vs0 = WebcamVideoStream(src=constants.PegStream).start()
vs1 = WebcamVideoStream(src=constants.TowerStream).start()

NetworkTables.setClientMode()
NetworkTables.initialize(server=constants.ServerIP)
Table = NetworkTables.getTable(constants.MainTable)
    
def trackPeg():
    while (True):

        if(Table.getNumber("PiState", 0) != 0):
            break
        else:
            pass

        #grab current frame from multithreaded process
        frame0 = vs0.read()
        
        #convert to HSV
        hsv = cv2.cvtColor(frame0, cv2.COLOR_BGR2HSV)

        #create the range of colour min/max
        green_range = cv2.inRange(hsv, constants.peg_green_lower, constants.peg_green_upper)

        #create blank area for sort
        areaArray = []
        try:
            #grab all contours based on colour range
            b, contours, _ = cv2.findContours(green_range, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #order contours into an array by area
            for i, c in enumerate(contours):
                area = cv2.contourArea(c)
                areaArray.append(area)
            
            #sort the array by greatest to smallest
            sorteddata = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)
            
            #find the nth largest contour [n-1][1], in this case 2
            secondlargestcontour = sorteddata[1][1]
            
            if len(contours) > 0: 
            #draw it #find second biggest contour, mark it.
                 x, y, w, h = cv2.boundingRect(secondlargestcontour)
                 cv2.drawContours(frame0, secondlargestcontour, -1, (0, 0, 255), 0)
        
                 #find biggest contour, mark it
                 green=max(contours, key=cv2.contourArea)
                 (xg,yg,wg,hg) = cv2.boundingRect(green)
                 
                 #find aspect ratio of contour
                 aspect_ratio1 = float(wg)/hg
                 aspect_ratio2 = float(w)/h

                 #set min and max ratios
                 ratioMax = 0.75
                 ratioMin = 0.30
                 
                 #only run if contour is within ratioValues
                 if (aspect_ratio1 and aspect_ratio2 <= ratioMax and aspect_ratio1 and aspect_ratio2 >= ratioMin):

                     #make the largest values always right rect
                     #this prevents negative values when not wanted
                     if (xg+wg) > x:
                        CenterOfTarget = (xg+wg-x)/2
                     else:
                        CenterOfTarget = (x-xg+wg)/2

                     if x < (xg+w):
                        CenterOfTargetCoords = (x+CenterOfTarget)
                     else:
                        CenterOfTargetCoords = (xg+w+CenterOfTarget)

                     #put values to networktable
                     Table.putNumber("PegCenterOfTargetCoords", CenterOfTargetCoords)
                     Table.putNumber("PegCenterOfTarget", CenterOfTarget)
                     Table.putBoolean("PegNoContoursFound", False)
                     
                 else: #contour not in aspect ratio
                     Table.putBoolean("PegNoContoursFound", True)

        except IndexError: #no contours found
            Table.putBoolean("PegNoContoursFound", True)
            
def trackTower():
    while (True):
        
        if(Table.getNumber("PiState", 0) != 1):
            break
        else:
            pass
        
        #grab current frame from thread
        frame1 = vs1.read()
        
        #convert to HSV
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

        #create the range of colour min/max
        green_range = cv2.inRange(hsv, constants.tower_green_lower, constants.tower_green_upper)
        
        try:
            #grab all contours based on colour range
            b, contours, _ = cv2.findContours(green_range, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0:
                #find biggest contour, mark it
                 green=max(contours, key=cv2.contourArea)
                 (xg,yg,wg,hg) = cv2.boundingRect(green)
                 
                 #find aspect ratio of contour
                 aspect_ratio1 = float(wg)/hg

                 #set min and max ratios
                 ratioMax = 3.92
                 ratioMin = 3.55
                 
                 #only run if contour is within ratioValues
                 if (ratioMin <= aspect_ratio1 <= ratioMax):
                     CenterOfTargetY = (yg+hg/2)
                     CenterOfTargetCoordsY = (yg+hg+CenterOfTargetY)

                     #put values to networktable
                     Table.putNumber("TowerCenterOfTargetCoords", CenterOfTargetCoordsY)
                     Table.putNumber("TowerCenterOfTarget", CenterOfTargetY)
                     Table.putBoolean("TowerNoContoursFound", False)
                     
                 else: #contour not in aspect ratio
                     Table.putBoolean("TowerNoContoursFound", True)

        except IndexError: #no contours found
            Table.putBoolean("TowerNoContoursFound", True)

def piState():
    return Table.getNumber("PiState", 0)

#roboRIO streams camera USB servers on ports 1181+
#Example- 10.0.66.2:1181

