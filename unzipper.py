from __future__ import print_function
import sys
import zipfile
from tools import *


def unzip(path):
    print("Unzipping " + path, end="")
    sys.stdout.flush()
    extractPath = '/'.join(path.split("/")[:-2])
    try:
        zipFile = zipfile.ZipFile(path, 'r')

        zipFile.extractall(extractPath)
        zipFile.close()
        print(" - Done")
        with open("unzipDone.log", "a") as f:
            f.write(path + "\n")
    except KeyboardInterrupt:
        return 1
    except:
        print(" - Error")
        with open("unzipError.log", "a") as f:
            f.write(path + "\n")
    return 0


def main():
    lesZipFile = locate_files(extension=".zip", dbName="locateZip")
    for zipFile in lesZipFile:
        if unzip(zipFile) == 1:
            return 1


if __name__ == "__main__":
    main()