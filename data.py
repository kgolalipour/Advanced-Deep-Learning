import pandas as pd
import glob
import os, sys

dataframe1 = pd.read_csv("List.txt",delimiter = '	')  #C:\Users\Ron\Desktop\Test\Product_List.txt
dataframe1.columns = ['Name', 'Platz']
dataframe1.to_csv('List.csv',index = None)

a = pd.read_csv('List.csv')   #,encoding='ansi'  ,encoding='utf-8'  ,encoding='latin1' ,encoding='iso-8859-1'  ,encoding='cp1252'  #b=a.describe()
data = pd.DataFrame(a)


path = r'C:\progC\github_company\other\crnn-pytorch\License_Plate_Dataset1\License Plate\NR\*.jpg'
dir = glob.glob(path, recursive=False)

for i in range(len(data)):
      sel = data.loc[i,'Name']
      if  sel in str(dir) :
        after = str(i)+'_'+str(data.loc[i,'Platz'])+'.jpg'
        befor = 'C:\\progC\\github_company\\other\\crnn-pytorch\\License_Plate_Dataset1\\License Plate\\NR\\'+sel
        os.renames(befor,after)

