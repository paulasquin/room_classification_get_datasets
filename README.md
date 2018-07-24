#room_classification_get_datasets
Project by Paul Asquin for Awabot - Summer 2018 paul.asquin@gmail.com  

# I.Introduction  
This repo is a part of the Room Classification Project. 
The aim of the Room Classification Project is to make an indoor mobile robot able to recognize a room using its 2D map. 
The output of the 2D map given should be "Kitchen", "Bedroom", "Batroom", etc.  

In order to achieve this goal, we have chosen to use Machine Learning techniques in order to obtain a powerfull recognition system with no hard-coded rules.  

As for every Machine Learning project, we need adapted datasets and a learning algorithm.  

Here is the overall architecture of the project :   
.  
├── room_classification_get_datasets  
├── room_classification_from_scratch_cnn  
├── room_classification_network_retrain  
├── Datasets (created be room_classification_get_datasets)  

For a quick start, just run  

```
sudo python big_main.py
```

This script will run every step to download and process the datasets. Still, it can stop at many steps due to dependencies lacking. For a slower but safer run, execute the following commands :  
```
sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3 python3-pip  
pip3 uninstall tensorflow --user  
pip3 install opencv-python tensorflow==1.3 Pillow plydata --user  
mkdir ../Datasets"  
python3 scannet_download_from_txts.py"  
python3 scannet_slicer.py"  
python3 matterport_download.py -o ../Datasets/HOUSE_SEGMENTATION --type house_segmentations"  
python3 matterport_unzipper.py"  
python3 matterport_slicer.py"  
python3 image_processing.py  
```
# II. Goals and instructions for room_classification_get_datasets  
  
## 0. Get the dependencies  
This project is using python3, tensorflow, opencv (cv2), PIL, plydata... So you may install them.
Maybe you'll find other forgoten dependencies. You will be able te easily install them. Do not hesitate to raise request to add their installation.
```
sudo apt-get install build-essential libssl-dev libffi-dev python-dev python3 python3-pip  
pip3 uninstall tensorflow --user  
pip3 install opencv-python tensorflow==1.3 Pillow plydata --user 
```

## 1. Download the datasets  
For this project, we are using datasets from [ScanNet](http://www.scan-net.org/) and [Matterport](https://matterport.com/).
In order to get them, we are using the scripts given by those organization [scannet_donwload.py](scannet_donwload.py) and [matterport_slicer.py](matterport_slicer.py).
We are also using specific command to class those datas. For the ScanNet dataset, we have developed [scannet_download_from_txts.py](scannet_download_from_txts.py).  

### a. ScanNet  
[ScanNet](http://www.scan-net.org/) is a dataset developped by Stanford University, Princeton University and the Technical University of Munich. 
It is made with RGB-D scan of multiple rooms, reconstructed in [PLY files](https://en.wikipedia.org/wiki/PLY_(file_format)) (Polygon File Format). 
For each room of a unique type, we have a unique PLY file corresponding.  

In order to smart-download the ScanNet dataset, we have to get the room IDs we want to download. In order to do so :   
- Go to : https://dovahkiin.stanford.edu/scannet-browse/scans/scannet/querier  
- Display wanted scenes with the search bar (for example : enter "Kitchen")  
- Click on "Save Ids" (the drop-down menu should be on "original")  
- A window opens. Make a Ctrl+S  
- Rename the file as "room.txt" (example : kitchen.txt, bedroom.txt, living.txt...)  
- Save the .txt file in a folder "Scannet_IDs", at the project root  

The script [scannet_download_from_txts.py](scannet_download_from_txts.py) will read those txt files and use the script [scannet_donwload.py](scannet_donwload.py) to download only the PLY file of requested rooms. 
We can notice that their is not only one ply file per room ID (also call scene ID). Here, we are using \_2.ply files, that are at lower resolutions than regular .ply files.
Because we are going to reduce the resolution of our slices, this is acceptable and will improve our downloading and processing time.
The dataset will be written into the "Datasets/Scannet_PLY" folder and can use up to 220Go. With our script, each type of scene is split in a named folder corresponding to the name of txt files ("Kitchen", "Bathroom").

You may just run :
```
mkdir ../Datasets"  
python3 scannet_download_from_txts.py"
```

