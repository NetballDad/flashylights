#!/usr/bin/python

# Simple strand test for Adafruit Dot Star RGB LED strip.
# This is a basic diagnostic tool, NOT a graphics demo...helps confirm
# correct wiring and tests each pixel's ability to display red, green
# and blue and to forward data down the line.  By limiting the number
# and color of LEDs, it's reasonably safe to power a couple meters off
# USB.  DON'T try that with other code!

import time, random
from dotstar import Adafruit_DotStar

numpixels = 30 # Number of LEDs in strip

# Here's how to control the strip from any two GPIO pins:
datapin  = 10
clockpin = 12
strip    = Adafruit_DotStar(numpixels, 6000000, order='gbr')

def ticktock(size, loops, aR, aG, aB, bR, bG, bB):
	
	for l in range(loops):
		colourstart = 0

		while True:
			#set the first olours up
			#print("setup first colour")
			for c1 in range(size):
				#print("setting pixel " + str(colourstart))
				strip.setPixelColor(colourstart, aR, aG, aB)
				colourstart += 1
				#print ("colour1start  " + str(colour1start))		
			
			strip.show()
			time.sleep(0.2)
			#set the second colours up
			#print ("setup second colour")
			for c2 in range(size):
				#print("setting second pixel " + str(colourstart))
				strip.setPixelColor(colourstart, bR, bG, bB)
				colourstart +=1
				#print ("colour1start 2nd loop" + str(colour1start))
			strip.show()
			time.sleep(0.2)
			
			#break if we get right around
			if colourstart > 30:
				print("breaking with 1 @" + str(colourstart))
				strip.clear()
				time.sleep(0.2)
				break


def chaseRandomPixels(loops, tail, bR,bG,bB,cR,cG,cB):
	strip.clear()
	strip.setBrightness(125)
	start = random.randint(3,10)
	print ("starting at" + str(start))
	chaser = random.randint(0,3)
	print ("chaser is " + str(chaser))
	#start is always between 5 and 10 pixels in.
	#chaser starts at between 0 and 5
	while True:
		for s in range(3):
			strip.setPixelColor(start, bR, bG, bB)
			print("start was " + str(start))
			start += 1
			#incremen
			strip.show()
			time.sleep(0.1)

			# if this is 0, we clear the tail out the chase.
			if tail == 0: 
				for t in range(chaser):
					strip.setPixelColor(t, 0, 0, 0 )
				strip.show()

		#now start the chaser at zero, with a max of 5 pixels
		for c in range(3):
			strip.setPixelColor(chaser, cR, cG, cB)
			#increament by 1
			print ("Chaser was " + str(chaser))
			chaser += 1
			strip.show()
			time.sleep(0.2)

		if chaser > 30:
			break

#not a cool as firsst thought - taken out of demo
def setRandomPixels():
	#set all the pixels to a base colour
	strip.clear()

	#now randomise them with other colours
	for r in random.sample(xrange(30), random.randrange(0,30)):
		strip.setPixelColor(r, random.randrange(0,175), random.randrange(0,175), random.randrange(0,175))
		print("random pixel set " + str(r))
		strip.show()
	flashLights(0.3)


def setAllPixels(R, G, B):
	strip.clear()
	for p in range(numpixels):
		strip.setPixelColor(p,R, G, B)
	strip.setBrightness(125)
	strip.show()
	

def splitPixels(l, R, G, B):
	
	for sl in range (l):
		setAllPixels(R, G, B)
		strip.show()

		midLeft = 14
		midRight = 15

		for p in  range (15):
			strip.setPixelColor(midLeft, 0,0,0)
			strip.setPixelColor(midRight, 0,0,0)
			midLeft -= 1
			midRight += 1
			#mini sleep before showing
			time.sleep(0.1)
			strip.show()
 


# this always increases by 50, 100, 150, 200, 250
def flashLights (duration):
	brightness = 50
	#now play with the brigthness,on and off flashing
	for f in range(5):
		print("flashing")
		strip.setBrightness(brightness)
		strip.show()
		time.sleep(duration)
		brightness += 50

def chasePixels (loops, mid, tail, R1, B1, G1, R2, B2, G2):  
	headerPix = 0
	strip.setBrightness(125)
	#to get the flash effect, need to set them up, then show, then clear, then show
	for p in range(150):

		strip.setPixelColor(headerPix, R1, B1, G1)
		strip.setPixelColor(mid, R2, B2, G2)
		strip.setPixelColor(tail, 0,0,0)

		headerPix += 1
		mid += 1
		tail += 1
	
		if(headerPix == numpixels): 
			headerPix = 0
		if(mid == numpixels): 
			mid = 0
		if(tail == numpixels): 
			tail = 0

		strip.show()
		time.sleep(1.0/50)
	#end of the chasePixels

def setInbetween(wait):
	strip.clear()
	strip.setPixelColor(0, 25, 25, 25)
	strip.setPixelColor(numpixels - 1, 25, 25, 25)
	strip.show()
	print("about to wait")
	time.sleep(wait)

#begin the happenings

strip.begin()           # Initialize pins for output
strip.setBrightness(50) # Limit brightness to ~1/4 duty cycle
strip.clear()

print("BNA Colours - ticktock")
#ticktock red and blue 3 pixels, 2 loops
ticktock(3, 2, 255, 0, 0, 0, 255, 0)

setInbetween(3)

#Red
splitPixels(2, 175, 0, 0)

setInbetween(3)
#blue
splitPixels(2, 0,0,175)

print(" transition -chasePixels")
setInbetween(3)

chasePixels(120, -10, -20, 0, 0, 255, 255, 0, 0)

print("transition - flash em")
#blue
setAllPixels(0, 225,0)
flashLights(0.1)

setInbetween(3)

#red
setAllPixels(175, 0, 0)
flashLights(0.2)

print("transition - chaseRandomPixels")
#set it to standby
setInbetween(3)

#chase random pixles, with tail (Red 175, 0, 0) and blue (0,175,0)
chaseRandomPixels(5, 1, 175, 0, 0, 0, 200, 0)

#CNA Blue 25, 255, 25
#CNA Maroon 255, 75, 75

strip.clear()
strip.show()
