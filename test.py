
import cv2
import json
import time
from threading import Thread
import numpy as np
from screeninfo import get_monitors
import urllib.request

screen = get_monitors()[0]
print(screen)
cameraFrame = np.zeros((screen.width, screen.height, 3), dtype = "uint8")
contentFrame = np.zeros((screen.width, screen.height, 3), dtype = "uint8")

class MyThread(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url
        self.frame = np.zeros((screen.width, screen.height, 3), dtype = "uint8")

    def run(self):
        cap = cv2.VideoCapture(self.url)
        if not cap.isOpened():
            print("Camera is not opened")
            return   
        while(True):
            ret, self.frame = cap.read()
            if not ret:
                print("frame error")
                cap.release()
                break
            time.sleep(0.04)
    def kill(self):
        if cap.isOpened():
            cap.release()
        self.join()

def frameStream(cap, config, start):
    
    seconds = [0]
    temp = 0
    for content in config['contents']:
        temp = temp + content['AdDuration']
        seconds.append(temp)
    tempStart = start
    camera = MyThread(0)
    camera.start()
    print(seconds)
    while(True):
        # cv2.imshow('asdf', camera.frame)
        now = time.time()
        
        # print('delta is ', delta)
        # if (delta > seconds[len(seconds) - 1]):
        #     tempStart = now
        delta = (now - tempStart) % seconds[len(seconds) - 1]
        index = 0
        contentFrame = np.zeros((screen.width, screen.height, 3), dtype = "uint8")
        for x in seconds:
            if (delta < x):
                break
            index = index + 1

        data = config['contents'][index - 1]
        print('Content Data is ', data)
        if (data['AdType'] == 'VIDEO'):
            content = camThread(data['AdPath'])
            content.start()
            contentFrame = content.frame
        elif (data['AdType'] == 'IMAGE'):
            url_response = urllib.request.urlopen(data['AdPath'])
            contentFrame = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)
        elif (data['AdType'] == 'SCROLL'):
            cv2.putText(contentFrame, data['AdPath'], (screen.width / 2, screen.height / 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255))
        try:
            # cv2.imshow('abc', camera.frame)
            # cv2.imshow('bcd', contentFrame)

            buildFrame(config['layout'], camera.frame, contentFrame)

            time.sleep(1)
            # if cv2.waitKey(1) == ord('q'):
            #     break
        except KeyboardInterrupt:
            print('Keyboard Interrupt')

def buildFrame(val, cameraFrame, contentFrame):
    frame = np.zeros((screen.width, screen.height, 3), dtype = "uint8")
    if val == 'left_50':
        contentFrame = cv2.resize(contentFrame, (int(screen.width * 0.5), screen.height))
        cameraFrame = cv2.resize(cameraFrame, (int(screen.width * 0.5), screen.height))
        cv2.imwrite("content.jpg", contentFrame)
        cv2.imwrite("camera.jpg", cameraFrame)
        frame = cv2.hconcat([cameraFrame, contentFrame])
        
        # cv2.imwrite("2.jpg", frame)
        # # b = cv2.vconcat(cameraFrame, contentFrame)
        # # cv2.imwrite("3.jpg", b)
    elif val == 'right_50':
        cameraFrame = cv2.resize(cameraFrame, (int(screen.width * 0.5), screen.height))
        contentFrame = cv2.resize(contentFrame, (int(screen.width * 0.5), screen.height))
        frame = cv2.hconcat(contentFrame, cameraFrame)
    elif val == 'top_10':
        cameraFrame = cv2.resize(cameraFrame, (int(screen.width * 0.9), screen.height))
        contentFrame = cv2.resize(contentFrame, (int(screen.width * 0.1), screen.height))
        frame = cv2.vconcat(contentFrame, cameraFrame)
    elif val == 'bottom_10':
        camera = cv2.resize(cameraFrame, (int(screen.width * 0.9), screen.height))
        contentFrame = cv2.resize(contentFrame, (int(screen.width * 0.1), screen.height))
        frame = cv2.vconcat(cameraFrame, contentFrame)
    print('concatenate done')
    # return contentFrame
    # cv2.imshow('frame', frame)
    
    # cv2.imwrite("content.jpg", contentFrame)
    
    # exit()
def loadConfig():
    with open('config.json', 'r') as config_file:
        configData = json.load(config_file)
        return configData

def main():
    config = loadConfig()
    cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    start = time.time()
    frame_thread = Thread(target=frameStream, args=('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4',config, start))
    frame_thread.start()
    while(True):
        # frame_thread.join()

        try: 
            # cv2.imshow('frame', buildFrame(config['layout'], ))
            if cv2.waitKey(1) == ord('q'):
                break
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            frame_thread.join()
            # camera_thread.kill()
            # content_thread.kill()
            break

if __name__ == '__main__':

    main()