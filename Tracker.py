from networktables import NetworkTables
import Constants
import logging
import cv2

logging.basicConfig(level=logging.DEBUG)
PEGCamera = Constants.PEGCameraIP
TowerCamera = Constants.TowerCameraIP

def trackPeg():
    #Send data over to roboRIO
    NetworkTables.setClientMode()
    NetworkTables.initialize(server=Constants.ServerIP)
    Table = NetworkTables.getTable(Constants.MainTable)
    
    #read the current frame from camera
    frame = PEGCamera.read()

    #convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #create the range of colour min/max
    peg_green_range = cv2.inRange(hsv, Constants.peg_green_lower, Constants.peg_green_upper)

    #create blank array for sort
    areaArray = []
    try:
        #grab all contours based on colour range
        contours, _ = cv2.findContours(peg_green_range, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #order contours into an array by area
        for c in enumerate(contours):
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
    #send data over to roboRIO
    NetworkTables.setClientMode()
    NetworkTables.initialize(server=Constants.ServerIP)
    Table = NetworkTables.getTable(Constants.MainTable)
    
    #read the current frame from camera
    frame = TowerCamera.read()

    #convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #create the range of colour min/max
    tower_green_range = cv2.inRange(hsv, Constants.tower_green_lower, Constants.tower_green_upper)

    try:
        #grab all contours based on colour range
        contours, _ = cv2.findContours(tower_green_range, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
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
                CenterOfTargetCoords = (yg+hg+CenterOfTargetY)

                #put values to networktable
                Table.putNumber("TowerCenterOfTargetCoords", CenterOfTargetCoords)
                Table.putNumber("TowerCenterOfTarget", CenterOfTargetY)
                Table.putBoolean("TowerNoContoursFound", False)
                 
            else: #contour not in aspect ratio
                Table.putBoolean("TowerNoContoursFound", True)

    except IndexError: #no contours found
        Table.putBoolean("TowerNoContoursFound", True)

def pegComplete():
    #Receive Data from roboRIO
    Table = NetworkTables.getTable(Constants.MainTable)
    
    return Table.getBoolean(pegStatus, False)
