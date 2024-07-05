#!/usr/bin/python3

import cv2

from picamera2 import Picamera2

cv2.startWindowThread()

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)})
picam2.configure(config)
picam2.set_controls({"FrameRate": 40})
picam2.start()

while True:
	im = picam2.capture_array()

	cv2.imshow("Camera", im)

	# Press 'q' to quit
	if cv2.waitKey(1) == ord('q'):
		break

picam2.stop()
