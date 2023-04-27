import glob
import os, sys
import pandas as pd
import random
import math
import numpy as np
import shutil

directory_path = "./NR/*.jpg"
train_path  =  "./train"
test_path   =  "./val"
train_rate = 0.7

dir = glob.glob(directory_path, recursive=False)
random.shuffle(dir)

train_number = math.floor(train_rate * len(dir))
test_number  = len(dir) - train_number
train_dir = dir[0:train_number]
test_dir  = dir[train_number:]

for i in train_dir:
     name = i.split("\\")[-1]
     new_path = os.path.join(train_path , name)
     shutil.copy(i, new_path)

for i in test_dir:
     name = i.split("\\")[-1]
     new_path = os.path.join(test_path , name)
     shutil.copy(i, new_path)
