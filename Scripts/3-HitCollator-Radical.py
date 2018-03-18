# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 22:38:19 2018

@author: Will
"""

import pandas as pd
import os
import re
import progressbar

chemdict = {'H':(1.007825, 0.99984),
            'C':(12.000000, 0.98892),
            'O':(15.994915, 0.99762),
            'S':(31.972071, 0.95041)}

# Aromaticity Index calculation. Unlike DBE, this factors in O and S. Taken from DOI: 10.1002/rcm.2386
# Added switch for using the "modified" aromaticity index instead of the normal one. This halves #O on basis/assumption only half will be pi-bound. 
def AIcalc(C,H,O,S,N=0,P=0,mod=True):
    if mod == True:
        O = O/2
    top = 1+C-O-S-(0.5*H)
    btm = C-O-S-N-P
    if btm == 0:
        AI = 0
    else:
        AI = top/btm
    if AI < 0:
        AI = 0
    return AI

# Calculates DBE
def DBEcalc(C,H,N,X=0):
    if C == 0:
        return None
    DBE = (C+1-(H/2)-(X/2)+(N/2))
    return DBE

def formulaproperties(df):     
    df1 = pd.DataFrame(columns=df.columns[3:],index=['C','H','O','Hetero','OC','HC','DBE','AImod','Mass'])
    bar = progressbar.ProgressBar()
    for y in bar(df1.columns.values):
        breakdown = re.split(r'(\d+)',y)
        C = int(breakdown[1])
        H = int(breakdown[3])
        if 'O' in y:
            O = int(breakdown[5])
            hetero = 'O'+str(O)
        if 'O' not in y:
            O = 0 #otherwise 0 count is wrong...
            hetero = 'CH'
        df1.loc['C',y] = C
        df1.loc['H',y] = H
        df1.loc['O',y] = O
        df1.loc['OC',y] = O/C
        df1.loc['HC',y] = H/C
        df1.loc['Hetero',y] = hetero
        df1.loc['DBE',y] = DBEcalc(C,H,0)
        df1.loc['AImod',y] = AIcalc(C,H,O,0)
        Mass = (C*chemdict['C'][0])+(H*chemdict['H'][0])+(O*chemdict['O'][0])
        df1.loc['Mass',y] = Mass
    return df1

path = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
#path = "C:/Users/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"

inputdata = path +"ReformAssignments/"
outputdata = path

files = os.listdir(inputdata)

mode = None
mode = "normalise"   

df = pd.DataFrame(index=files,columns=['Mode','Polarity','Sample'])
bar = progressbar.ProgressBar()
for x in bar(files):
    sample = x[:-5]
    df1 = pd.read_excel(inputdata+x,sheet_name="Hits")
    #df1=df1.groupby('Formula',as_index=False).mean() #This clever line averages the values for duplicated formula, i.e. radicals found. 
    df1.rename(columns={sample:'Abundance'},inplace=True)
    df.loc[x,'Mode'] = x.split('-')[0]
    df.loc[x,'Polarity'] = x.split('-')[1]
    df.loc[x,'Sample'] = sample[-8:]
    for index,data in df1.iterrows():
        if mode == 'normalise':
            df.loc[x,data['Formula']] = data['Abundance']/df1['Abundance'].sum()
        else:
            df.loc[x,data['Formula']] = data['Abundance']

filename = outputdata+"AllHits-Matrix.xlsx"
if mode == 'normalise':
    filename = outputdata+"AllHits-Matrix-Norm.xlsx"
    
df.to_excel(filename)


# Long form generation
df1 = formulaproperties(df)


df['id'] = df.index
dflong = pd.melt(df, id_vars=['id','Mode','Polarity','Sample'],value_vars=df.columns[3:-1].values.tolist(),
                 var_name='Formula', value_name='Abundance')
dflong = dflong.dropna(axis=0,how='any').reset_index()

bar = progressbar.ProgressBar()
for index,data in bar(dflong.iterrows()):
    dflong.loc[index,'C'] = df1.loc['C',data['Formula']]
    dflong.loc[index,'H'] = df1.loc['H',data['Formula']]
    dflong.loc[index,'O'] = df1.loc['O',data['Formula']]
    dflong.loc[index,'OC'] = df1.loc['OC',data['Formula']]
    dflong.loc[index,'HC'] = df1.loc['HC',data['Formula']]
    dflong.loc[index,'HeteroClass'] = df1.loc['Hetero',data['Formula']]
    dflong.loc[index,'DBE'] = df1.loc['DBE',data['Formula']]
    dflong.loc[index,'AImod'] = df1.loc['AImod',data['Formula']]
    dflong.loc[index,'Mass'] = df1.loc['Mass',data['Formula']]
 
dflong = dflong.drop('index',axis=1)

filename = outputdata+"AllHits-Longform.xlsx"
if mode == 'normalise':
    filename = outputdata+"AllHits-Longform-Norm.xlsx"
dflong.to_excel(filename)