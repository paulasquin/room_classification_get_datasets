#!/usr/bin/python3
# General toolbox for the Room Classification Project
# Written by Paul Asquin - paul.asquin@gmail.com - Summer 2018

import os
import sys
import subprocess
import numpy as np
from PIL import Image


class Point:
    x = 0
    y = 0
    z = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y and self.z > other.z

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y and self.z >= other.z


class BoundsBox:
    p = Point(0, 0, 0)
    lo = Point(0, 0, 0)
    hi = Point(0, 0, 0)

    def __init__(self, p, lo, hi):
        self.p = p
        self.lo = lo
        self.hi = hi


def computeSections(lesAltitudes, sectionWidth):
    """ From given altitudes and section width, generate the lower and upper z values of a section.
     The values are taken from alt - width/2 to alt + width/2 """

    sectionsDownUp = []
    for alt in lesAltitudes:
        sectionsDownUp.append([alt - sectionWidth / 2, alt + sectionWidth / 2])
    return sectionsDownUp

def relative_to_absolute_path(path=""):
    """ Send back absolute path if relative was given """
    # Check if not already absolute path
    if path == "":
        path = os.getcwd()
    elif path[0] == ".":
        up = path.count("../")
        path = '/'.join(os.getcwd().split("/")[0:-up]) + "/" + path.replace("../", "")
    elif path[0] != "/":
        path = os.getcwd() + "/" + path
    return path


def locate_files(extension, path=os.getcwd(), dbName="locate"):
    """ Locate files using .db database. May need sudo to write the database"""
    print("\nCreating the database \"" + dbName + ".db\" for the \"local\" command")
    print("Searching " + extension + " in " + path)
    try:
        cmd = "updatedb -l 0 -o " + dbName + ".db -U " + path + "/"
        print(cmd)
        subprocess.call(["echo 'You may need sudo access' &" + cmd], shell=True)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Might be an error in permission to write the locate database."
              " Try to launch the script with \"sudo python\"")
    cmd = "locate -d " + dbName + ".db " + relative_to_absolute_path(path) + "*" + extension
    print(cmd)
    p = subprocess.Popen([cmd],
                         stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    paths = out.decode('utf-8')
    paths = paths.split('\n')
    paths.pop()  # We delete the last, empty, element
    print("Found " + str(len(paths)) + " elements")
    return paths


def createFolder(path):
    """ Create the folder label if not already exists """
    if not os.path.isdir(path):
        print("Creating folder " + str(path))
        os.mkdir(path)
    return 0


def filepathImage(pathToPly, label, imgFolder, prefix="", suffix="", folderName="", extension="jpg", ):
    """ Generate the path name for the image, default folder name is label.title()
    A suffix can be indicated to indicate, for example, the altitude level """
    if folderName == "":
        folderName = label.title()
    if suffix != "":
        suffix = "-" + suffix
    if prefix != "":
        prefix = "-" + prefix
    sceneId = pathToPly.split("/")[-2] + "_" + pathToPly.split("/")[-3]
    path = imgFolder + "/" + folderName + "/" + sceneId + prefix + suffix + "." + extension
    return path

def exportSlice(slice, extrema, path, label, imageFolder, width=500, height=500):
    """ Export an image from given slice. Use of extrema and shape for resolution, label for naming the image """
    resize = slice.copy()
    minX, maxX, minY, maxY, minZ, maxZ = extrema
    # Put values to a [0, width-1]*[0, height-1] domain
    # Minus width to have a "bird like" view (mirror transformation)
    try:
        resize['x'] = (width - 1) - (slice['x'] - minX) * (width - 1) / (maxX - minX)
        resize['y'] = (slice['y'] - minY) * (height - 1) / (maxY - minY)

    except IndexError:
        print("Problem with resize for " + str(path)
              + "\nminX : " + str(minX) + " maxX : " + str(maxX) + " minY : " + str(minY) + " maxY : " + str(maxY)
              + "\nnp.minX : " + str(np.min(resize['x'])) + " np.maxX : " + str(np.max(resize['x'])) + "np.minY : " +
              str(np.min(resize['y'])) + " np.maxY : " + str(np.max(resize['y'])))
        return -1

    # Image initialization to white
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    # Affect coordinates of points to black
    try:
        image[(resize['y'].astype(int), resize['x'].astype(int))] = [0, 0, 0]
    except IndexError:
        print("Problem with resize for " + str(path)
              + "\nminX : " + str(minX) + " maxX : " + str(maxX) + " minY : " + str(minY) + " maxY : " + str(maxY)
              + "\nnp.minX : " + str(np.min(slice['x'])) + " np.maxX : " + str(np.max(slice['x'])) + "np.minY : " +
              str(np.min(slice['y'])) + " np.maxY : " + str(np.max(slice['y'])))
        return -1
    createFolder(imageFolder + "/" + str(label.title()))
    print("\t" + path.split("/")[-1], end="")
    sys.stdout.flush()
    try:
        img = Image.fromarray(image, 'RGB')
        if imageFolder[:3] == "JPG":
            img.save(path, "JPEG", quality=80, optimize=True, progressive=True)
        else:
            img.save(path)
    except KeyboardInterrupt:
        raise
    except:
        print("\n!!! Problem exporting " + path)
        img = Image.fromarray(image, 'RGB')
        img.show()
        return -1
    print(" - exported")
    return 0

def getSlices(lesPoints, sectionsDownUp):
    """ Open lesPoints, read the data and return slices points with extrema
    Vectorized implementation """
    #  Compute min and max values
    minX, minY, minZ, maxX, maxY, maxZ = np.min(lesPoints['x']), np.min(lesPoints['y']), np.min(lesPoints['z']), np.max(
        lesPoints['x']), np.max(lesPoints['y']), np.max(lesPoints['z'])

    # Initialisation of "sliced" section points
    sliced = []
    for k in range(len(sectionsDownUp)):
        downLimit = sectionsDownUp[k][0]
        upLimit = sectionsDownUp[k][1]
        temp = lesPoints[np.where(downLimit <= lesPoints['z'])]
        sliced.append(temp[np.where(temp['z'] <= upLimit)])
    return sliced, [minX, maxX, minY, maxY, minZ, maxZ]


def getExportNumber(modelFolder):
    """ Get the number of the export folder looking at already existing folders
    Handle the presence of '_precisions' at the end of the folder name """

    lesDir = os.listdir(modelFolder)
    lesExport = []
    lesNum = []
    num = 0
    for dir in lesDir:
        if "export_" in dir:
            lesExport.append(dir)
    for i in range(len(lesExport)):
        # Get number of export and add 1 to it
        # If we have an extension in the name
        if lesExport[i][7:].find("_") != -1:
            lesNum.append(int(lesExport[i][7:7 + lesExport[i][7:].find("_")]))
        # If there is not extension
        else:
            lesNum.append(int(lesExport[i][7:]))

    if len(lesNum) != 0:
        num = max(lesNum) + 1

    return num