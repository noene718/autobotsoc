#!/usr/bin/env python3
# -- coding: utf-8 --
"""
Process manager for all the SoC funtions
Usage::
    ./watchsoc.py
"""

import os
import json
import requests
from picamera import PiCamera 
from time import sleep


def main():
    # start camera
    camera = PiCamera()
    camera.start_preview()
    sleep(2)

    while(True):
        # do everything forever
        sleep(15)
        camera.capture('image.jpg')
        os.system('git add image.jpg')
        os.system('git commit')
        os.system('git push')

        response = requests.get("uas-at-fgcu/soc")
        tasks = json.load(response.text)

        if tasks["camera-mode"] == 'default':
            camera.exposure_mode = 'auto'
            camera.image_effect = 'none'

        if tasks["camera-mode"] == 'night':
            camera.exposure_mode = 'night'

        if tasks["camera-restart"] == True:
            # restart camera
            camera.stop_preview()
            sleep(2)
            camera.start_preview()
            sleep(2)
        
        if tasks["soc-restart"] == True:
            os.command("shutdown -r now")
    pass

if __name__ == "__main__":
    main()