#!/usr/bin/python3
# Script to detect, open and convert .ply files to image files, slices at regular altitude from the ply mesh.
# Written by Paul Asquin - paul.asquin@gmail.com - Summer 2018
from __future__ import print_function
from plyfile import PlyData  # , PlyElement
import numpy as np
import io
import sys
from tools import *

LES_ALTITUDES = [0.2, 0.3, 0.4, 0.5, 0.7, 0.8, 0.9, 1]  # Altitudes around which the section will be taken
SECTION_HEIGHT = 0.02  # A section is 2 cm high
IMAGE_FOLDER = "../Datasets/JPG"
PLY_FOLDER = "../Datasets/HOUSE_SEGMENTATION"
IMAGE_SIZE = 256
LES_LABELS = [
    ["a", "bathroom"],
    ["b", "bedroom"],
    ["k", "kitchen"],
    ["l", "living"]]


def getMetas(pathToHouse):
    """ Read and return metadatas from given house files corresponding to a label in LES_LABELS """
    print("Opening " + pathToHouse.split("/")[-1])
    lesMeta = []
    lesCorrespLabel = []
    with open(pathToHouse, 'r') as f:
        for line in f:
            ligneProcess = line.replace(" \n", "").split("  ")

            for label in LES_LABELS:
                if ligneProcess[0] == 'R' and ligneProcess[3] == label[0]:
                    print("\tFound a " + label[1] + " !")
                    lesMeta.append(ligneProcess)
                    lesCorrespLabel.append(label[1])
    return lesMeta, lesCorrespLabel


def extractRoom(lesMeta, pathToPly):
    """ Extract points from PLY files with use of metadatas.
    Vectorized implementation """
    lesBoundsBox = []
    lesRoomPly = []
    for meta in lesMeta:
        print("Creating bounds boxes")
        # Get bounds values
        val_p = meta[4].split(" ")
        val_lo = meta[5].split(" ")
        val_hi = meta[6].split(" ")

        # Write value to BoundsBox object
        lesBoundsBox.append(
            BoundsBox(
                Point(float(val_p[0]), float(val_p[1]), float(val_p[2])),
                Point(float(val_lo[0]), float(val_lo[1]), float(val_lo[2])),
                Point(float(val_hi[0]), float(val_hi[1]), float(val_hi[2]))
            )
        )

    print("Opening " + pathToPly + " this may take a while...", end="")
    sys.stdout.flush()
    plydata = PlyData.read(pathToPly)
    print(" - Done !")
    print("Extracting rooms...")
    for k, boundsBox in enumerate(lesBoundsBox):
        print("\tRoom " + str(k + 1) + "/" + str(len(lesBoundsBox)), end="")
        sys.stdout.flush()
        lessLoX = plydata['vertex'][np.where(boundsBox.lo.x <= plydata['vertex']['x'])]
        lessHiX = lessLoX[np.where(lessLoX['x'] <= boundsBox.hi.x)]
        lessLoY = lessHiX[np.where(boundsBox.lo.y <= lessHiX['y'])]
        lessHiY = lessLoY[np.where(lessLoY['y'] <= boundsBox.hi.y)]
        lessLoZ = lessHiY[np.where(boundsBox.lo.z <= lessHiY['z'])]
        lessHiZ = lessLoZ[np.where(lessLoZ['z'] <= boundsBox.hi.z)]
        print(" - " + str(len(lessHiZ)) + " points")
        lesRoomPly.append(lessHiZ)
    return lesRoomPly


def generateImage(pathToPly, pathToHouse):
    """ Treat information to use of given .ply file to generate images at given altitudes with given sectionWidth """
    try:
        with open(IMAGE_FOLDER + "/house_out.log", 'r') as f:
            if pathToHouse in f.read():
                print(" - already treated")
                return 0
            else:
                print("")
    except FileNotFoundError:
        print("No house_out.log file yet")
    lesMeta, lesCorrespLabel = getMetas(pathToHouse=pathToHouse)
    lesRoomPly = extractRoom(lesMeta=lesMeta, pathToPly=pathToPly)
    i = 0
    while i < len(lesRoomPly):
        try:
            lenRoom = len(lesRoomPly[i])
        except TypeError:
            lenRoom = 0
        if lenRoom == 0:
            print("Room " + str(i + 1) + "/" + str(len(lesRoomPly)) + " - " + lesCorrespLabel[i] + " is empty")
            lesRoomPly.pop(i)
            lesCorrespLabel.pop(i)
        else:
            i += 1
    sectionsDownUp = computeSections(lesAltitudes=LES_ALTITUDES, sectionWidth=SECTION_HEIGHT)
    for k, roomPly in enumerate(lesRoomPly):
        slices, extrema = getSlices(roomPly, sectionsDownUp=sectionsDownUp)
        for i in range(len(LES_ALTITUDES)):
            # Try to export and detect error
            if exportSlice(
                    slice=slices[i],
                    extrema=extrema,
                    label=lesCorrespLabel[k],
                    path=filepathImage(
                        pathToPly=pathToPly,
                        label=lesCorrespLabel[k],
                        prefix=str(k) + "-" + lesCorrespLabel[k],
                        suffix=str(LES_ALTITUDES[i]),
                        extension="jpg",
                        imgFolder=IMAGE_FOLDER),
                    width=IMAGE_SIZE,
                    height=IMAGE_SIZE,
                    imageFolder=IMAGE_FOLDER) != 0:
                print("Error with export of " + str(lesCorrespLabel[k]) + " altitude " + str(LES_ALTITUDES[i]))
                # log error
                with open(IMAGE_FOLDER + "/house_error.log", 'a') as f:
                    try:
                        if pathToHouse not in f.read():
                            f.write(pathToHouse + "\n")
                    except io.UnsupportedOperation:
                        f.write(pathToHouse + "\n")
                return -1  # Send back we have an error
    # Write to out.log
    with open(IMAGE_FOLDER + "/house_out.log", 'a') as f:
        f.write(pathToHouse + "\n")


def main():
    # Create image directory if it doesn't exist yet
    createFolder(IMAGE_FOLDER)

    # Load files and sort the names
    lesPlyPath = locate_files(
        extension=".ply",
        dbName="plyfiles",
        path=relative_to_absolute_path(PLY_FOLDER))
    lesPlyPath.sort()
    lesHousePath = locate_files(
        extension=".house",
        dbName="housefiles",
        path=relative_to_absolute_path(PLY_FOLDER))
    lesHousePath.sort()

    for i in range(len(lesPlyPath)):
        print("\nHouse " + str(i + 1) + "/" + str(len(lesPlyPath)) + " : " + lesHousePath[i], end="")
        sys.stdout.flush()
        generateImage(
            pathToPly=lesPlyPath[i],
            pathToHouse=lesHousePath[i])
    return 0


if __name__ == "__main__":
    main()
