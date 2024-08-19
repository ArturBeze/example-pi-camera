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
import numpy as np
from datetime import datetime, timedelta
from pprint import pprint

from picamera2 import Picamera2, Metadata

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference
	
def main():
	default_model_dir = "all_models"
	default_model = "mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
	default_labels = "coco_labels.txt"
	
	parser = argparse.ArgumentParser()
	
	parser.add_argument('--model', help='.tflite model path', default=os.path.join(default_model_dir, default_model))
	parser.add_argument('--labels', help='label file path', default=os.path.join(default_model_dir, default_labels))
	parser.add_argument('--top_k', type=int, help='number of categories with highest score to display', default = 3)
	parser.add_argument('--threshold', type=float, help='classifier score threshold', default = 0.78)
	
	args = parser.parse_args()
	
	print("Loading {} with {} labels.".format(args.model, args.labels))
	
	interpreter = make_interpreter(args.model)
	interpreter.allocate_tensors()
	labels = read_label_file(args.labels)
	inference_size = input_size(interpreter)
	
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

	input("Press any key: ")

	while(True):		
		request = picam2.capture_request()
		frame = request.make_array('main')
		metadata = request.get_metadata()
		request.release()

		captureUSECLast = captureUSEC
		captureNanoSEC = str(metadata["SensorTimestamp"])
		captureUSEC = int(captureNanoSEC[0:(len(captureNanoSEC)-3)])

		print(f"TS = {metadata['SensorTimestamp']} fps = {round(1000000 / (captureUSEC - captureUSECLast), 2)}")
		
		cv2_im = frame
		cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
		cv2_im_rgb = cv2.resize(cv2_im_rgb, inference_size)
		run_inference(interpreter, cv2_im_rgb.tobytes())
		objs = get_objects(interpreter, args.threshold)[:args.top_k]
		cv2_im = append_objs_to_img(cv2_im, inference_size, objs, labels)
		pprint(f"Objects: {objs}")
		
		cv2.imshow('frame', cv2_im)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

def append_objs_to_img(cv2_im, inference_size, objs, labels):
	height, width, channels = cv2_im.shape
	scale_x, scale_y = width / inference_size[0], height / inference_size[1]
	for obj in objs:
		bbox = obj.bbox.scale(scale_x, scale_y)
		x0, y0 = int(bbox.xmin), int(bbox.ymin)
		x1, y1 = int(bbox.xmax), int(bbox.ymax)

		percent = int(100 * obj.score)
		label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))

		v2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
		cv2_im = cv2.putText(cv2_im, label, (x0, y0 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

	return cv2_im

def time_elapsed(start_time, event):
	time_now = time.time()
	duration = (time_now - start_time) * 1000
	duration=round(duration, 2)
	print (">>> ", duration, " ms (" ,event, ")")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Keyboard Interrupt")
		try:
			sys.exit(130)
		except SystemExit:
			os._exit(130)
