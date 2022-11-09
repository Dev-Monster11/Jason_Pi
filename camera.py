import cv2
import time
cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()

	if not ret:
		
		break
	cv2.imshow("frame", frame)
	time.sleep(0.04)
cap.release()
