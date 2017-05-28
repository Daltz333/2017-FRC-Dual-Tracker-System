import tracker
import constants

#PiState is by default 0. If change is detected,
#at the top of each method is a if-else
#that checks whenever it isn't the correct value,
#if it is not the correct value, than
#it breaks the internal loop in each method.
#It then continues running the following loop
#where it sets what target to track.

while(True):
    PiState = tracker.piState()
    
    #grab selection of target from roborio
    if(PiState == 0):
        tracker.trackPeg()
    elif(PiState == 1):
        tracker.trackTower()
    elif(PiState == -1):
        break
    else:
        continue
