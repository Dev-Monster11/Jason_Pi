
import cv2
import json
import time
import sys
from screeninfo import get_monitors
import urllib.request

from PyQt5.QtCore import QTimer, QThread, Qt
from PyQt5.QtWidgets import QLabel, QApplication, QDialog
from PyQt5.QtGui import QImage, QPixmap, QPainter
import numpy as np
# screen = get_monitors()[0]
# width = screen.width
# height = screen.height
width = 640
height = 480
class MainDlg(QDialog):
    def __init__(self):
        super(MainDlg, self).__init__()

        self.config = self.loadConfig()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.frame = np.zeros((width, height, 3), dtype = "uint8")
        self.camera = cv2.VideoCapture(0)
        self.cameraStarted = False
        if self.camera.isOpened():
            self.timer.start(1)

    def loadConfig(self):
        with open('config.json', 'r') as config_file:
            configData = json.load(config_file)
            return configData
    def paintEvent(self, event):
        if (self.cameraStarted == True):
            painter = QPainter(self)
            frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            h, w, _ = frame.shape
            bg = QImage(frame.data, w, h, w * 3 ,QImage.Format_RGB888)
            bg = bg.scaled(width, height)
            painter.drawImage(0, 0, bg)
            cv2.imshow('frame', frame)
    def releaseAll(self):
        self.timer.stop()
        self.camera.release()
        exit(0)
    def keyPressEvent(self, event):
        if event.key() == 'q':
            self.releaseAll()
    def updateFrame(self):
        ret, self.frame = self.camera.read()
        if ret:
            self.cameraStarted = True
def main():
    app = QApplication(sys.argv)
    mainDlg = MainDlg()
    mainDlg.setGeometry(0, 0, width, height)
    mainDlg.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()