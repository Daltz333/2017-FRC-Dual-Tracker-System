import tracker
import constants
from networktables import NetworkTables

NetworkTables.setClientMode()
NetworkTables.initialize(server=constants.ServerIP)
Table = NetworkTables.getTable(constants.MainTable)

while(True):
    PiState = Table.getNumber("PiState", 0)
    
    if(PiState == 0):
        tracker.trackPeg()
    elif(PiState == 1):
        tracker.trackTower()
    else:
        continue
