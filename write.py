
import cv2
import json
import time
from threading import Thread
import numpy as np
from screeninfo import get_monitors
import urllib.request
import random

screen = get_monitors()[0]
width = screen.width
height = screen.height


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (width, height))
def loadConfig():
    with open('config.json', 'r') as config_file:
        configData = json.load(config_file)
        return configData

class MyThread(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url
        self.frame = np.zeros((width, height, 3), dtype = "uint8")
        self.flag = False
        self.cap = cv2.VideoCapture(self.url)
        if not self.cap.isOpened():
            print("Camera is not opened")
            exit(0)
    def startThread():
        self.flag = True
    def killThread():
        self.flag = False
        if self.cap.isOpened():
            self.cap.release()
        self.join()
    def run(self):
        while(self.flag):
            ret, self.frame = self.cap.read()
            if not ret:
                print("frame error")
                self.cap.release()
                break
            time.sleep(0.04)
    def kill(self):

        self.join()
def buildFrame(val, cameraFrame, contentFrame):
    frame = np.zeros((width, height, 3), dtype = "uint8")
    if val == 'left_50':
        contentFrame = cv2.resize(contentFrame, (int(width * 0.5), height))
        cameraFrame = cv2.resize(cameraFrame, (int(width * 0.5), height))
        frame = cv2.hconcat([cameraFrame, contentFrame])

    elif val == 'right_50':
        cameraFrame = cv2.resize(cameraFrame, (int(width * 0.5), height))
        contentFrame = cv2.resize(contentFrame, (int(width * 0.5), height))
        frame = cv2.hconcat(contentFrame, cameraFrame)
    elif val == 'top_10':
        cameraFrame = cv2.resize(cameraFrame, (int(width * 0.9), height))
        contentFrame = cv2.resize(contentFrame, (int(width * 0.1), height))
        frame = cv2.vconcat(contentFrame, cameraFrame)
    elif val == 'bottom_10':
        camera = cv2.resize(cameraFrame, (int(width * 0.9), height))
        contentFrame = cv2.resize(contentFrame, (int(width * 0.1), height))
        frame = cv2.vconcat(cameraFrame, contentFrame)
    cv2.imshow('frame', frame)
    # out.write(frame)
def main():
    config = loadConfig()

    start = time.time()
    # camera = MyThread(0)
    # camera.startThread()
    
    # seconds = [0]
    # temp = 0
    # for content in config['contents']:
    #     temp = temp + content['AdDuration']
    #     seconds.append(temp)
    # # print(seconds)
    # # exit(0)
    start = time.time()
    tempStart = start
    cap = cv2.VideoCapture(0)
    adSize = (0, 0)
    if (config['layout'] == 'left_50' or config['layout'] == 'right_50'):
        adSize = (int(width * 0.5), height)
    else:
        adSize = (width, int(height * 0.1))
    contentShow = False
    while(True):

        now = time.time()
        

        if (now - start) % config['period'] == 0:
            tempStart = now
            contentShow = True
        # index = 0
        # contentFrame = np.zeros((width, height, 3), dtype = "uint8")
        # for x in seconds:
        #     if (delta < x):
        #         break
        #     index = index + 1

        # data = config['contents'][index - 1]
        # if (data['AdType'] == 'VIDEO'):
        #     content = camThread(data['AdPath'])
        #     content.start()
        #     contentFrame = content.frame
        # elif (data['AdType'] == 'IMAGE'):
        #     url_response = urllib.request.urlopen(data['AdPath'])
        #     contentFrame = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)
        # elif (data['AdType'] == 'SCROLL'):
        #     cv2.putText(contentFrame, data['AdPath'], (width / 2, height / 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255))

        # buildFrame(config['layout'], camera.frame, contentFrame)

        _, frame = cv2.read()
        if contentShow:
            index = random.randint(0, len(config['contents']) - 1)
            data = config['contents'][index]
            adDuration = time.time() - tempStart
            if (adDuration > data['AdDuration']):
                contentShow = False
            if (data['AdType'] == 'IMAGE'):
                url_response = urllib.request.urlopen(data['AdPath'])
                contentFrame = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)
                contentFrame = cv2.resize(contentFrame, adSize)
                if (data['layout'] == 'left_50'):
                    frame[0:height, 0:int(width/2)] = contentFrame
                elif (data['layout'] == 'right_50'):
                    frame[0:height, int(width/2):width] = contentFrame
                elif (data['layout'] == 'top_10'):
                    frame[0:int(height/10), 0:width] = contentFrame
                elif (data['layout'] == 'bottom_10'):
                    frame[int(height/10):height, 0:width] = contentFrame
            cv2.imshow('frame', frame)
        try:
            if cv2.waitKey(1) == ord('q'):
                break
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            camera.kill()
            out.release()
            # camera_thread.kill()
            # content_thread.kill()
            break

if __name__ == '__main__':
    main()