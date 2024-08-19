"""
Created on Tue Feb  9 14:30:58 2021
adapted from
https://gist.github.com/keithweaver/5bd13f27e2cc4c4b32f9c618fe0a7ee5
but nearly same code is referenced in
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
"""

import sys, os
import cv2
import argparse
import time
from datetime import datetime, timedelta
from pprint import pprint

from picamera2 import Picamera2, Metadata

import numpy as np
from PIL import Image
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

def main():
	resX = 640
	resY = 480
	fps = 206

	picam2 = Picamera2()
	video_config = picam2.create_video_configuration(main={"size": (resX, resY), "format": 'RGB888'}, raw=picam2.sensor_modes[0], buffer_count=8)
	picam2.configure(video_config)

	pprint(picam2.sensor_modes)
	print("##############################")

	picam2.set_controls({"FrameRate": fps})
	picam2.start()
	picam2.title_fields = ["ExposureTime", "AnalogueGain"]

	metadata = Metadata(picam2.capture_metadata())
	pprint(picam2.capture_metadata())
	print("##############################")

	captureNanoSEC = str(metadata.SensorTimestamp)
	captureUSEC0 = int(captureNanoSEC[0:(len(captureNanoSEC)-3)])
	captureUSEC = captureUSEC0

	#TimeUSecond = timedelta(microseconds = 1)

	#tFrame0 = datetime.now()
	#tNowFrame = tFrame0 + TimeUSecond * (captureUSEC - captureUSEC0)
	#tNowFrameLast = tNowFrame

	input("Press any key: ")

	while(True):
		#frame = picam2.capture_array()
		#metadata = Metadata(picam2.capture_metadata())

		request = picam2.capture_request()
		frame = request.make_array('main')
		metadata = request.get_metadata()
		request.release()

		captureUSECLast = captureUSEC
		captureNanoSEC = str(metadata["SensorTimestamp"])
		captureUSEC = int(captureNanoSEC[0:(len(captureNanoSEC)-3)])

		#tNowFrameLast = tNowFrame
		#tNowFrame = tFrame0 + TimeUSecond * (captureUSEC - captureUSEC0)

		print(f"TS = {metadata['SensorTimestamp']} fps = {round(1000000 / (captureUSEC - captureUSECLast), 2)}")

		#cv2.imshow('frame',frame)
		#if cv2.waitKey(1) & 0xFF == ord('q'):
		#	break

	#cv2.destroyAllWindows()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Keyboard Interrupt")
		try:
			sys.exit(130)
		except SystemExit:
			os._exit(130)
