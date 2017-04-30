#!/usr/bin/env python2
#
# OpenCV Python reference: http://opencv.willowgarage.com/documentation/python/index.html

import cv
import cv2
import Key
import random
import time
import numpy
from PIL import Image, ImageDraw, ImageFont


class Target:
    """ Class representing the target """

    def __init__(self, x, y, ):
        self.x = x
        self.y = y
        self.width = 0
        self.height = frame_size[0]
        self.speed = (0, -1)
        self.colourCode = 0
        # If ball hasn't been touched yet
        self.active = True

    def getDimensions(self):
        return (self.x, self.y, self.width, self.height)

    def centerOrigin(self):
        return (self.x - self.width / 2, self.y - self.height / 2)

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

    def getColourCode(self):
        return self.colourCode

class Targetsb:
    """ Class representing the  bomb """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.speed = (0,5)
        self.active = True

    def getDimensions(self):
        return (self.x, self.y, self.width, self.height)

    def centerOrigin(self):
        return (self.x - self.width/2, self.y - self.height/2)

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

class PrintScore:
    def __init__(self):
        self.score = 0
        self.scoreMask = 0

        self.points = 0

    def update(self):
        # Create image
        size = width, height = 400, 90
        scoreImage = Image.new('RGBA', size)
        scoreMaskImage = Image.new('RGB', size, "black")

        # Add font
        titleFont = ImageFont.truetype("font/fibre-font.otf", 60)
        scoreFont = ImageFont.truetype("font/fibre-font.otf", 118)

        drawScore = ImageDraw.Draw(scoreImage)
        drawScore.text((16, 19), "Score:", font=titleFont, fill=(227, 37, 81))
        drawScore.text((160, -3), str(self.points), font=scoreFont, fill=(2, 157, 175))

        drawMaskScore = ImageDraw.Draw(scoreMaskImage)
        drawMaskScore.text((16, 19), "Score:", font=titleFont, fill=(225, 225, 225))
        drawMaskScore.text((160, -3), str(self.points), font=scoreFont, fill=(225, 225, 225))

        self.score = cv2.cvtColor(numpy.array(scoreImage), cv2.COLOR_RGB2BGR)
        self.score = cv.fromarray(self.score)

        self.scoreMask = cv2.cvtColor(numpy.array(scoreMaskImage), cv2.COLOR_RGB2BGR)
        self.scoreMask = cv.fromarray(self.scoreMask)


class PrintTimer:
    def __init__(self):
        self.timer = 0
        self.timerMask = 0

        self.time = 0

    def update(self):
        # Create image
        size = width, height = 300, 90
        timerImage = Image.new('RGBA', size)
        timerMaskImage = Image.new('RGB', size, "black")

        # Add font
        titleFont = ImageFont.truetype("font/fibre-font.otf", 60)
        scoreFont = ImageFont.truetype("font/fibre-font.otf", 118)

        drawTimer = ImageDraw.Draw(timerImage)
        drawTimer.text((16, 19), "Time:", font=titleFont, fill=(227, 37, 81))
        drawTimer.text((160, -3), str(self.time), font=scoreFont, fill=(2, 157, 175))

        drawMaskTimer = ImageDraw.Draw(timerMaskImage)
        drawMaskTimer.text((16, 19), "Time:", font=titleFont, fill=(225, 225, 225))
        drawMaskTimer.text((160, -3), str(self.time), font=scoreFont, fill=(225, 225, 225))

        # Create CV image
        self.timer = cv2.cvtColor(numpy.array(timerImage), cv2.COLOR_RGB2BGR)
        self.timer = cv.fromarray(self.timer)

        self.timerMask = cv2.cvtColor(numpy.array(timerMaskImage), cv2.COLOR_RGB2BGR)
        self.timerMask = cv.fromarray(self.timerMask)


class PrintEnding:
    def __init__(self,points):
        self.ending = 0
        self.endingMask = 0
        self.point = points

    def update(self):
        # Create image
        size = width, height = 600, 450
        endingImage = Image.new('RGBA', size)
        endingMaskImage = Image.new('RGB', size, "black")

        # Add font
        titleFont = ImageFont.truetype("font/fibre-font.otf", 140)
        scoreFont = ImageFont.truetype("font/fibre-font.otf", 200)

        drawEnding = ImageDraw.Draw(endingImage)
        drawEnding.text((12, 36), "You Scored", font=titleFont, fill=(227, 37, 81))
        drawEnding.text((200, 135), str(self.point), font=scoreFont, fill=(2, 157, 175))

        drawMaskEnding = ImageDraw.Draw(endingMaskImage)
        drawMaskEnding.text((12, 36), "You Scored", font=titleFont, fill=(225, 225, 225))
        drawMaskEnding.text((200, 135), str(self.point), font=scoreFont, fill=(225, 225, 225))

        self.ending = cv2.cvtColor(numpy.array(endingImage), cv2.COLOR_RGB2BGR)
        self.ending = cv.fromarray(self.ending)

        self.endingMask = cv2.cvtColor(numpy.array(endingMaskImage), cv2.COLOR_RGB2BGR)
        self.endingMask = cv.fromarray(self.endingMask)


# Create windows to show the captured images
# cv.NamedWindow("window_a", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("Balloon Up - Motion", cv.CV_WINDOW_NORMAL)



# cv.NamedWindow("window_a", cv.CV_WINDOW_AUTOSIZE)

# Structuring element
# Create an circle and puts it on the screen at postiion (4,4)
es = cv.CreateStructuringElementEx(9, 9, 4, 4, cv.CV_SHAPE_ELLIPSE)

## Webcam settings
# Use default webcam.
# If that does not work, try 0 as function's argument
cam = cv.CaptureFromCAM(-1)
# Dimensions of player's webcam
frame_size = (int(cv.GetCaptureProperty(cam, cv.CV_CAP_PROP_FRAME_WIDTH)),
              int(cv.GetCaptureProperty(cam, cv.CV_CAP_PROP_FRAME_HEIGHT)))

# Create image of size 'frame_size'
previous = cv.CreateImage(frame_size, 8L, 3)
# Possiblity clears the image
cv.SetZero(previous)

difference = cv.CreateImage(frame_size, 8L, 3)
cv.SetZero(difference)

current = cv.CreateImage(frame_size, 8L, 3)
cv.SetZero(current)









#IMPORT ALL IMAGES

# Resize gives the src image specs such as height and width
balloonMask_Image = cv.LoadImage("images/balloonMask.png")
balloonMask = cv.CreateImage((64, 105), balloonMask_Image.depth, balloonMask_Image.channels)
cv.Resize(balloonMask_Image, balloonMask)

# Different colour balloons
balloonGreen_Image = cv.LoadImage("images/balloonGreen.png")
balloonGreen = cv.CreateImage((64, 105), balloonGreen_Image.depth, balloonGreen_Image.channels)
cv.Resize(balloonGreen_Image, balloonGreen)

balloonBlue_Image = cv.LoadImage("images/balloonBlue.png")
balloonBlue = cv.CreateImage((64, 105), balloonBlue_Image.depth, balloonBlue_Image.channels)
cv.Resize(balloonBlue_Image, balloonBlue)

balloonPink_Image = cv.LoadImage("images/balloonPink.png")
balloonPink = cv.CreateImage((64, 105), balloonPink_Image.depth, balloonPink_Image.channels)
cv.Resize(balloonPink_Image, balloonPink)

balloonOrange_Image = cv.LoadImage("images/balloonOrange.png")
balloonOrange = cv.CreateImage((64, 105), balloonOrange_Image.depth, balloonOrange_Image.channels)
cv.Resize(balloonOrange_Image, balloonOrange)

balloonYellow_Image = cv.LoadImage("images/balloonYellow.png")
balloonYellow = cv.CreateImage((64, 105), balloonYellow_Image.depth, balloonYellow_Image.channels)
cv.Resize(balloonYellow_Image, balloonYellow)

balloons = [balloonGreen, balloonBlue, balloonOrange, balloonPink, balloonYellow]

bombMaskImage = cv.LoadImage("images/bombMask.png")
bombMask = cv.CreateImage((75, 75), bombMaskImage.depth, bombMaskImage.channels)
cv.Resize(bombMaskImage, bombMask)

bombImage = cv.LoadImage("images/bomb.png")
bomb = cv.CreateImage((75, 75), bombImage.depth, bombImage.channels)
cv.Resize(bombImage, bomb)

startMaskImage = cv.LoadImage("images/startMask.png")
startMask = cv.CreateImage((600, 450), startMaskImage.depth, startMaskImage.channels)
cv.Resize(startMaskImage, startMask)

startImage = cv.LoadImage("images/start.png")
start = cv.CreateImage((600, 450), startImage.depth, startImage.channels)
cv.Resize(startImage, start)

readyImage = cv.LoadImage("images/ready.png")
ready = cv.CreateImage((600, 450), readyImage.depth, readyImage.channels)
cv.Resize(readyImage, ready)

readyMaskImage = cv.LoadImage("images/readyMask.png")
readyMask = cv.CreateImage((600, 450), readyMaskImage.depth, readyMaskImage.channels)
cv.Resize(readyMaskImage, readyMask)

setImage = cv.LoadImage("images/set.png")
set = cv.CreateImage((600, 450), setImage.depth, setImage.channels)
cv.Resize(setImage, set)

setMaskImage = cv.LoadImage("images/setMask.png")
setMask = cv.CreateImage((600, 450), setMaskImage.depth, setMaskImage.channels)
cv.Resize(setMaskImage, setMask)

popImage = cv.LoadImage("images/pop.png")
pop = cv.CreateImage((600, 450), popImage.depth, popImage.channels)
cv.Resize(popImage, pop)

popMaskImage = cv.LoadImage("images/popMask.png")
popMask = cv.CreateImage((600, 450), popMaskImage.depth, popMaskImage.channels)
cv.Resize(popMaskImage, popMask)








#Hit targets

# Checks the movement in that of the target
def hit_value(image, target):
    # Get's coordinates for where it needs to go from the target class.
    roi = cv.GetSubRect(image, target.getDimensions())
    return cv.CountNonZero(roi)


def create_targets(count):
    targets = list()
    for i in range(count):
        # Choose random x coordinates for targets to start
        tgt = Target(random.randint(0, frame_size[0] - balloonMask.width), frame_size[1] - balloonMask.height)
        tgt.width = balloonMask.width
        tgt.height = balloonMask.height
        tgt.colourCode = random.randrange(0, 5, 1)
        targets.append(tgt)

    return targets

def create_targetsb(count):
    targetsb = list()
    for j in range(count):
        tgtb = Targetsb(random.randint(0, frame_size[0]-bomb.width), 0)
        tgtb.width = bomb.width
        tgtb.height = bomb.height
        targetsb.append(tgtb)

    return targetsb


# capture - original footage
# current - blurred footage
# difference - difference frame
# frame - difference frame gray scaled > threshold > dilate | working image
# ball_original - imagem da ball
# ball - imagem da ball menor
# mask_original - Mask image
# mask - Image of the smaller mask
# Main loop
def gameIntro(previous):
    start_intro = False
    initialDelay = 75

    while True:

        # Capture a frame
        capture = cv.QueryFrame(cam)
        cv.Flip(capture, capture, flipMode=1)

        # Difference between frames
        cv.Smooth(capture, current, cv.CV_BLUR, 15, 15)
        cv.AbsDiff(current, previous, difference)

        frame = cv.CreateImage(frame_size, 8, 1)
        cv.CvtColor(difference, frame, cv.CV_BGR2GRAY)
        cv.Threshold(frame, frame, 10, 0xff, cv.CV_THRESH_BINARY)
        cv.Dilate(frame, frame, element=es, iterations=3)

        # Start Screen
        if start_intro is False:
            cv.SetImageROI(capture, ((frame_size[0] / 2) - 300, (frame_size[1] / 2) - 225, 600, 450))
            cv.Copy(start, capture, startMask)
            cv.ResetImageROI(capture)

            # Press space bar to run game
            if cv2.waitKey(33) is 32:
                start_intro = True

        # Ready Set POP to start the game
        if (75 > initialDelay > 50):
            cv.SetImageROI(capture, ((frame_size[0] / 2) - 300, (frame_size[1] / 2) - 225, 600, 450))
            cv.Copy(ready, capture, readyMask)
            cv.ResetImageROI(capture)

        if (50 > initialDelay > 25):
            cv.SetImageROI(capture, ((frame_size[0] / 2) - 300, (frame_size[1] / 2) - 225, 600, 450))
            cv.Copy(set, capture, setMask)
            cv.ResetImageROI(capture)

        if (25 > initialDelay > 0):
            cv.SetImageROI(capture, ((frame_size[0] / 2) - 300, (frame_size[1] / 2) - 225, 600, 450))
            cv.Copy(pop, capture, popMask)
            cv.ResetImageROI(capture)

        if (initialDelay is 0):
            break;

        if start_intro is True:
            initialDelay -= 1

        cv.ShowImage("Balloon Up - Motion", capture)
        previous = cv.CloneImage(current)

        # Exit game if ESC key is pressed
        c = Key.WaitKey(2)



def startPlaying(previous):
    # No. of targets and creates the that many targets using the createTarget method
    nballs = 5
    nbombs = 1
    targets = create_targets(nballs)
    targetsb = create_targetsb(nbombs)

    myScore = PrintScore()

    myTimer = PrintTimer()
    start_time = time.clock()
    game_duration = 30

    while True:
        # Capture a frame
        capture = cv.QueryFrame(cam)
        cv.Flip(capture, capture, flipMode=1)

        # Difference between frames
        cv.Smooth(capture, current, cv.CV_BLUR, 15, 15)
        cv.AbsDiff(current, previous, difference)

        frame = cv.CreateImage(frame_size, 8, 1)
        cv.CvtColor(difference, frame, cv.CV_BGR2GRAY)
        cv.Threshold(frame, frame, 10, 0xff, cv.CV_THRESH_BINARY)
        cv.Dilate(frame, frame, element=es, iterations=3)

        for t in targets:
            # You only allowed to let 5 target touch the ground
            if t.active:
                nzero = hit_value(frame, t)
                # If the is NO MOVEMENT in the area of the target, draw next shape
                if nzero < 6500:
                    # Draws the target to screen
                    cv.SetImageROI(capture, t.getDimensions())
                    colour = t.getColourCode()
                    cv.Copy(balloons[colour], capture, balloonMask)
                    cv.ResetImageROI(capture)
                    t.update()
                    # If the target hits the bottom
                    if t.y <= 0:
                        t.y = frame_size[1] - balloonMask.height
                        t.x = random.randint(0, frame_size[0] - balloonMask.width)
                        t.speed = (0, t.speed[1] - 1)
                # If the is balloon it hit
                else:
                    t.y = frame_size[1] - balloonMask.height
                    t.x = random.randint(0, frame_size[0] - balloonMask.width)
                    t.speed = (0, t.speed[1] - 1)
                    # Change colour of balloon
                    t.colourCode = random.randrange(0, 5, 1)

                    # Move faster downwards the more goes
                    if t.speed[1] < 15:
                        t.speed = (0, t.speed[1] - 2)
                    myScore.points += 1

        for l in targetsb:
            if l.active:
                nzero = hit_value(frame, l)
                if nzero < 5500:
                    # Draws the target to screen
                    cv.SetImageROI(capture, l.getDimensions())
                    cv.Copy(bomb, capture, bombMask)
                    cv.ResetImageROI(capture)
                    l.update()
                    # If the target hits the bottom
                    if l.y + l.height >= frame_size[1]:
                        l.y = 0
                        l.x = random.randint(0, frame_size[0] - bomb.width)
                else:
                    l.y = 0
                    l.x = random.randint(0, frame_size[0]-bomb.width)
                    myScore.points -= 2

        myScore.update()
        myTimer.update()

        myTimer.time = int((game_duration + 1) - (time.clock() - start_time))

        #Print score and Timer
        cv.SetImageROI(capture, (30, (frame_size[1] - 120), 400, 90))
        cv.Copy(myScore.score, capture, myScore.scoreMask)
        cv.ResetImageROI(capture)

        cv.SetImageROI(capture, ((frame_size[0] - 300), (frame_size[1] - 120), 400, 90))
        cv.Copy(myTimer.timer, capture, myTimer.timerMask)
        cv.ResetImageROI(capture)

        if myTimer.time < 0:
            return myScore.points

        # cv.ShowImage("window_a", frame)

        cv.ShowImage("Balloon Up - Motion", capture)

        previous = cv.CloneImage(current)

        # Exit game if ESC key is pressed
        c = Key.WaitKey(2)

        if (c is 27):
            return None

def endScreen(previous, points):
    while True:
        # Capture a frame
        capture = cv.QueryFrame(cam)
        cv.Flip(capture, capture, flipMode=1)

        # Difference between frames
        cv.Smooth(capture, current, cv.CV_BLUR, 15, 15)
        cv.AbsDiff(current, previous, difference)

        frame = cv.CreateImage(frame_size, 8, 1)
        cv.CvtColor(difference, frame, cv.CV_BGR2GRAY)
        cv.Threshold(frame, frame, 10, 0xff, cv.CV_THRESH_BINARY)
        cv.Dilate(frame, frame, element=es, iterations=3)

        credits = PrintEnding(points)
        credits.update()

        cv.SetImageROI(capture, ((frame_size[0] / 2) - 300, (frame_size[1] / 2) - 225, 600, 450))
        cv.Copy(credits.ending, capture, credits.endingMask)
        cv.ResetImageROI(capture)

        c = Key.WaitKey(2)

        if (c is 27):
            return False

        if cv2.waitKey(33) is 32:
            return True

        cv.ShowImage("Balloon Up - Motion", capture)

while True:
    gameIntro(previous)
    points = startPlaying(previous)

    #Handle exiting the program
    if points is None:
        break

    if endScreen(previous, points) is False:
        break


# Print score to console
#print myScore
