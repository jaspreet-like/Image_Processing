from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = ['cv2_imshow', 'cv_imshow']

import cv2
from IPython import display
from PIL import Image

import numpy as np
import subprocess
import os
import io

from base64 import b64decode, b64encode
from IPython.display import HTML

assignment_no_list = [0, 1, 2, 3]
task_no_list = [[3], [2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
def download_dataset(assignment_no=0, task_no=3):
    if (assignment_no in assignment_no_list) and (task_no in task_no_list[assignment_no]):
        url = "https://github.com/ee604/ee604_assignments/raw/master/assignment_" + str(assignment_no) + "/data/task_" + str(task_no) + ".zip"
        subprocess.check_output(["wget", "-O", "data.zip", url])
        subprocess.check_output(["unzip", "-o", "data.zip", "-d", "./data/"])
        print("Download Complete!")
    else:
        print("No dataset available for assignment", assignment_no, ", task no", task_no)

cwd = os.path.dirname(__file__)
def dummy_camera():
    img = np.load(cwd + "/data/dummy_camera.npy")
    return img

def cv2_imshow(a):
  """A replacement for cv2.imshow() for use in Jupyter notebooks.
  Taken from https://github.com/googlecolab/colabtools/blob/master/google/colab/patches/__init__.py
  Args:
    a : np.ndarray. shape (N, M) or (N, M, 1) is an NxM grayscale image. shape
      (N, M, 3) is an NxM BGR color image. shape (N, M, 4) is an NxM BGRA color
      image.
  """
  a = a.clip(0, 255).astype('uint8')
  # cv2 stores colors as BGR; convert to RGB
  if a.ndim == 3:
    if a.shape[2] == 4:
      a = cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA)
    else:
      a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
  display.display(Image.fromarray(a))

cv_imshow = cv2_imshow

def playVideo(filename, format='mp4', width=640, height=480):
    encoded = b64encode(io.open(filename, 'r+b').read())
    embedded = HTML('''
        <video width="{1}" height="{2}" controls>
            <source src="data:video/{3};base64,{0}" type="video/{3}" />
        </video>'''.format(encoded.decode('utf-8'), width, height, format))

    display.display(embedded)
