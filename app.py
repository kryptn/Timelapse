
from time import sleep
from datetime import datetime

from picamera import PiCamera

def capture():
    c = PiCamera()
    c.resolution = (1920, 1080)
    filename = datetime.now().strftime("%F.%T")
    c.iso = 400
    sleep(2)
    c.shutter_speed = c.exposure_speed
    c.exposure_mode = 'off'
    g = c.awb_gains
    c.awb_mode = 'off'
    c.awb_gains = g
    sleep(2)
    c.capture("images/{}.png".format(filename))

if __name__ == "__main__":
    capture()
