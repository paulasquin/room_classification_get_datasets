#  Process images to augment the dataset or clean it of blank like image
# Written by Paul Asquin paul.asquin@gmail.com for Awabot Intelligence, 2018

from tools import *
import PIL

LES_AUGMENTATION = ['width-flip', 'height-flip', 'cwRotate', 'ccwRotate', 'inverse']
DATASET_FOLDER = "../Datasets/JPG"
CHOOSE = False


def delBlankImage(lesImgPath):
    """ Check if given image paths are empty-like (less than 6ko), if yes, they are removed """
    print("Deleting empty-like image (<6ko)")
    for path in lesImgPath:
        if os.path.getsize(path) < 6000 or "-1.jpg" in path or "-0.2.jpg" in path:
            print("\tDel " + path.split("/")[-1] + " "*30, end="\r")
            os.remove(path)
            with open("empty_image.txt", "a") as f:
                f.write(path + "\n")
    print("Ended")
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
    for imgPath in lesImgPath:
        with PIL.Image.open(imgPath) as img:
            print(imgPath)
            for augmentation in LES_AUGMENTATION:
                if augmentation == 'width-flip' and notAlreadyAugmented(imgPath=imgPath, augmentation=augmentation):
                    print("\t" + augmentation + " Augmenting")
                    img.transpose(PIL.Image.FLIP_LEFT_RIGHT).save(
                        getAugmentationPath(
                            imgPath=imgPath,
                            augmentation=augmentation)
                    )
                elif augmentation == 'height-flip' and notAlreadyAugmented(imgPath=imgPath, augmentation=augmentation):
                    print("\t" + augmentation + " Augmenting")
                    img.transpose(PIL.Image.FLIP_TOP_BOTTOM).save(
                        getAugmentationPath(
                            imgPath=imgPath,
                            augmentation=augmentation)
                    )
                elif augmentation == 'cwRotate' and notAlreadyAugmented(imgPath=imgPath, augmentation=augmentation):
                    print("\t" + augmentation + " Augmenting")
                    img.transpose(PIL.Image.ROTATE_270).save(
                        getAugmentationPath(
                            imgPath=imgPath,
                            augmentation=augmentation)
                    )
                elif augmentation == 'ccwRotate' and notAlreadyAugmented(imgPath=imgPath, augmentation=augmentation):
                    print("\t" + augmentation + " Augmenting")
                    img.transpose(PIL.Image.ROTATE_90).save(
                        getAugmentationPath(
                            imgPath=imgPath,
                            augmentation=augmentation)
                    )
                elif augmentation == 'inverse' and notAlreadyAugmented(imgPath=imgPath, augmentation=augmentation):
                    print("\t" + augmentation + " Augmenting")
                    img.transpose(PIL.Image.ROTATE_180).save(
                        getAugmentationPath(
                            imgPath=imgPath,
                            augmentation=augmentation)
                    )


def main():
    while CHOOSE:
        command = input("Enter \n"
                        "\t- 'rm' to del blank-like images from the dataset " + DATASET_FOLDER + "\n" + \
                        "\t- 'aug' to augment the dataset with " + ', '.join(LES_AUGMENTATION) + "\n" + \
                        "\t- 'e' to end the program\n>> ")
        if command == "rm":
            delBlankImage(locate_files(extension=".jpg", dbName="image", path=DATASET_FOLDER))
        elif command == "aug":
            augmentImage(locate_files(extension=".jpg", dbName="image", path=DATASET_FOLDER))
        elif command == "e":
            print("Exiting the program")
            return 0
        else:
            print("Command not understood")
    if not CHOOSE:
        delBlankImage(locate_files(extension=".jpg", dbName="image", path=DATASET_FOLDER))
        augmentImage(locate_files(extension=".jpg", dbName="image", path=DATASET_FOLDER))

if __name__ == "__main__":
    main()
