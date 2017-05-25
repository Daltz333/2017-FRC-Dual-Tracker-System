import tracker
import constants

while(True):
    PiState = tracker.piState()
    
    if(PiState == 0):
        tracker.trackPeg()
    elif(PiState == 1):
        tracker.trackTower()
    else:
        continue
