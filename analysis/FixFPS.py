#changing to_array to True will cause the issue

from picamera2 import Picamera2
import time
import sys
import os

last_timestamp = 0

to_array = True

def frame_time(cam):
    global last_timestamp
    picam2 = cam
    timestamp = picam2.capture_metadata()['SensorTimestamp']
    frameTime = (timestamp - last_timestamp) / 1000000
    last_timestamp = timestamp
    return frameTime

def main():
    picam2 = Picamera2()
    print("\n Sensor modes...." )
    print(picam2.sensor_modes)

    config = picam2.create_video_configuration(
    main={"size": (640, 480), "format": "RGB888"}, 
    controls={"FrameRate": 206},
    buffer_count=4
    )
    picam2.configure(config)
    print("\n Config....")
    print(config)

    picam2.start()

    print("\n Meta data....")
    metadata = picam2.capture_metadata()
    print(metadata,"\n")

    while True:
        #1st
        a_time = time.time()
        this_frame_time = frame_time(picam2)
        #2nd
        b_time = time.time()
        if to_array:
            img = picam2.capture_array("main")
            
            c_time = time.time()
            print("Res:", img.shape)
            print("Fps:",round(1000/this_frame_time, 2),"1st:",b_time - a_time, "2nd:",c_time-b_time, "Total:", c_time-a_time)
            
        else: 
            c_time = time.time()
            print("Fps:",round(1000/this_frame_time, 2),"1st:",b_time - a_time, "2nd:",c_time-b_time, "Total:", c_time-a_time)
            
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
