# Script to detect, open and convert .ply files to image files with slices at given altitude from the ply mesh.
# Written by Paul Asquin paul.asquin@gmail.com for Awabot Intelligence, 2018

from plyfile import PlyData
import sys
import numpy as np
import io
from tools import *

LES_ALTITUDES = [0.4, 0.5, 0.7]  # Altitudes around which the section will be taken
SECTION_HEIGHT = 0.04  # A section is 4 cm high
IMG_FOLDER = relative_to_absolute_path("../Datasets/JPG")
PLY_FOLDER = relative_to_absolute_path("../Datasets/Scannet_PLY")
LABEL_FOLDER = "Scannet_IDs"
IMG_SIZE = 500


def getLabels():
    """ Get label names by looking à .txt files in the main folder """
    parentPath = os.getcwd()
    # Go to subfolder labels
    os.chdir(LABEL_FOLDER)
    # Get file names
    brut = os.listdir()
    # Go back to parent folder
    os.chdir(parentPath)
    lesLabels = []
    for b in brut:
        if '.txt' in b:
            lesLabels.append(b.replace(".txt", ""))
    return lesLabels


def filepathImage(filepath, label, suffix="", folderName="", extension="jpg"):
    """ Generate the path name for the image, default folder name is label.title()
    A suffix can be indicated to indicate, for example, the altitude level """
    if folderName == "":
        folderName = label.title()
    if suffix != "":
        suffix = "-" + suffix
    sceneId = filepath.split("/")[-2]
    path = IMG_FOLDER + "/" + folderName + "/" + sceneId + suffix + "." + extension

    return path

def extractPoints(pathToPly):
    print("Opening " + pathToPly + " this may take a while...", end="")
    sys.stdout.flush()
    plydata = PlyData.read(pathToPly)
    print(" - Done !")
    return plydata['vertex']

def generateImage(filepath, lesAltitudes, sectionWidth, label):
    """ Treat information to use of given .ply file to generate image at given altitudes with given sectionWidth
    A label have to be indicated to precise if the file is a Kitchen, a bathroom, etc """
    try:
        with open(IMG_FOLDER + "/out.log", 'r') as f:
            if filepath in f.read():
                print(filepath + " already treated")
                return 0

    except FileNotFoundError:
        print("No out.log file yet")

    sectionsDownUp = computeSections(lesAltitudes=lesAltitudes, sectionWidth=sectionWidth)
    lesPoints = extractPoints(pathToPly=filepath)
    slices, extrema = getSlices(lesPoints, sectionsDownUp=sectionsDownUp)
    for i in range(len(lesAltitudes)):
        # Try to export and detect error
        if exportSlice(slice=slices[i], extrema=extrema, label=label,
                       path=filepathImage(filepath=filepath, label=label, suffix=str(lesAltitudes[i]),
                                          extension="jpg"), imageFolder=IMG_FOLDER, width=IMG_SIZE, height=IMG_SIZE) != 0:
            print("Error with export of " + str(label) + " altitude " + str(lesAltitudes[i]))
            # log error
            with open(IMG_FOLDER + "/error.log", 'a') as f:
                try:
                    if filepath not in f.read():
                        f.write(filepath + "\n")
                except io.UnsupportedOperation:
                    f.write(filepath + "\n")
            return 1

    # Write to out.log
    with open(IMG_FOLDER + "/out.log", 'a') as f:
        f.write(filepath + "\n")


def main():
    # Create image directory if it doesn't exist yet
    createFolder(IMG_FOLDER)
    for label in getLabels():
        paths = locate_files(extension="_vh_clean_2.ply", dbName=label + "_plyfiles",
                             path=PLY_FOLDER + "/" + label.title())
        print("\n--- " + label + " : " + str(len(paths)) + " ---")
        for i in range(len(paths)):
            print("\n" + str(i + 1) + "/" + str(len(paths)) + " " + str(label))
            generateImage(filepath=paths[i], lesAltitudes=LES_ALTITUDES, sectionWidth=SECTION_HEIGHT, label=label)
    return 0


if __name__ == "__main__":
    main()
