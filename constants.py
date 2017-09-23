import numpy as np

#IPs and Default Table
ServerIP = '10.0.66.2' #the roboRIO
MainTable = "SmartDashboard" #reduces java footprint since SmartDashboard
								#is already initialized
PegStream = 'http://10.0.66.11/mjpg/video.mjpg' #axis camera stream
TowerStream = 'http://10.0.66.2:1181/stream.mjpg' #roboRIO usb stream

#color ranges to filter
#peg color range
peg_green_lower = np.array([72, 114, 169],np.uint8)
peg_green_upper = np.array([255, 255, 255],np.uint8)

#tower color range
tower_green_lower = np.array([72, 114, 169],np.uint8)
tower_green_upper = np.array([255, 255, 255],np.uint8)

#peg ratio values
peg_ratioMax = 0.75
peg_ratioMin = 0.30

#tower ratio values
tower_ratioMax = 3.92
tower_ratioMin = 3.55
