import glob
import os, sys
import pandas as pd
import random
import math
import numpy as np
import shutil
import time

tic = time.time()

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

def train_test(data_path,
               data_dir,
               train_rate = 0.7):

     for i in data_dir:
          name = i.split("\\")[-1]
          new_path = os.path.join(data_path , name)
          shutil.copy(i, new_path)

train_test(train_path,train_dir)
train_test(test_path,test_dir)

toc = time.time()
print(f"time : {toc - tic:0.4f} seconds")
