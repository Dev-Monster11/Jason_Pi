
import cv2
import json
import time
import sys
from screeninfo import get_monitors
import urllib.request
import numpy as np
from PyQt5.QtCore import QTimer, QThread, Qt
from PyQt5.QtWidgets import QLabel, QApplication, QDialog
from PyQt5.QtGui import QImage, QPixmap, QPainter

screen = get_monitors()[0]
width = screen.width
height = screen.height


class MainDlg(QDialog):
    def __init__(self):
        super(MainDlg, self).__init__()
        self.config = self.loadConfig()
        self.seconds = [0]
        temp = 0
        for content in self.config['contents']:
            temp = temp + content['AdDuration']
            self.seconds.append(temp)
        self.camera = cv2.VideoCapture(0)
        self.frame = np.zeros((width, height, 3), dtype = "uint8")
        self.content = np.zeros((width, height, 3), dtype="uint8")
        self.start = time.time()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)

        self.transitionTimer = QTimer()
        self.transitionTimer.timeout.connect(self.transition)


        self.changeContentTimer = QTimer()
        self.changeContentTimer.timeout.connect(self.changeContent)
        self.changeContentTimer.setSingleShot(True)
        self.changeContentTimer.start(self.seconds[0] * 1000)
        self.contentIndex = 0

        self.timer.start(40)

        self.startFlag = False


        # self.content = QLabel(self)
        # self.content.setStyleSheet('background-color: transparent')


    def transition(self):

        pass
    def changeContent(self):
        print('changecontent')
        data = self.config['contents'][self.contentIndex]
        contentFrame = cv2.imread(data['AdPath'])
        
        if self.config['layout'] == 'left_50' or self.config['layout'] == 'right_50':
            print('asdf')
            contentFrame = cv2.resize(contentFrame, (int(width*0.5), height))
        else:
            print('asdf')
            contentFrame = cv2.resize(contentFrame, (int(width*0.1), height))
        self.content = contentFrame
        
        self.contentIndex = self.contentIndex + 1
        self.changeContentTimer.start(self.seconds[self.contentIndex] * 1000)
    def paintEvent(self, event):
        if self.startFlag == True:
            painter = QPainter(self)
            if self.config['layout'] == 'left_50':
                self.frame[0:height, 0:int(width/2)] = self.content
            elif self.config['layout'] == 'right_50':
                self.frame[0:height, int(width/2):width] = self.content
            elif self.config['layout'] == 'bottom_10':
                self.frame[int(height*0.9):height, 0:width] = self.content
            elif self.config['layout'] == 'top_10':
                self.frame[0:int(height*0.1), 0:width] = self.content
            frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            h, w, _ = frame.shape
            bg = QImage(frame.data, w, h, w * 3 ,QImage.Format_RGB888)
            bg = bg.scaled(width, height)
            painter.drawImage(0, 0, bg)
    def loadConfig(self):
        with open('config_local.json', 'r') as config_file:
            configData = json.load(config_file)
            return configData

    def updateFrame(self):
        print('update')
        ret, self.frame = self.camera.read()
        # self.startFlag = ret
        # now = time.time()
        # delta = (int(now - tempStart / 1000)) % self.seconds[len(seconds) - 1]

        # index = 0
        # for x in seconds:
        #     if (delta < x):
        #         break
        #     index = index + 1
        # data = config['contents'][index - 1]
        # if (data['AdType'] == 'IMAGE'):

        #     url_response = urllib.request.urlopen(data['AdPath'])
        #     contentFrame = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)
        #     if (config['layout'] == 'left_50' or config['layout'] == 'right_50'):
        #         contentFrame = cv2.resize(contentFrame, (int(width*0.5), height))
        #     else:
        #         contentFrame = cv2.resize(contentFrame, (int(width*0.1), height))
        # elif (data['AdType'] == 'VIDEO'):

        # elif (data['AdType'] == 'SCROLL'):
        #     url_response = urllib.request.urlopen(data['AdPath'])
        #     contentFrame = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)

        self.repaint()    
    def releaseAll(self):
        self.timer.stop()
        self.camera.release()
        exit(0)
    def keyPressEvent(self, event):
        if event.key() == 'q':
            self.releaseAll()       




def main():
    app = QApplication(sys.argv)
    mainDlg = MainDlg()
    mainDlg.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()