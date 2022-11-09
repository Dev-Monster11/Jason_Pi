import cv2
import json
import time
from threading import Thread
import numpy as np
from screeninfo import get_monitors
import urllib.request

screen = get_monitors()[0]
cameraFrame = np.zeros((screen.width, screen.height, 3), dtype = "uint8")
contentFrame = np.zeros((screen.width, screen.height, 3), dtype = "uint8")

def loadConfig():
    with open('config.json', 'r') as config_file:
        configData = json.load(config_file)
        return configData

def cameraStream(url, flag):
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Camera is not opened")
        return    
    while(True):
        if flag == True:
            ret, cameraFrame = cap.read()
        else:
            ret, contentFrame = cap.read()
        if not ret:
            print("frame error")
            break
        if cv2.waitKey(1) == ord('q'):
            break

def contentStream(contents, start):
    # contents = val[0]
    # start = val[1]
    seconds = [0]
    temp = 0
    for content in contents:
        temp = temp + content['AdDuration']
        seconds.append(temp)
    tempStart = start
    while(True):
        now = time.perf_counter()
        delta = now - tempStart / 1000

        if (delta > seconds[len(seconds) - 1]):
            tempStart = now
        index = 0
        print('Delta is ', delta)
        for x in seconds:
            print('X is ', x)
            if (delta < x):
                print('index is ', index)
                data = contents[index - 1]
                CC(data)
            index = index + 1
        time.sleep(0.1)
def camThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
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
                break
            time.sleep(0.04)

def CC(data):
    if (data['AdType'] == 'VIDEO'):
        temp_thread = Thread(target=cameraStream, args=(data['AdPath'], False))
        temp_thread.start()
    elif (data['AdType'] == 'IMAGE'):
        url_response = urllib.request.urlopen(data['AdPath'])
        contentFrame = cv2.imdecode(np.array(bytearray(url_response.read()), dtype=np.uint8), -1)
        # contentFrame = cv2.imread(data['AdPath'])
    elif (data['AdType'] == 'SCROLL'):
        cv2.putText(contentFrame, data['AdPath'], Point(screen.width / 2, screen.height / 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, Scalar(255, 255, 255))

def buildFrame(val):
    if val == 'left_50':
        cameraFrame = cv2.resize(cameraFrame, (screen.width * 0.5, screen.height))
        contentFrame = cv2.resize(contentFrame, (screen.width * 0.5, screen.height))
    elif val == 'right_50':
        cameraFrame = cv2.resize(cameraFrame, (screen.width * 0.5, screen.height))
        contentFrame = cv2.resize(contentFrame, (screen.width * 0.5, screen.height))
    elif val == 'top_10':
        cameraFrame = cv2.resize(cameraFrame, (screen.width * 0.9, screen.height))
        contentFrame = cv2.resize(contentFrame, (screen.width * 0.1, screen.height))
    elif val == 'bottom_10':
        camera = cv2.resize(cameraFrame, (screen.width * 0.9, screen.height))
        contentFrame = cv2.resize(contentFrame, (screen.width * 0.1, screen.height))
    
    frame = np.concatenate((cameraFrame, contentFrame), axis=0)
    return frame

def frameStream(cap, config):
    frame = np.concatenate((cameraFrame, contentFrame), axis=0)
    seconds = [0]
    temp = 0
    for content in config['contents']:
        temp = temp + content['AdDuration']
        seconds.append(temp)
    tempStart = start
    while(True):
        now = time.perf_counter()
        delta = now - tempStart / 1000
        if (delta > seconds[len(seconds) - 1]):
            tempStart = now
        index = 0
        for x in seconds:
            print('X is ', x)
            if (delta < x):
                data = config['contents'][index - 1]

        try: 
            cv2.imshow('frame', buildFrame(config['layout']))
            if cv2.waitKey(1) == ord('q'):
                break
        except KeyboardInterrupt:
            print('Keyboard Interrupt')

def main():
    config = loadConfig()
    cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    frame_thread = Thread(target=frameStream, args('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4', config))
    frame_thread.start()
    # camera_thread = Thread(target=cameraStream, args=('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4', True))
    # content_thread = Thread(target=contentStream, args=(config['contents'], time.perf_counter()))
    # start = time.perf_counter()
    # camera_thread.start()
    # content_thread.start()
    # camera_thread.join()
    # content_thread.join()
    while(True):
        try: 
            cv2.imshow('frame', buildFrame(config['layout']))
            if cv2.waitKey(1) == ord('q'):
                break
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            # camera_thread.kill()
            # content_thread.kill()
            break
    # camera_thread.terminate()
    # content_thread.terminate()

    # cap.release()
if __name__ == '__main__':
    # loadConfig()
    main()
    # cap = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4')
    # if not cap.isOpened():
    #     print("Camera is not opened")

    # flag = True
    # while(True):
    #     if flag == True:
    #         ret, cameraFrame = cap.read()
    #     else:
    #         ret, contentFrame = cap.read()
    #     if not ret:
    #         print("frame error")
    #         break
    #     cv2.imshow("camera", cameraFrame)
    #     if cv2.waitKey(1) == ord('q'):
    #         break