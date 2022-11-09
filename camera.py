import cv2
import time
cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	cv2.imshow("frame", frame)
	if not ret:
		
		break
	cv2.waitKey(0)

cap.release()
