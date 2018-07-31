import subprocess


class Script:
    cmd = ""
    description = ""

    def __init__(self, cmd, description):
        self.cmd = cmd
        self.description = description


LES_SCRIPTS = [
    Script(
        "sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3 python3-pip",
        "Installing python3, python3-pip"
    ),
    Script(
        "pip3 uninstall tensorflow --user",
        "Uninstalling other tensorflow version"
    ),		
    Script(
        "pip3 install opencv-python tensorflow==1.3 Pillow plydata --user",
        "Installing cv2, tensorflow"
    ),	
    Script(
        "mkdir ../Datasets",
        "Make Datasets dir if doesn't already exist"
    ),	
    Script(
        "python3 scannet_download_from_txts.py",
        "Downloading the ScanNet dataset from IDs text files in the 'Scannet_IDs' folder"
    ),
    Script(
        "python3 scannet_slicer.py",
        "Slicing the ScanNet dataset"
    ),
    Script(
        "python3 matterport_download.py -o ../Datasets/HOUSE_SEGMENTATION --type house_segmentations",
        "Downloading the Matterport dataset"
    ),
    Script(
        "python3 matterport_unzipper.py",
        "Unzipping Matterport"
    ),
    Script(
        "python3 matterport_slicer.py",
        "Slicing the Matterport dataset"
    ),
    Script(
        "python3 image_processing.py --clean --augment",
        "Augmenting datasets"
    )
]


def main():
    print("Big Main program to download and process datasets for the Room Classification project")
    input("Press any key to continue...")

    for script in LES_SCRIPTS:
        print("*" * 10)
        print(script.description)
        print(script.cmd)
        print("*" * 10)
        p = subprocess.Popen([script.cmd], stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        print(out.decode('utf-8'))
    return 0


if __name__ == "__main__":
    main()
