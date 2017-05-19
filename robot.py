import tracker

#if statement in each method determines which is ran.
#if pegComplete == True, ends the trackPeg method and only
#then does it run the trackTower method. The inverse applies
#and the trackPeg begins again.

while(True):
    tracker.trackPeg()
    tracker.trackTower()
