import Tracker

#keep sending data
while True:
    #only track tower if roboRIO signals peg is complete
    if Tracker.pegComplete() == True:
        Tracker.trackTower()
        
    else:
        Tracker.trackPeg()