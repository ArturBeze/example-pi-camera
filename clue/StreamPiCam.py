import time, libcamera
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder

picam2 = Picamera2()

camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, \
	lores={"size": (640, 480)}, display="lores")

preview_config = picam2.create_preview_configuration(main={"size": (1600, 1200), "format": "XRGB8888"}, \
	lores={"size": (640,480), "format": "YUV420"}, display = "lores")
preview_config["transform"] = libcamera.Transform(hflip = 1, vflip = 1)

picam2.configure(preview_config)

picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(10)
picam2.capture_file("test.jpg")
picam2.stop_preview()
picam2.close()
