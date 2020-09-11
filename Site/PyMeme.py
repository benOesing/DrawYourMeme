#! /usr/bin/env python
import imageio
import sys
import os
import errno
import time
import marshal
from math import sqrt, log10
from math import pi
from numpy.core.umath import arctan2, rad2deg
from PIL import Image
from random import shuffle
from math import sin, cos, tan, floor, ceil
from time import sleep
from cmath import log

def loadImage():  # You get it.
    print ("LoadImage")
    img = Image.open(inputPath)  # Load the image.
    return img

def initVariables():
    print ("Init")
    args = sys.argv[1:]
    global extraWidth, extraHeight, drawBoarder, style, fps, duration,colorThreshold, inputPath, outputPath, extraStartFrames,extraEndFrames,start_time
    start_time = time.time()
    extraWidth = int(args[0])
    extraHeight = int(args[1])
    drawBoarder = (int(args[2]) == 1)
    style = int(args[3])
    fps = int(args[4])
    duration = int(args[5])
    colorThreshold = int(args[6])
    inputPath = args[7]
    outputPath = args[8]
    extraStartFrames = 5 # <----- Frames added to start (empty)
    extraEndFrames = extraStartFrames # <----- Frames added to end (full picture)
    #print(str(extraWidth) + " "+ str(extraHeight) + " " + str(drawBoarder) + " " + str(style) + " " + str(fps) + " " + str(duration) + " " + str(colorThreshold) + " " + inputPath + " " + outputPath + " " + str(extraStartFrames) + " " + str(extraEndFrames))
    
def binarize(img):  # Binary black/white.
    print ("Binarize")
    gray = img.convert("L")  # Grayscale the image.
    bi = gray.point(lambda x: 0 if x < colorThreshold else 255, '1') 
    # Use the grayscale to turn it black/white.
    # Like this: For every Point(Pixel) if grayscale < 128 => its black, otherwise white.
    return bi

def addSpace(img, colorToAdd):  # Adds a boarder.
    print ("AddSpace")
    size = img.size  # Old size size[0]/size[1].
    new_size = (size[0] + extraWidth, size[1] + extraHeight)  # Add boarder to size.
    bigImg = Image.new("L", new_size, colorToAdd)  # Create a blank image in the given color.
    bigImg.paste(img, (int(extraWidth / 2), int(extraHeight / 2)))  # Add the original image.
    return bigImg

def getSetPixels(img):  # Gets all set(black) pixels.
    print ("GetSetPixels")
    size = img.size  # Get size of image size[0]/size[1].
    listOfPixels = []  # Empty List.
    for x in range(0, size[0] * size[1]):  # For every pixel of the image.
        pixel = img.getpixel((x % size[0], x / size[0]))  # Pixel[x][y] = Pixel[x/size[0]][x/size[0]].
        if(pixel == 0):  # If black pixel.
            listOfPixels.append((x % size[0], x / size[0]))  # Add to list.
    return listOfPixels

def orderSequence(listOfPixels, size, startPoint):
    print ("OrderSequence")
    mid = (size[0] / 2, size[1] / 2)
    if(style == 0):  # Random fade in.
        shuffle(listOfPixels)
        return listOfPixels
    if(style == 1):  # Up.
        return sorted(listOfPixels, key=lambda x: (-x[1], x[0]))
    if(style == 2):  # Right.
        return sorted(listOfPixels, key=lambda x: (x[0], x[1]))
    if(style == 3):  # Down.
        return sorted(listOfPixels, key=lambda x: (x[1], x[0]))
    if(style == 4):  # Left.
        return sorted(listOfPixels, key=lambda x: (-x[0], x[1]))
    if(style == 5):  # Connected flood fill.
        current = []  # Empty list, current pixels.
        out = []  # Empty list, resulting order.
        smallestDistance = size[0]  # Distance between startPoint and any set pixel. Init with "big" number.
        existingStartPoint = None
        setPixels = set()
        while len(listOfPixels) > 0:
            t = listOfPixels.pop()
            d = eulerDistance(t, startPoint)
            if d <= smallestDistance:
                smallestDistance = d
                existingStartPoint = t
            setPixels.add(t)
        current.append(existingStartPoint)
        out.append(current[0])
        while(len(setPixels) > 0):
            currentPoints = len(current)
            for i in range(0, currentPoints):
                p = current[i]
                positions = []  # All orientations.
                positions.append((p[0] + 1, p[1] + 1))
                positions.append((p[0] + 1, p[1]))
                positions.append((p[0], p[1] + 1))
                positions.append((p[0] - 1, p[1] - 1))
                positions.append((p[0] - 1, p[1]))
                positions.append((p[0], p[1] - 1))
                positions.append((p[0] + 1, p[1] - 1))
                positions.append((p[0] - 1, p[1] + 1))
                for pos in positions:
                    if pos in setPixels:
                        current.append(pos)
                        out.append(pos)
                        setPixels.remove(pos)
            for _ in range(0, currentPoints):
                current.pop(0)
            if len(current) == 0:
                smallestDistance = size[0]
                existingStartPoint = None
                for pix in setPixels:
                    d = eulerDistance(pix, out[len(out) - 1])
                    if d <= smallestDistance:
                        smallestDistance = d
                        existingStartPoint = pix
                current.append(pix)
                setPixels.remove(pix)
        return out
    if(style == 6):  # Connected depth fill.
        current = []  # Empty list, current pixels.
        out = []  # Empty list, resulting order.
        smallestDistance = size[0]  # Distance between startPoint and any set pixel. Init with "big" number.
        existingStartPoint = None
        setPixels = set()
        while len(listOfPixels) > 0:
            t = listOfPixels.pop()
            d = eulerDistance(t, startPoint)
            if d <= smallestDistance:
                smallestDistance = d
                existingStartPoint = t
            setPixels.add(t)
        current.append(existingStartPoint)
        out.append(current[0])
        while(len(setPixels) > 0):
            p = current[0]
            current.remove(p)
            positions = []  # All orientations.
            positions.append((p[0] + 1, p[1] + 1))
            positions.append((p[0] + 1, p[1]))
            positions.append((p[0], p[1] + 1))
            positions.append((p[0] - 1, p[1] - 1))
            positions.append((p[0] - 1, p[1]))
            positions.append((p[0], p[1] - 1))
            positions.append((p[0] + 1, p[1] - 1))
            positions.append((p[0] - 1, p[1] + 1))
            shuffle(positions)
            for pos in positions:
                if pos in setPixels:
                    current.insert(0, pos)
                    out.append(pos)
                    setPixels.remove(pos)
            if len(current) == 0:
                smallestDistance = size[0]
                existingStartPoint = None
                for pix in setPixels:
                    d = eulerDistance(pix, out[len(out) - 1])
                    if d <= smallestDistance:
                        smallestDistance = d
                        existingStartPoint = pix
                current.append(pix)
                setPixels.remove(pix)
        return out
    if(style == 7):  # CircleOut
        listOfPixels = sorted(listOfPixels, cmp=lambda x, y: circleCompare(x, y, mid))
        return listOfPixels
    if(style == 8):  # CircleIn
        return sorted(listOfPixels, cmp=lambda x, y: circleCompare(x, y, mid), reverse=True)
    if(style / 10 == 9):  # 2d Function
        threshold = 0.01 * size[0] * size[1]  # Percentage of pixels left.
        listOfPixels = set(listOfPixels)
        out = []
        function = style % 10
        lasty = float("inf")
        for startx in range(size[0], -1, -1):
            start = (startx, mid[1])
            for x in range(0, size[0] + 1):
                if x == size[0]:
                    arg = 1
                arg = 2 * pi * (float(x + start[0]) / size[0])
                if function == 0:  # sin
                    y = cos(arg) * mid[1] + start[1]
                elif function == 1:  # cos
                    y = sin(arg) * mid[1] + start[1]
                elif function == 2:  # tan
                    if tan(arg) != 0:
                        y = (1 / tan(arg)) * mid[1] + start[1]
                    else:
                        y = -1
                elif function == 3:  # sawtooth wave
                    y = size[1] - (((x + start[0]) * 2) % (size[1] + 1))
                elif function == 4:  # triangular wave
                    y = 2 / pi * (arg - pi * floor((arg / pi) + (1 / 2))) * (-1) ** (floor(arg / pi) + 1 / 2) * mid[1] + start[1]
                yu = int(ceil(y))
                yu = max(yu, 0)
                yu = min(yu, size[1])
                if abs(yu - lasty) < size[1] / 2:
                    if yu > lasty:
                        for z in range(lasty, yu + 1):
                            if z <= ((yu - lasty) / 2 + lasty):
                                p = (x - 1, z)
                            else:
                                p = (x, z)
                            if p in listOfPixels:
                                out.append(p)
                                listOfPixels.remove(p)
                        lasty = yu
                    else:
                        for z in range(lasty, yu - 1, -1):
                            if z <= ((lasty - yu) / 2 + lasty):
                                p = (x - 1, z)
                            else:
                                p = (x, z)
                            if p in listOfPixels:
                                out.append(p)
                                listOfPixels.remove(p)
                        lasty = yu
                else:
                    lasty = yu
        if len(listOfPixels) != 0:
            percentageOfFail = float(len(listOfPixels)) / (size[0] * size[1])
            roundedPercentageOfFail = (round(percentageOfFail, int(floor(abs(log10(percentageOfFail)))) + 1) * 100)
            out.extend(listOfPixels)
            print ("Error:", str(roundedPercentageOfFail) + "%")
        #saveSequence(out, style, size)
        return out
    else:
        print ("Only 0-8 and [90-94] are valid styles.")
        quit()
        
def saveSequence(sequence, style, size):
    print ("saveSequence")
    newPath = os.path.dirname(outputPath)
    print ("New Path: " + newPath)
    fileName = str(style)+ "_" + str(size[0]) + "x" + str(size[1]) + ".p"
    marshal.dump(sequence, open(newPath + "/Precalculated/" + fileName, "wb"))
    obj = marshal.load(open(newPath + "Precalculated/" + fileName, 'rb'))
    if sequence != obj:
        print ("Saving didnt work, delete ", newPath + "/Precalculated/" + fileName)
        os.remove(newPath + "/Precalculated/" + fileName);
             
def circleCompare(p1, p2, mid):
    d1 = eulerDistance(p1, mid)
    d2 = eulerDistance(p2, mid)
    if(d1 < d2):
        return -1
    elif (d1 > d2):
        return 1
    else:
        a1 = anglePoints(p1, mid)
        a2 = anglePoints(p2, mid)
        if(a1 < a1):
            return -1
        elif (a1 > a2):
            return 1
        else:
            return 0
     
def eulerDistance(x, y):  # ||x-y||
    return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)  # ** = exponent
   
def anglePoints(x, y):  # Angle between two points.
    ang1 = arctan2(x[0],x[1])
    ang2 = arctan2(y[0],y[1])
    arctan2
    return rad2deg((ang1 - ang2) % (2 * pi))
    
def createDirectory():
    try:
        os.makedirs(outputPath)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise  
     
def drawImages(listOfPixels, size):
    print ("DrawImages")
    outList = []  # Empty list.
    out = Image.new("L", (size[0], size[1]), (255))  # Image that gets drawn.
    if(drawBoarder):
        out = addSpace(out, 0)
    for s in range(0,extraStartFrames):
        out.save(outputPath + str(s) + ".png")
    pixelPerFrame = int(len(listOfPixels) / (fps * duration))  # Pixels that gets added per frame.
    for x in range(0, fps * duration):
        for y in range(0, pixelPerFrame):
            pos = listOfPixels[x * pixelPerFrame + y]  # Position of black pixel.
            if(drawBoarder):
                out.putpixel((int(pos[0]+extraWidth/2), int(pos[1]+extraHeight/2)), 0)  # Draw a pixel with offset.
            else:
                out.putpixel((int(pos[0]), int(pos[1])), 0)  # Draw a pixel.
        out.save(outputPath + str(x + extraStartFrames) + ".png")  # Save the file.
    for e in range(0,extraEndFrames):
        out.save(outputPath + str(fps*duration+ e + extraStartFrames) + ".png")
    return outList

def createGif():  # Create Gif from images.
    print ("CreateGif")
    images = []  # Empty list.
    for i in range(0, fps * duration + extraStartFrames + extraEndFrames):  # For every saved image
        images.append(imageio.imread(outputPath + str(i) + ".png"))  # Load all images.
    imageio.mimsave(outputPath + "out.gif", images)  # Create Gif.
  
def moveFile():
    print ("MoveFile")
    fileName = os.path.basename(outputPath)
    if not os.path.isfile("dankmemes/"+fileName+".gif"):
        os.rename(outputPath+"out.gif", "dankmemes/"+fileName+".gif")
    else:
        os.remove("dankmemes/"+fileName+".gif")
        os.rename(outputPath+"out.gif", "dankmemes/"+fileName+".gif") 

def cleanUp():  # Delete Images.
    print ("CleanUp")
    for i in range(0, fps * duration + extraStartFrames + extraEndFrames):  # For every saved image
        os.remove(outputPath + str(i) +".png")
    os.rmdir(outputPath)
  
def main():  # Shit gets done:
    initVariables()
    img = loadImage()
    img = binarize(img)
    setPixels = getSetPixels(img)
    setPixels = orderSequence(setPixels, img.size,(img.size[0]/2,img.size[1]/2))
    createDirectory()
    drawImages(setPixels, img.size)
    createGif()
    moveFile()
    cleanUp()
    print (time.time() - start_time, "seconds")

# Start of Script: 
# Start main
if __name__ == '__main__':
    main()
