
##The original FITS files stored in folder 'ktwo' and detrended FITS files in folder 'ktwo-detrended', 
##both in parent directory 'kepler'

import os, sys, matplotlib, pylab
import numpy  as np
from astropy.io import fits
from matplotlib import pyplot as plt
import re

#Read folder name starting with ktwo

os.chdir("/home/vatsal/UThesis/K2/data/kepler") # Change Directory
nowpath = os.getcwd()
filenamelist = filter(lambda x: x.startswith('ktwo'), os.listdir(nowpath))
writelist = [ i +'\n' for i in filenamelist]
with open('list.txt','w') as f:
    map( f.write , writelist)
f.close()                                       #making the list of folders

Q10up = 'list.txt'
Q10_file = file(Q10up).readlines()

ktwoID = []
ktwo_detID = []

for i in Q10_file:
    path = i.replace('\n','')
    os.chdir("/home/vatsal/UThesis/K2/data/kepler/%s"%path)
    
    foldername = i.strip().split(' ')
    folderlistfile = '%s_list.txt' %foldername[0]
    
    
    #1 Read names of all files ending with .fits
    nowpath = os.getcwd()
    filenamelist = filter(lambda x: x.endswith('.fits'), os.listdir(nowpath))
    
    #1.5 Write Raw data file into txt list (.fits)
    writelist = [ i +'\n' for i in filenamelist]
    with open('%s_Fits_list.txt' %foldername[0],'w') as f:
        map(f.write , writelist)
        
    #2 Read needed file data
    Kepler = '%s_Fits_list.txt' %foldername[0]
    LC_file= file(Kepler).readlines()
    
    print LC_file
    
    for j in LC_file:
        if(j.startswith('ktwo')):
            a = re.findall('\d+', j)
            ktwoID.append(a[0])
        
        elif(j.startswith('EPIC')):
            a = re.findall('\d+', j)
            ktwo_detID.append(a[0])

# print ktwoID
# print ktwo_detID
# print set(ktwoID) & set(ktwo_detID)

com_ID =  [i for i in set(ktwoID) & set(ktwo_detID)]      #list of IDs common to both original and detrended list of files-
                                                          #essentially the ones that have to be analysed

