#!/usr/bin/python3
# Process the dataset to clean it and augment it
# Written by Paul Asquin - paul.asquin@gmail.com - Summer 2018

from tools import *
import PIL
import sys

LES_AUGMENTATION = ['width-flip', 'height-flip', 'cwRotate', 'ccwRotate', 'inverse']
DATASET_FOLDER = "../Datasets/JPG"


def cleanDataset(lesImgPath):
    """ Del images that are not present in clean_dataset.txt """
    print("Going to remove every blank-like images (<3ko) + \
        and every room not present in clean_dataset.txt. Are you sure ?")
    print("Press Enter to continue, CTRL+C to exit")
    key = input('')
    print("Removing 'blank-like' images...")
    delBlankImage(lesImgPath)
    print("Removing unreferenced images")
    with open("clean_dataset.txt", "r") as f:
        lesGood = f.read().split("\n")
    for path in lesImgPath:
        # Extract the file name without extension
        name = path.split("/")[-1].replace(".jpg", "")
        if ("scene" in name and name.split("-")[0] not in lesGood) or (
                "segmentations" in name and "-".join(name.split("-")[:3]) not in lesGood):
            # Remove the file if the core name of the file is not indicated in clean_dataset.txt
            print("Removing " + path.split("/")[-1] + " " * 30, end="\r")
            os.remove(path)
        else:
            print("Keeping : " + path + " " * 30, end="\r")
    print("Completed")


def makeCleanDataset(lesImgPath):
    """ Generate the file clean_dataset.txt using the room in the diven dataset path considering every image room presented is ok for you"""
    print("Generating a new clean_dataset.txt file.")
    print("Checking if the file alread exists", end="")
    sys.stdout.flush()
    if os.path.isfile("clean_dataset.txt"):
        print(" : Yes, removing")
        os.remove("clean_dataset.txt")
    else:
        print(" : Not alteady existing")

    print("Writing files name")
    lesGood = []
    with open("clean_dataset.txt", "w") as f:
        for path in lesImgPath:
            name = path.split("/")[-1].replace(".jpg", "")
            # Extracting room name
            if "scene" in name:
                room = name.split("-")[0]  # We get something like 'scene0009_00'
            elif "segmentations" in name:
                room = "-".join(
                    name.split("-")[:3])  #  We get something like 'house_segmentations_17DRP5sb8fy-1-bathroom'
            else:
                print("Error in the name structure of " + path)
                continue
            if room not in lesGood:
                lesGood.append(room)
                f.write(room + "\n")
                print("Saving" + room + " " * 30, end="\r")
    print("Completed")


def delBlankImage(lesImgPath):
    """ Check if given image paths are empty-like (less than 6ko), if yes, they are removed """
    print("Deleting empty-like image (<3ko)")
    for path in lesImgPath:
        if os.path.getsize(path) < 3000:
            print("\tRemoving " + path.split("/")[-1] + " " * 30, end="\r")
            os.remove(path)
            with open("empty_image.txt", "a") as f:
                f.write(path + "\n")
        else:
            print("\tKeeping " + path.split("/")[-1] + " " * 30, end="\r")
    print("Completed")
    return 0


def getAugmentationPath(imgPath, augmentation):
    """ Generate the augmented image path, with given original path and augmentation """
    return imgPath.replace(".jpg", "-" + augmentation + ".jpg")


def notAlreadyAugmented(imgPath, augmentation):
    """ Return False if asked augmentation already exists or if the file is already an augmentation"""
    augPath = getAugmentationPath(imgPath=imgPath, augmentation=augmentation)
    augmented = False
    for aug in LES_AUGMENTATION:
        if "-" + aug in imgPath:
            augmented = True
    return not (os.path.isfile(augPath) or augmented)


def augmentImage(lesImgPath):
    """ Apply augmentation operations defined by LES_AUGMENTATION corresponding to PIL transformations"""
    global LES_AUGMENTATION
    print(', '.join(LES_AUGMENTATION))
    for i, imgPath in enumerate(lesImgPath):
        with PIL.Image.open(imgPath) as img:
            print(str(i=1) + "/" + str(len(lesImgPath)) + " : Augmenting " + imgPath.split("/")[-1], end="\r")
            for augmentation in LES_AUGMENTATION:
                if augmentation == 'width-flip' and notAlreadyAugmented(imgPath=imgPath, augmentation=augmentation):
                    img.transpose(PIL.Image.FLIP_LEFT_RIGHT).save(
                        getAugmentationPath(
                            imgPath=imgPath,
                            augmentation=augmentation)
                    )
                elif augmentation == 'height-flip' and notAlreadyAugmented(imgPath=imgPath, augmentation=augmentation):
                    img.transpose(PIL.Image.FLIP_TOP_BOTTOM).save(
                        getAugmentationPath(
                            imgPath=imgPath,
                            augmentation=augmentation)
                    )
                elif augmentation == 'cwRotate' and notAlreadyAugmented(imgPath=imgPath, augmentation=augmentation):
                    img.transpose(PIL.Image.ROTATE_270).save(
                        getAugmentationPath(
                            imgPath=imgPath,
                            augmentation=augmentation)
                    )
                elif augmentation == 'ccwRotate' and notAlreadyAugmented(imgPath=imgPath, augmentation=augmentation):
                    img.transpose(PIL.Image.ROTATE_90).save(
                        getAugmentationPath(
                            imgPath=imgPath,
                            augmentation=augmentation)
                    )
                elif augmentation == 'inverse' and notAlreadyAugmented(imgPath=imgPath, augmentation=augmentation):
                    img.transpose(PIL.Image.ROTATE_180).save(
                        getAugmentationPath(
                            imgPath=imgPath,
                            augmentation=augmentation)
                    )


def main():
    for i, arg in enumerate(sys.argv[1:]):
        lesImgPath = locate_files(extension=".jpg", dbName="image", path=DATASET_FOLDER)
        if arg == "--blank":
            delBlankImage(lesImgPath)
        elif arg == "--augment":
            augmentImage(lesImgPath)
        elif arg == "--clean":
            cleanDataset(lesImgPath)
        elif arg == "--make_clean_dataset":
            makeCleanDataset(lesImgPath)
        else:
            if arg != "--help":
                print("Command not understood")
            print("Usage : \nsudo python3 image_processing.py \n" + \
                  "\t- '--blank' : Remove blank-like images (<3ko) from the dataset " + DATASET_FOLDER + "\n" + \
                  "\t- '--augment' : Augment the dataset with " + ', '.join(LES_AUGMENTATION) + "\n" + \
                  "\t- '--clean' : Exectute '--blank' and remove every image extracted from rooms not indicated in clean_dataset.txt" + \
                  "\t- '--make_clean_dataset' : Create clean_dataset.txt considering each image in " + DATASET_FOLDER + " is OK ")
            return 0


if __name__ == "__main__":
    main()
