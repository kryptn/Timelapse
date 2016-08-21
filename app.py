import os
from time import sleep
from datetime import datetime

import yaml
import boto3
from pantry import pantry
from picamera import PiCamera

def initialize_pantry(pf):
    if os.path.isfile(pf):
        return

    with pantry(pf) as db:
        db['local'] = list()
        db['images'] = list()
        db['captured'] = 0
        db['uploaded'] = 0

def capture(pf):
    c = PiCamera()
    c.resolution = (1920, 1080)
    now = datetime.now()
    filename = now.strftime("%F.%T")
    c.iso = 200
    sleep(2)
    c.shutter_speed = c.exposure_speed
    c.exposure_mode = 'off'
    g = c.awb_gains
    c.awb_mode = 'off'
    c.awb_gains = g
    sleep(2)
    c.capture("images/{}.png".format(filename))
    data = {'filename': '{}.png'.format(filename),
            'datetime': now}
    with pantry(pf) as db:
        db['local'].append(data)
        db['captured'] += 1

def upload_image(filename, bucket):
    s3 = boto3.resource('s3')
    target = '/home/pi/projects/timelapse/images/{}'.format(filename)
    dest = 'images/{}'.format(filename)
    s3.meta.client.upload_file(target, bucket, dest)

def upload_local(pf, bucket):
    with pantry(pf) as db:
        while db['local']:
            im = db['local'].pop(0)
            upload_image(im['filename'], bucket)
            db['images'].append(im)
            db['uploaded'] += 1

if __name__ == "__main__":
    with open('config.yml') as f:
        settings = yaml.load(f)

    initialize_pantry(settings['pantry_filename'])

    capture(settings['pantry_filename'])


