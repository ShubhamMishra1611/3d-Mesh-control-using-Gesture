import subprocess
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