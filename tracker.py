import numpy as np
import cv2
import logging
import constants
from networktables import NetworkTables

#set networktable information
logging.basicConfig(level=logging.DEBUG)
NetworkTables.setClientMode()
NetworkTables.initialize(server=constants.ServerIP)
Table = NetworkTables.getTable(constants.MainTable)

#seperate camera read from processing to reduce lag when
#switching targets. Needs to be tested
camera0 = cv2.VideoCapture(constants.PegStream)
(grabbed0, frame0) = camera.read()
camera1 = cv2.VideoCapture(constants.TowerStream)
(grabbed1, frame1) = camera.read()

    
def trackPeg():
    while (True):
        #stop
        if (Table.getBoolean("pegStatus", False) == True):
            break
        else:
            print("Tracking Peg...")

        #convert to HSV
        hsv = cv2.cvtColor(frame0, cv2.COLOR_BGR2HSV)

        #create the range of colour min/max
        green_range = cv2.inRange(hsv, constants.peg_green_lower, green_upper)

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
                 cv2.drawContours(frame, secondlargestcontour, -1, (0, 0, 255), 0)
        
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
        if (Table.getBoolean("pegStatus", True) == False):
            break
        else:
            print("Tracking Tower...")
            
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

                     #put values to networktable
                     Table.putNumber("TowerCenterOfTargetCoords", CenterOfTargetCoords)
                     Table.putNumber("TowerCenterOfTarget", CenterOfTarget)
                     Table.putBoolean("TowerNoContoursFound", False)
                     
                 else: #contour not in aspect ratio
                     Table.putBoolean("TowerNoContoursFound", True)

        except IndexError: #no contours found
            Table.putBoolean("TowerNoContoursFound", True)


def pegComplete():
    #grab peg status from roboRIO
    return Table.getBoolean("pegStatus", False)

#roboRIO streams camera USB servers on ports 1181+
#Example- 10.0.66.2:1181

