from threading import Thread
import cv2
import constants

def __init__(self, src1=constants.PegStream):
    self.stream = cv2.VideoCapture(src1)
    (self.grabbed, self.frame) = self.stream.read()
    self.stopped = False

def start(self):
    Thread(target=self.update, args=()).start()
    return self

def update(self):
    while True:
        if self.stopped:
            return

        (self.grabbed, self.frame) = self.stream.read()

def read(self):
    return self.frame

def stop(self):
    self.stopped = True
