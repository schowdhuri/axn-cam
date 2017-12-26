#!/usr/bin/python
import RPi.GPIO as gpio
import picamera

from datetime import datetime
from time import sleep

LOG_FILE = "/var/log/axn_cam.log"
INDEX_FILE = "index"

PIN_RECORD_LED = 15
PIN_RECORD_SWITCH = 11

logfile = None

def log(msg=""):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log = "[%s] %s" % (timestamp, msg)
    logfile.write(log)
    logfile.write("\n")
    logfile.flush()
    print log

def startup_blip():
    for i in xrange(1,3):
        set_recording_light(True)
        sleep(0.2)
        set_recording_light(False)
        sleep(0.2)

def setup_gpio():
    gpio.setwarnings(False)
    gpio.cleanup()
    gpio.setmode(gpio.BOARD)
    gpio.setup(PIN_RECORD_SWITCH, gpio.IN)
    gpio.setup(PIN_RECORD_LED, gpio.OUT)
    log("GPIO ready")

def set_recording_light(status=False):
    gpio.output(PIN_RECORD_LED, gpio.HIGH if status else gpio.LOW)

def get_record_switch_status():
    return gpio.input(PIN_RECORD_SWITCH)==1

def get_filename():
    try:
        indexfile = open(INDEX_FILE, "r")
        last_index = int(indexfile.read().strip())
        indexfile.close()
        new_index = last_index + 1
        indexfile = open(INDEX_FILE, "w")
        indexfile.write("%s" % new_index)
        indexfile.flush()
        indexfile.close()
        return "video-%05d.h264" % new_index
    except Exception as ex:
        print ex.message
        return "video-%s.h264" % datetime.now().strftime("%F-%H-%M-%S")

def start_recording(camera):
    filename = get_filename()
    camera.start_recording(filename, "h264", bitrate=0, quality=25)  
    set_recording_light(True)
    log("Recording to %s" % filename)
    sleep(2)

def stop_recording(camera):
    camera.stop_recording()
    set_recording_light(False)
    log("Stopped recording")
    sleep(1)

def setup_camera():
    camera = picamera.PiCamera()
    camera.resolution = (1280, 720)
    camera.rotation = 90
    log("Camera ready")
    return camera

if __name__ == "__main__":
    logfile = open(LOG_FILE, "a")
    log("Starting up...")
    setup_gpio()
    camera = setup_camera()
    startup_blip()
    recording = False
    log("Waiting for user action...")
    try:
        while True:
            if get_record_switch_status():
                if recording:
                    stop_recording(camera)
                    recording = False
                else:
                    start_recording(camera)
                    recording = True
    except Exception as ex:
        log(ex.message)
    finally:
        log("All done. Bye!")
        logfile.close()
        gpio.cleanup()
