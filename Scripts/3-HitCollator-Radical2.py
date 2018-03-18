# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 17:43:28 2018

@author: s1457548
"""

import pandas as pd
import os
#import re
import progressbar


path = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
#path = "C:/Users/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"

inputdata = path +"ReformAssignments/"
outputdata = path

files = os.listdir(inputdata)

mode = None
#mode = "normalise"   
df = pd.DataFrame(index=files,columns=['Total','Deprotonated','Radical','De-Duplicated'])

bar = progressbar.ProgressBar()
for x in bar(files):
    sample = x[:-5]
    df1 = pd.read_excel(inputdata+x,sheet_name="Hits")
    totallength = len(df1)
    deprotonatedlength = len(df1[df1['State']=="H-"])
    radicallength = len(df1[df1['State']==".-"])
    df1=df1.groupby('Formula',as_index=False).mean() #This clever line averages the values for duplicated formula, i.e. radicals found. 
    dedupedlength = len(df1)
    df.loc[x,'Total']=totallength
    df.loc[x,'Deprotonated']=deprotonatedlength
    df.loc[x,'Radical']=radicallength    
    df.loc[x,'De-Duplicated']=dedupedlength
    
df.to_excel(outputdata+"RadicalStats.xlsx")