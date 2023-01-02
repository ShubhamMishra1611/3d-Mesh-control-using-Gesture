# **3d Mesh control using real time hand gestures**
Blender addon to control 3d mesh using real time hand gestures. This addon uses mediapipe to detect hand landmarks and then uses the landmarks to control the 3d mesh. Though this addon is working fine but requires a lot of improvement. I am working on it. If you want to contribute then you are most welcome.
## **Requirements**
This addon requires the following python packages to be installed in blender python environment.
1. mediapipe
2. matplotlib
3. opencv-python
4. scikit-learn
## **Installation**
To install these packages in blender python environment follow the following steps:
### Using pip
If you are confortable with pip you can install the packages using pip. To install open the terminal and type the following command:

``` pip install mediapipe matplotlib opencv-python scikit-learn --target "C:\Program Files\Blender Foundation\Blender 2.93\2.93\python\lib\site-packages" ```

You can change the path to site packages according to your blender installation path.
### Using blender scripting
To install usng blender scripting follow the following steps:
1. Open blender
2. Open the script editor
3. Copy the following code and paste it in the script editor
``` import subprocess
import sys
import os

# path to python.exe
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')

# upgrade pip
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

# install required packages
subprocess.call([python_exe, "-m", "pip", "install", "matplotlib"])
subprocess.call([python_exe, "-m", "pip", "install", "mediapipe"])
subprocess.call([python_exe, "-m", "pip", "install", "opencv-python"])
subprocess.call([python_exe, "-m", "pip", "install", "scikit-learn"])
```
You can copy the same code from [here]()

After installing the packages you need to add some files manually.
1. Add hand_track.py file from [here]() to the site-packages folder.
2. Add the DTC.pkl file from [here]() to the addon folder.
Though you can place the DTC.pkl file anywhere but you need to change the path in the gesture.py and make the add-on again.

After this you can download the addon from [here]() and install it in blender using the following steps:
1. Open blender
2. Go to Edit -> Preferences -> Add-ons
3. Click on Install button and select the gesture.zip file you downloaded.
4. Enable the addon and you are good to go.

## **Usage**
Once you have installed, to use the addon follow the following steps:
1. On the 3d view port press "N" to open the properties panel.There you can see the Gesture control panel.
2. Click on the "Start" button to start the addon.
3. Once the camera has started you can start controlling the mesh.
4. Currently we are supporting only 3 gestures:
    1. Expand and contract: To scale up and down the mesh
    2. Rotate palm when palm facing screen : To rotate the mesh about global z axis
    3. Rotate palm when palm facing upwards: To rotate the mesh about global y axis
    4. Rotate palm when palm facing sideways: To rotate the mesh about global x axis
