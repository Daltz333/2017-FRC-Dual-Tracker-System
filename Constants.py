import numpy as np

#IPs and Default Table
ServerIP = '10.0.66.2'
MainTable = "SmartDashboard"
PEGCameraIP = '10.0.66.11'
TowerCameraIP = '10.0.66.14'

#color ranges to filter
#peg color range
peg_green_lower = np.array([72, 114, 169],np.uint8)
peg_green_upper = np.array([255, 255, 255],np.uint8)

#tower color range
tower_green_lower = np.array([72, 114, 169],np.uint8)
tower_green_upper = np.array([255, 255, 255],np.uint8)