# Dual Tracking System for the 2017 FRC Game
	The Dual Tracking System for the 2017 FRC Game SteamWorks was developed by
	Dalton Smith of Robotics Team 66. It was designed to be used with an axis camera
	and a RaspberryPi3 but can be easily changed to work with USB cameras. Code can be
	ran on any co-processor with python and opencv capabilities. 
	
## Development Environment
	**The code was used in a virtual environment with the following installed:**
	
	Python 3.4 (Programming Language)
	OpenCV 3.1.0 (Vision Tracking Library)
	Numpy (Managing numpy arrays from OpenCV)
	PyNetworkTables (Sending and Receiving Data)
	imutils (Easy way for camera multithreading)

## Program Goals:
	*Code is completely modular and adaptable.
	*Code is simple to use and well commented.
	*Code is reusable.

## To Note:
	*Prefered IP setup is static IP, untested for MDNS
	*roboRIO streams camera USB servers on ports 1181+
	*Example- 10.0.66.2:1181 //Streams the first camera server.
	
## License:
	*The 2017-FRC-Dual-Tracker-System is licensed under the GNU General Public License v3.0.
	*License can by found under the file license.txt
