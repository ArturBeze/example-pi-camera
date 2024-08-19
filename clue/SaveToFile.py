import time
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2 import Metadata

picam2 = Picamera2()

video_config = picam2.create_video_configuration(main={"size": (1640, 1232)}, \
	controls={"FrameDurationLimits": (40000, 40000)}, \
	lores={"size": (640, 480)})

picam2.configure(video_config)

encoder = H264Encoder(10000000)
output = "test.h264"

picam2.start_preview(Preview.QTGL)
picam2.start_recording(encoder, output)
time.sleep(10)
picam2.stop_recording()
picam2.stop_preview()

#picam2.capture_metadata()["FrameDuration"]
#picam2.capture_metadata()["SensorTimestamp"]
#metadata = Metadata(picam2.capture_metadata())
