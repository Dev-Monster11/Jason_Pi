
from PyQt5.QtCore import QObject, QThread, Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage, QPixmap
import cv2
class CameraBackend(QObject):
    def __init__(self):
        super(CameraBackend, self).__init__()
        self.tempPath = './'
    def setViewFinder(self, label):
        self.viewFinder = label
    def startStream(self):
        self.cap = cv2.VideoCapture(0)
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.captureVideo)
        self.thread.start()
    def stopStream(self):
        self.cap.release()
        self.thread.quit()
    def captureVideo(self):
        if not self.cap.isOpened():
            print('camera is not detected')
            return
        while True:
            _, frame = self.cap.read()
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            h, w, _ = image.shape

            bPL = w
            qImg = QImage(image.data, w, h, bPL, QImage.Format_RGB888).scaled(self.viewFinder.width(), self.viewFinder.height())
            self.viewFinder.setPixmap(QPixmap.fromImage(qImg))
            
            QThread.msleep(40)
    
