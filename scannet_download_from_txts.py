#!/usr/bin/python3
# Automated scene downloading of scene using id files
# Written by Paul Asquin - paul.asquin@gmail.com - Summer 2018

from tools import *
import subprocess

LABEL_FOLDER = "Scannet_IDs"
PLY_FOLDER = "../Datasets/Scannet_PLY"


def downloadScene(sceneId, folder):
    """ Use scannet_download.py to dowbload the ScanNet .ply dataset """
    # scannet_download.py manages itself already downloaded files
    cmd = "python scannet_download.py -o " + folder + "/ --id " + sceneId + " --type _vh_clean_2.ply"

    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    print(out.decode('utf-8'))
    return 0


def main():
    createFolder(PLY_FOLDER)
    les_files = locate_files('.txt', relative_to_absolute_path(LABEL_FOLDER), dbName="scannet_txt_id")
    les_folders = []
    for file in les_files:
        fileName = file.split("/")[-1]
        print("--- " + str(fileName) + " ---")
        les_folders.append(fileName.replace(".txt", "").title())
        createFolder(les_folders[-1])
        with open(file, 'r') as f:
            for line in f:
                line = line.replace("\n", "")
                if "scene" in line:
                    print("Downloading " + str(line))
                    try:
                        downloadScene(sceneId=line, folder=relative_to_absolute_path(PLY_FOLDER) + "/" + les_folders[-1])
                    except KeyboardInterrupt:
                        return 0


if __name__ == '__main__':
    main()
