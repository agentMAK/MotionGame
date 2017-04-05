#!/usr/bin/env python2
#
# OpenCV Python reference: http://opencv.willowgarage.com/documentation/python/index.html

import cv
import cv2
import Key
import random
import time
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


class Score:
    def __init__(self):
        scoreImage = cv.LoadImage("images/score.png")
        self.score = cv.CreateImage((400, 90), scoreImage.depth, scoreImage.channels)
        cv.Resize(scoreImage, self.score)

        scoreMaskImage = cv.LoadImage("images/scoreMask.png")
        self.scoreMask = cv.CreateImage((400, 90), scoreMaskImage.depth, scoreMaskImage.channels)
        cv.Resize(scoreMaskImage, self.scoreMask)

        self.points = 0

    def update(self):
        # Create image
        size = width, height = 400, 90;
        scoreImage = Image.new('RGBA', size)
        scoreMaskImage = Image.new('RGB', size, "black")

        # Add font
        titleFont = ImageFont.truetype("font/fibre-font.otf", 60)
        scoreFont = ImageFont.truetype("font/fibre-font.otf", 118)

        drawScore = ImageDraw.Draw(scoreImage)
        drawScore.text((16, 19), "score:", font=titleFont, fill=(227, 37, 81))
        drawScore.text((160, -3), str(self.points), font=scoreFont, fill=(2, 157, 175))

        drawMaskScore = ImageDraw.Draw(scoreMaskImage)
        drawMaskScore.text((16, 19), "score:", font=titleFont, fill=(225, 225, 225))
        drawMaskScore.text((160, -3), str(self.points), font=scoreFont, fill=(225, 225, 225))

        scoreImage.save("images/score.png")
        scoreMaskImage.save("images/scoreMask.png")

        # Update the file input
        scoreImage = cv.LoadImage("images/score.png")
        self.score = cv.CreateImage((400, 90), scoreImage.depth, scoreImage.channels)
        cv.Resize(scoreImage, self.score)

        scoreMaskImage = cv.LoadImage("images/scoreMask.png")
        self.scoreMask = cv.CreateImage((400, 90), scoreMaskImage.depth, scoreMaskImage.channels)
        cv.Resize(scoreMaskImage, self.scoreMask)



# Create windows to show the captured images
# cv.NamedWindow("window_a", cv.CV_WINDOW_AUTOSIZE)
cv.NamedWindow("window_b", cv.CV_WINDOW_NORMAL)
#cv.NamedWindow("window_a", cv.CV_WINDOW_AUTOSIZE)

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
bombMask = cv.CreateImage((500, 488), bombMaskImage.depth, bombMaskImage.channels)
cv.Resize(bombMaskImage, bombMask)

bombImage = cv.LoadImage("images/bomb.png")
bomb = cv.CreateImage((500, 488), bombImage.depth, bombImage.channels)
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



# capture - original footage
# current - blurred footage
# difference - difference frame
# frame - difference frame gray scaled > threshold > dilate | working image
# ball_original - imagem da ball
# ball - imagem da ball menor
# mask_original - Mask image
# mask - Image of the smaller mask
# Main loop
def startPlaying(previous):

    # No. of targets and creates the that many targets using the createTarget method
    nballs = 5
    targets = create_targets(nballs)

    # Delay at the start of the game
    startGame = False
    endGame = False
    initialDelay = 0
    t0 = -1

    myScore = Score()

    font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX, 1, 4)
    selected = False


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

        # Looks at list of targets
        if startGame == False:
            cv.SetImageROI(capture,((frame_size[0] / 2) - 300, (frame_size[1] / 2) - 225, 600, 450))
            cv.Copy(start, capture, startMask)
            cv.ResetImageROI(capture)

            # Press space bar to run game
            if cv2.waitKey(33) == 32:
                initialDelay = 75
                startGame = True

        # Ready Set POP to start the game
        if(initialDelay>50):
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

        if(initialDelay == 0):
            t0 = time.clock()
            initialDelay -= 1


        if startGame == True and initialDelay <= -1:
           for t in targets:
                # You only allowed to let 5 target touch the ground
                if t.active:
                    nzero = hit_value(frame, t)
                    # If the is NO MOVEMENT in the area of the target, draw next shape
                    if nzero < 1000:
                        # Draws the target to screen
                        cv.SetImageROI(capture, t.getDimensions())
                        colour = t.getColourCode()
                        cv.Copy(balloons[colour], capture, balloonMask)
                        cv.ResetImageROI(capture)
                        t.update()
                        # If the target hits the bottom
                        if t.y <= 0:
                            t.active = False
                            nballs -= 1
                    # If the is balloon it hit
                    else:
                        t.y = frame_size[1]-balloonMask.height
                        t.x = random.randint(0, frame_size[0] - balloonMask.width)
                        t.speed = (0, t.speed[1]-1)
                        # Change colour of balloon
                        t.colourCode = random.randrange(0, 5, 1)

                        # Move faster downwards the more goes
                        if t.speed[1] < 15:
                            t.speed = (0, t.speed[1] - 2)
                        myScore.points += 1

        if startGame == True and initialDelay == -1 and time.clock() - t0 < 60:
            timer = 61 - (time.clock() - t0)
            cv.PutText(capture, "Timer: %d" % timer, (frame_size[0]-500, frame_size[1] - 50), font, cv.RGB(221, 87, 122))

            #Update score every few seconds
            myScore.update()
            cv.SetImageROI(capture, (30, (frame_size[1] - 120), 400, 90))
            cv.Copy(myScore.score, capture, myScore.scoreMask)
            cv.ResetImageROI(capture)
        else:
            timer = -1

        check = (time.clock() - t0)


        if check > 60:
            endGame = True


        # cv.ShowImage("window_a", frame)

        cv.ShowImage("window_b", capture)

        previous = cv.CloneImage(current)

        # Exit game if ESC key is pressed
        c = Key.WaitKey(2)

        if (c == 27 or endGame == True and initialDelay == -1 and timer == -1):
            print "Game ended"
            return (myScore.points)

        if(initialDelay > 0):
            initialDelay -= 1

startPlaying(previous)

while True:

        capture = cv.QueryFrame(cam)
        cv.Flip(capture, capture, flipMode=1)
        c = Key.WaitKey(2)
        if (c == 27):
            break
        cv.ShowImage("window_b", capture)

# Print score to console
#print myScore
