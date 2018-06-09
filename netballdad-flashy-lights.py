#!/usr/bin/python


import time, random
from dotstar import Adafruit_DotStar

# Here's how to control the strip from any two GPIO pins:
datapin = 10
clockpin = 12

# red, blue, green
colourArray = [["red", 255, 0, 0],
               ["orange", 255, 0, 128],
               ["yellow", 255, 0, 255],
               ["light green", 128, 0, 255],
               ["green", 0, 0, 255],
               ["teal", 0, 128, 255],
               ["acqua", 0, 255, 255],
               ["light blue", 0, 255, 128],
               ["blue", 0, 255, 0],
               ["purple", 128, 255, 0],
               ["light purple", 255, 255, 0],
               ["pink", 255, 128, 0]]


def getNumpixels():
    findNumPixels = 0
    while True:
        strip.setPixelColor(findNumPixels, 100, 100, 100) #we won't show this setting anyways
        print("setting this pixel " + str(findNumPixels))
        findNumPixels += 1

    numpixels = findNumPixels + 1
    print("this strip has " + str(numpixels) + " in it")

def getColour(colour):
    for c in range(len(colourArray)):
        if colourArray[c][0] == colour:
            return colourArray[c]

def rainbow():
    for c in range(len(colourArray)):

        strip.clear()
        strip.show()
        time.sleep(0.5)
        print(colourArray[c][0])
        for n in range(numpixels):
            strip.setPixelColor(n, colourArray[c][1], colourArray[c][2], colourArray[c][3])
            print("about to show next pixel " + str(n))
            strip.show()
            time.sleep(0.15)

        time.sleep(1.0)
        print("about to flash ")
        flashLights(0.5)


def ticktock(size, loops, colourA, colourB):
    for l in range(loops):
        colourstart = 0
        strip.clear()
        strip.show()
        print("start Loop")
        for aLoop in range(numpixels):
            # set the first olours up
            print("inner loop 1 - setup first colour")
            for c1 in range(size):
                print("setting pixel " + str(colourstart))
                strip.setPixelColor(colourstart, colourA[1], colourA[2], colourA[3])
                colourstart += 1
            # print ("colour1start  " + str(colour1start)
            colourstart += size
            if colourstart >= 30:
                colourstart = 0
                break
        strip.show()
        time.sleep(0.5)
        # blank them out
        strip.clear()

        for bLoops in range(numpixels):
            print ("setup second colour")
            colourstart += size  # start at the end of the first set
            print("the starting for the second loop is " + str(colourstart))
            for c2 in range(size):
                print("setting second pixel " + str(colourstart))
                strip.setPixelColor(colourstart, colourB[1], colourB[2], colourB[3])
                colourstart += 1
                # print ("colour1start 2nd loop" + str(colour1start))

                if colourstart >= 30:
                    break
        strip.show()
        time.sleep(0.5)
        strip.clear()
        # loop around again


def chaseRandomPixels(loops, tail, colourA, colourB):
    strip.clear()
    strip.setBrightness(125)
    start = random.randint(3, 10)
    print ("starting at" + str(start))
    chaser = random.randint(0, 3)
    print ("chaser is " + str(chaser))
    # start is always between 5 and 10 pixels in.
    # chaser starts at between 0 and 5
    while True:
        for s in range(3):
            strip.setPixelColor(start, colourA[1], colourA[2], colourA[3])
            print("start was " + str(start))
            start += 1
            # increment
            strip.show()
            time.sleep(0.1)

            # if this is 0, we clear the tail out the chase.
            if tail == 0:
                for t in range(chaser):
                    strip.setPixelColor(t, 0, 0, 0)
                strip.show()

        # now start the chaser at zero, with a max of 5 pixels
        for c in range(3):
            strip.setPixelColor(chaser, colourB[1], colourB[2], colourB[3])
            # increament by 1
            print ("Chaser was " + str(chaser))
            chaser += 1
            strip.show()
            time.sleep(0.2)

        if chaser > 30:
            break


# not a cool as firsst thought - taken out of demo
def setRandomPixels():
    # set all the pixels to a base colour
    strip.clear()

    # now randomise them with other colours
    for r in random.sample(xrange(30), random.randrange(0, 30)):
        strip.setPixelColor(r, random.randrange(0, 175), random.randrange(0, 175), random.randrange(0, 175))
        print("random pixel set " + str(r))
        strip.show()
    flashLights(0.3)


def setAllPixels(colour):
    strip.clear()
    for p in range(numpixels):
        strip.setPixelColor(p, colour[1], colour[2], colour[3])
    strip.setBrightness(125)
    strip.show()


def splitPixels(l, colour):
    for sl in range(l):
        setAllPixels(colour)
        strip.show()

        midLeft = 14
        midRight = 15

        for p in range(15):
            strip.setPixelColor(midLeft, 0, 0, 0)
            strip.setPixelColor(midRight, 0, 0, 0)
            midLeft -= 1
            midRight += 1
            # mini sleep before showing
            time.sleep(0.1)
            strip.show()


# this always increases by 50, 100, 150, 200, 250
def flashLights(duration):
    brightness = 50
    # now play with the brigthness,on and off flashing
    for f in range(5):
        print("flashing..." + str(brightness))
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(duration)
        brightness += 50


def chasePixels(loops, mid, tail, colourA, colourB):
    headerPix = 0
    strip.setBrightness(125)
    # to get the flash effect, need to set them up, then show, then clear, then show
    for p in range(loops):

        strip.setPixelColor(headerPix, colourA[1], colourA[2], colourA[3])
        strip.setPixelColor(mid, colourB[1], colourB[2], colourB[3])
        strip.setPixelColor(tail, 0, 0, 0)

        headerPix += 1
        mid += 1
        tail += 1

        if (headerPix == numpixels):
            headerPix = 0
        if (mid == numpixels):
            mid = 0
        if (tail == numpixels):
            tail = 0

        strip.show()
        time.sleep(1.0 / 50)
        # end of the chasePixels


def setInbetween(wait):
    strip.clear()

    for i in range(numpixels):
        strip.setPixelColor(i, 0, 0, 0)

    strip.setPixelColor(numpixels - 1, 100, 100, 100)
    strip.setPixelColor(numpixels - 1, 100, 100, 100)
    strip.show()
    print("about to wait")
    time.sleep(wait)

# start playing with the flashy lights now.


# print("rainbow")
rainbow()
# setAllPixels(getColour("orange"))
print("testing battery life")

while True:
    strip.clear()
    time.sleep(1)
    setAllPixels(getColour("red"))
    flashLights(0.5)
    strip.clear()
    strip.show()
    time.sleep(10)


#work out how many pixels there is
numpixels = getNumpixels()  # Number of LEDs in strip

# initate the strip
strip.begin()  # Initialize pins for output
strip.setBrightness(50)  # Limit brightness to ~1/4 duty cycle
strip.clear()

#configure the strip

strip = Adafruit_DotStar(numpixels, 6000000, order='gbr')

# setInbetween(5)
# chasePixels(120, -10, -20, getColour("orange"), getColour("light blue"))

# print("ticktock blue - red")
# ticktock red and blue 3 pixels, 5 loops
# ticktock(3, 5, getColour("red"), getColour("blue"))

# setInbetween(5)
# ticktock(5, 5, getColour("red"), getColour("blue"))

# setInbetween(10)
# print("split pixels - red")
# Red
# splitPixels(2, getColour("red"))

# setInbetween(10)
# blue
# print("split pixels - blue")
# splitPixels(2, getColour("blue"))

# print(" transition -chasePixels - red - green")
# setInbetween(10)
# chasePixels(120, -5, -10, getColour("red"), getColour("green"))

# setInbetween(10)
# blue
# print("should be blue")
# setAllPixels(getColour("blue"))
# print("now flash")
# flashLights(0.2)

# setInbetween(10)

# red
# print("all red")
# setAllPixels(getColour("red"))
# print("flash")
# flashLights(0.2)


# setAllPixels(getColour("acqua"))
# flashLights(0.1)
# setAllPixels(getColour("purple"))
# flashLights(0.1)
# setAllPixels(getColour("pink"))
# flashLights(0.1)
# setAllPixels(getColour("blue"))
# flashLights(0.1)

# set it to standby
# setInbetween(10)
# print("chasePixels red and blue")
# chase random pixles, with tail (Red 175, 0, 0) and blue (0,175,0)
# chaseRandomPixels(5, 1, getColour("red"), getColour("blue"))

