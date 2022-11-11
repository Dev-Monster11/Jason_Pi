import cv2
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('../output.avi', fourcc, 25.0, (1920, 1080))

def main():
	index = 0
	while True:
		img = cv2.imread("{0}.jpg".format(index))
		if img is not None:
			out.write(img)
		else:
			break;
		cv.waitKey(1)
		if (index % 100 == 0):
			print(index / 100)
		if index == 15000:
			break
		index = index + 1
	out.release()
	exit(1)


if __name__ == '__main__':
    main()