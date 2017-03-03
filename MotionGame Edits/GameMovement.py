#!/usr/bin/env python2
#
# OpenCV Python reference: http://opencv.willowgarage.com/documentation/python/index.html

import cv
import time
import Key
import random

class Target:
    """ Class representing the target """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.speed = (0,1)
        #If ball hasn't been touched yet
        self.active = True

    def getDimensions(self):
        return (self.x, self.y, self.width, self.height)

    def centerOrigin(self):
        return (self.x - self.width/2, self.y - self.height/2)

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

# Create windows to show the captured images
#cv.NamedWindow("window_a", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("window_b", cv.CV_WINDOW_AUTOSIZE)

# Structuring element
#Create an circle and puts it on the screen at postiion (4,4)
es = cv.CreateStructuringElementEx(9,9, 4,4, cv.CV_SHAPE_ELLIPSE)


## Webcam settings
# Use default webcam.
# If that does not work, try 0 as function's argument
cam = cv.CaptureFromCAM(-1)
# Dimensions of player's webcam
frame_size = (int(cv.GetCaptureProperty(cam, cv.CV_CAP_PROP_FRAME_WIDTH)),int(cv.GetCaptureProperty(cam, cv.CV_CAP_PROP_FRAME_HEIGHT)))

#Create image of size 'frame_size'
previous = cv.CreateImage(frame_size, 8L, 3)
#Possiblity clears the image
cv.SetZero(previous)

difference = cv.CreateImage(frame_size, 8L, 3)
cv.SetZero(difference)

current = cv.CreateImage(frame_size, 8L, 3)
cv.SetZero(current)

#Resize gives the src image specs such as height and width
bola_original = cv.LoadImage("Aqua-Ball-Red-icon.png")
bola = cv.CreateImage((100,100), bola_original.depth, bola_original.channels)
cv.Resize(bola_original, bola)

bolaG_original = cv.LoadImage("Aqua-Ball-Green-icon.png")
bolaG = cv.CreateImage((100,100), bolaG_original.depth, bolaG_original.channels)
cv.Resize(bolaG_original, bolaG)

mask_original = cv.LoadImage("input-mask.png")
mask = cv.CreateImage((100,100), mask_original.depth, bola_original.channels)
cv.Resize(mask_original, mask)

#Checks the movement in that of the target
def hit_value(image, target):
    # Get's coordinates for where it needs to go from the target class.
    roi = cv.GetSubRect(image, target.getDimensions())
    return cv.CountNonZero(roi)

def create_targets(count):
    targets = list()
    for i in range(count):
        #Choose random x coordinates for targets to start
        tgt = Target(random.randint(0, frame_size[0]-bola.width), 0)
        tgt.width = bola.width
        tgt.height = bola.height
        targets.append(tgt)

    return targets

#No. of targets and creates the that many targets using the createTarget method
nbolas = 1
targets = create_targets(nbolas)

#Delay at the start of the game
initialDelay = 100

score = 0
#Time
t0 = time.clock()


font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX, 1, 4)

# capture - original footage
# current - blurred footage
# difference - difference frame
# frame - difference frame gray scaled > threshold > dilate | working image
# bola_original - imagem da bola
# bola - imagem da bola menor
# mask_original - Mask image
# mask - Image of the smaller mask
# Main loop
selected = False;

while True:
    # Capture a frame
    capture = cv.QueryFrame(cam)
    cv.Flip(capture, capture, flipMode=1)

    # Difference between frames
    cv.Smooth(capture, current, cv.CV_BLUR, 15,15)
    cv.AbsDiff(current, previous, difference)

    frame = cv.CreateImage(frame_size, 8, 1)
    cv.CvtColor(difference, frame, cv.CV_BGR2GRAY)
    cv.Threshold(frame, frame, 10, 0xff, cv.CV_THRESH_BINARY)
    cv.Dilate(frame, frame, element=es, iterations=3)

#Looks at list of targets



    if initialDelay <= 0:
        for t in targets:
            #You only allowed to let 5 target touch the ground
            if t.active:
                nzero = hit_value(frame, t)
                #If the is NO MOVEMENT in the area of the target, draw next shape
                if nzero < 1000 and selected == False:
                    # Draws the target to screen
                    cv.SetImageROI(capture, t.getDimensions())
                    cv.Copy(bola, capture, mask)
                    cv.ResetImageROI(capture)
                    #t.update()
                    # If the target hits the bottom
                    if t.y + t.height >= frame_size[1]:
                        t.active = False
                        nbolas -= 1
                #If the is move that it HIT
                else:
                    selected = True
                    timeSelected = time.clock();
                    cv.SetImageROI(capture, t.getDimensions())
                    cv.Copy(bolaG, capture, mask)
                    cv.ResetImageROI(capture)


                    #Move faster downwards the more goes
                    #if t.speed[1] < 15:
                        #t.speed = (0, t.speed[1]+1)
                    score += nbolas


        if selected == True:
            selectedTimeElapsed = time.clock() - timeSelected
            print selectedTimeElapsed
            if selectedTimeElapsed > 2:
                selected = False
                t.y = random.randint(0, frame_size[1]-bola.height)
                t.x = random.randint(0, frame_size[0]-bola.width)

    #cv.PutText(capture, "Score: %d" % score, (30,frame_size[1]-30), font, cv.RGB(221,87,122))

    #Time elplased
    timer = time.clock() - t0
    cv.PutText(capture, "Timer: %d" % timer, (30,frame_size[1]-30), font,cv.RGB(221,87,122))
    #cv.ShowImage("window_a", frame)

    cv.ShowImage("window_b", capture)

    previous = cv.CloneImage(current)

    # Exit game if ESC key is pressed
    c = Key.WaitKey(2)
    if c == 27:
        break

    initialDelay -= 1

#Print score to console
print score
