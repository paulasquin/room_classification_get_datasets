#room_classification_get_datasets
Project by [Paul Asquin](https://www.linkedin.com/in/paulasquin/) for Awabot - Summer 2018 paul.asquin@gmail.com  

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
This script will run every step to download and process the datasets. Still, it can stop at many steps due to dependencies lacking.  
For a slower but safer run, follow the next instructions 

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
  
**WARNING** : In order to use those datasets, you need to obtain autorizations from ScanNet and Matterport teams.  
\- For Matterport : you will wind the instructions to accept the [END USER LICENSE AGREEMENT](http://dovahkiin.stanford.edu/matterport/public/MP_TOS.pdf) in the _Data_ section of their [Github page](https://github.com/niessner/Matterport)  
\- For ScanNet : you will find the instructions to accept the [ScanNet Terms of Use](http://dovahkiin.stanford.edu/scannet-public/ScanNet_TOS.pdf) in the _ScanNet Data_ section of their [Github page](https://github.com/ScanNet/ScanNet)  

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

### b. Matterport  
The [Matterport](https://matterport.com/) dataset contains, like ScanNet, .ply files. However, those files are the result of a complete house scan. Auxiliary files with the .house extension give a label to the regions of the house. Thus, it is possible to cross the datas to extract specific rooms.

In order to download the Matrerport dataset, run : 
```
python3 matterport_download.py -o ../Datasets/HOUSE_SEGMENTATION --type house_segmentations
```

## 2. Process the datasets  
### a. Cut the rooms into slices
PLY files a 3D representation of rooms. Because we want to train an algorithm on 2D maps, as those created by regular mobile robot with LIDAR, we have to slice those datasets.
Furthermore, we will choose multiple slice altitudes. The altitudes and the heigth of the slices are given into the "dataset"\_slicer.py
Once the altitudes are chosen (or unchanged), you can run : 
```
sudo python3 scannet_slicer.py
sudo python3 matterport_slicer.py
```
The datasets will be written under the Datasets/JPG, splited between Bathroom, Kitchen, etc, folders. They will form a new and unique dataset.  

Here is an example of Matterport kitchen slices : 

Altitude 0.4m :  
![kitchen 0.4](docs/ex_kitchen-0.4.jpg)

Altitude 0.5m :  
![kitchen 0.5](docs/ex_kitchen-0.5.jpg)

Altitude 0.7m :  
![kitchen 0.7](docs/ex_kitchen-0.7.jpg)

### b. Clean and augment the dataset  
Sometimes, datas can have strange shapes. They can be bugs on multiple levels causing an unwanted image : almost empty maps, non-representative architectures, noises... 
You can remove those file by hand. But before that, you can use [image_processing.py](image_processing.py) rm technique to speed up the process. 
For this, disable the automatic processing by changing the _CHOOSE_ variable from False to True. You can also fine tune the deleting conditions
Then, run 
```
sudo python3 image_processing.py --clean --augment
```

In order to train or re-train our models, we need a lot of data. 
From the data we have, we have the possibility to create variants to enrich our total set, by using 4 different rotations of each maps and 2 mirror transformations (vertical and horizontal. 
This operation allows the models to extract new features or generalizations. 
Selecting multiple cutting heights is already a form of data augmentation. 
We can also create new images from rotations or mirror effects of the original.

If those steps saw an happy ending, you can move to either the _room_classification_from_scratch_cnn_ or _room_classification_network_retrain_ repo
