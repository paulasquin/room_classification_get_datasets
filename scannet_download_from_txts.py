# Automating scene downloading of scene id files
# Written by Paul Asquin paul.asquin@gmail.com for Awabot Intelligence, 2018

from tools import *
import subprocess

LABEL_FOLDER = "Scannet_IDs"
PLY_FOLDER = "../Datasets/Scannet_PLY"


def downloadScene(sceneId, folder):
    # scannet_download.py manage itself already downloaded files
    cmd = "python scannet_download.py -o " + folder + "/ --id " + sceneId + " --type _vh_clean_2.ply"

    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    print(out.decode('utf-8'))
    return 0


def main():
    createFolder(PLY_FOLDER)
    lesFile = locate_files('.txt', relative_to_absolute_path(LABEL_FOLDER), dbName="scannet_txt_id")
    lesFolder = []
    for file in lesFile:
        fileName = file.split("/")[-1]
        print("--- " + str(fileName) + " ---")
        lesFolder.append(fileName.replace(".txt", "").title())
        createFolder(lesFolder[-1])
        with open(file, 'r') as f:
            for line in f:
                line = line.replace("\n", "")
                if "scene" in line:
                    print("Downloading " + str(line))
                    try:
                        downloadScene(sceneId=line, folder=relative_to_absolute_path(PLY_FOLDER) + "/" + lesFolder[-1])
                    except KeyboardInterrupt:
                        return 0


if __name__ == '__main__':
    main()
