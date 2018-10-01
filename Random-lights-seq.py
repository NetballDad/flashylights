#!/usr/bin/python


import time, random, sys
from dotstar import Adafruit_DotStar

# Here's how to control the strip from any two GPIO pins:
datapin = 10
clockpin = 12

numpixels = 0 #which is the therotical max of the Netball ring lights.

#configure the strip

strip = Adafruit_DotStar(numpixels, 6000000, order='gbr')

# red, blue, green
colourArray = [["red", 255, 0, 0],
               ["orange", 255, 0, 128],
               ["yellow", 255, 0, 255],
               ["light-green", 128, 0, 255],
               ["green", 0, 0, 255],
               ["teal", 0, 128, 255],
               ["acqua", 0, 255, 255],
               ["light-blue", 0, 255, 128],
               ["blue", 0, 255, 0],
               ["purple", 128, 255, 0],
               ["light-purple", 255, 255, 0],
               ["white", 255, 255, 255],
               ["pink", 255, 128, 0]]

def getColour(colour):
    for c in range(len(colourArray)):
        #print(" colour we are looking for is " + colour)
        if colourArray[c][0] == colour:
            return colourArray[c]

def rainbow(timeBetweenColours, coloursInRainbow):
    for c in range(coloursInRainbow):

        strip.clear()
        strip.show()
        time.sleep(timeBetweenColours)
        print(colourArray[c][0])
        for n in range(numpixels):
            strip.setPixelColor(n, colourArray[c][1], colourArray[c][2], colourArray[c][3])
            #no need to sleep
        strip.show()
        time.sleep(timeBetweenColours)


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
            if colourstart >= numpixels:
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

                if colourstart >= numpixels:
                    break
        strip.show()
        time.sleep(0.5)
        strip.clear()
        # loop around again


def chaseRandomPixels(loops, tail, colourA, colourB):
    strip.clear()
    strip.setBrightness(125)
    start = random.randint(5, 10)
    print ("starting at" + str(start))
    chaser = random.randint(0, 5)
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
        for c in range(5):
            strip.setPixelColor(chaser, colourB[1], colourB[2], colourB[3])
            # increament by 1
            print ("Chaser was " + str(chaser))
            chaser += 1
            strip.show()
            time.sleep(0.1)

        if chaser > numpixels:
            break


# not a cool as firsst thought - taken out of demo
def setRandomPixels():
    # set all the pixels to a base colour
    strip.clear()

    # now randomise them with other colours
    for r in random.sample(xrange(numpixels), random.randrange(0, numpixels)):
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

	mid = numpixels/2
        midLeft = mid -1
        midRight = mid

        for p in range(mid):
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
        time.sleep(0.25)
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


# initate the strip
strip.begin()  # Initialize pins for output
strip.setBrightness(50)  # Limit brightness to ~1/4 duty cycle
strip.clear()

##################################################################
# start playing with the flashy lights now - below here.
##################################################################


#grab the colours from the command line arguments
#interesting arg 0 is the file name!!
colourOne = str(sys.argv[1])
colourTwo = str(sys.argv[2])
numpixels = str(sys.argv[3])

for o in sys.argv:

    if sys.argv[1] == "":
        print "missing first colour"
        sys.exit()
    elif sys.argv[2] == "":
        print "missing second colour"
        sys.exit()
    elif sys.argv[2] == "":
        print "missing number of LEDS"
        sys.exit()


lights = random.randint(0, 4)

print("lights is " + str(lights))
# print(colourOne)

if lights == 0:
    splitPixels(3, getColour(colourOne))
elif lights == 1:
    splitPixels(3, getColour(colourTwo))
elif lights == 2:
    ticktock(5, 5, getColour(colourOne), getColour(colourTwo))
elif lights == 3:
    ticktock(10, 5, getColour(colourOne), getColour(colourTwo))
elif lights == 4:
    chasePixels(100, -5, -10, getColour(colourOne), getColour(colourTwo))
elif lights == 5:
    chasePixels(100, -5, -10, getColour(colourTwo), getColour(colourOne))
elif lights == 6:
    chaseRandomPixels(5, 1, getColour(colourOne), getColour(colourTwo))
elif lights == 7:
    chaseRandomPixels(5, 1, getColour(colourTwo), getColour(colourOne))
elif lights ==8:
    rainbow(0.2, 10)

strip.clear()
strip.show()