#!/usr/bin/python


import time, random
from dotstar import Adafruit_DotStar

# Here's how to control the strip from any two GPIO pins:
datapin = 10
clockpin = 12

numpixels = 60 #which is the therotical max of the Netball ring lights.

#configure the strip

strip = Adafruit_DotStar(numpixels, 6000000, order='gbr')

strip.begin()
strip.clear()
strip.show()
