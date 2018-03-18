# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:04:37 2017

@author: s1457548
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import ticker
#import re
#import numpy as np
#import pyupset as pyu


path = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
#path = "C:/Users/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"

inputdata = path +"ReformAssignments/"
outputdata = path+"Images/"

df = pd.read_excel(path+"AllHits-Longform.xlsx")
norm = False
#df1 = pd.read_excel(path+"AllHits-Longform-Norm.xlsx")
#norm = True

df = df[df['Mass']<800]
df = df[df['O']<20]


sns.set_style("white")
sns.set_context("paper",font_scale=2)  
glocmap = cm.viridis_r


staticolumns = ['C','H','O','OC','HC','Mass','DBE','AImod']
df2 = df.rename(columns={'id':'Count'}).groupby(['Polarity','Mode','Formula'],as_index=False)['Count'].count()
df2['Abundance'] = df.groupby(['Polarity','Mode','Formula'],as_index=False)['Abundance'].median()['Abundance']
df2['HeteroClass'] = df.groupby(['Polarity','Mode','Formula'],as_index=False)['HeteroClass'].first()['HeteroClass']
df2[staticolumns] = df.groupby(['Polarity','Mode','Formula'],as_index=False)[staticolumns].mean()[staticolumns]


#polarities = ["Neg","Pos"]
polarity='Neg'
modes = ["APCI","APPI","ESI","LDI"]
pal = sns.color_palette("Set1", len(modes))
colors = {'APCI':pal[0], 'APPI':pal[1], 'ESI':pal[2], 'LDI':pal[3]}
labelsize=20

def VKplot():
    df3 = df2.drop_duplicates(subset=['Formula'],keep=False).copy()
    df4 = df2.drop(df3.index)
    #scalefactor=1E-5
    scalefactor = (df3['Abundance'].mean()/(df3['Abundance'].sum()*len(df3)))*20
    
    xlim = (0,1.5)
    ylim = (0,2.5)
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(x=df4['OC'], y=df4['HC'],c='gray',
               s=df4['Abundance']*scalefactor*0.5,alpha=0.3,label='Common')
    for i in modes:
        ax.scatter(x=df3[df3['Mode']==i]['OC'], y=df3[df3['Mode']==i]['HC'],
                   c=df3[df3['Mode']==i]['Mode'].apply(lambda x: colors[x]),
                   s=df3[df3['Mode']==i]['Abundance']*scalefactor,alpha=0.6,label=i)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("O/C",fontdict={'fontsize':labelsize})
    ax.set_ylabel("H/C",fontdict={'fontsize':labelsize})
    ax.tick_params(axis="both",which="major",left="on",bottom="on",top="off",right="off",labelsize=labelsize)
    ax.tick_params(axis="both",which="minor",left="on",bottom="on",top="off",right="off")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(3))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(3))
    ax.xaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
    ax.yaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
    
    lgnd = plt.legend()
    for i in range(5):
        lgnd.legendHandles[i]._sizes = [30]
    plt.tight_layout()
    plt.savefig(outputdata+"UniqueVanKrevelen-"+polarity+".png",dpi=300) #saves the PNG (raster) at high DPI
    plt.show()
    
VKplot()
 

def DBEplot():
    df3 = df2.drop_duplicates(subset=['Formula'],keep=False).copy()
    df4 = df2.drop(df3.index)
    #scalefactor=1E-5
    scalefactor = (df3['Abundance'].mean()/(df3['Abundance'].sum()*len(df3)))*20
    
    xlim = (0,60)
    ylim = (0,30)
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(x=df4['C'], y=df4['DBE'],c='gray',
               s=df4['Abundance']*scalefactor*0.5,alpha=0.3,label='Common')
    for i in modes:
        ax.scatter(x=df3[df3['Mode']==i]['C'], y=df3[df3['Mode']==i]['DBE'],
                   c=df3[df3['Mode']==i]['Mode'].apply(lambda x: colors[x]),
                   s=df3[df3['Mode']==i]['Abundance']*scalefactor,alpha=0.6,label=i)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("C",fontdict={'fontsize':labelsize})
    ax.set_ylabel("DBE",fontdict={'fontsize':labelsize})
    ax.tick_params(axis="both",which="major",left="on",bottom="on",top="off",right="off",labelsize=labelsize)
    ax.tick_params(axis="both",which="minor",left="on",bottom="on",top="off",right="off")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(3))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(3))
    ax.xaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
    ax.yaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
    
    lgnd = plt.legend()
    for i in range(5):
        lgnd.legendHandles[i]._sizes = [30]
    plt.tight_layout()
    plt.savefig(outputdata+"UniqueDBE-"+polarity+".png",dpi=300) #saves the PNG (raster) at high DPI
    plt.show()


DBEplot()
"""

df_APCI = df[df['Mode']=='APCI']
df_APPI = df[df['Mode']=='APPI']
df_ESI = df[df['Mode']=='ESI']
df_LDI = df[df['Mode']=='LDI']

sns.kdeplot(df_APCI['OC'],df_APCI['HC'],shade=True,cmap="Greens", shade_lowest=False,alpha=0.75)
sns.kdeplot(df_APPI['OC'],df_APPI['HC'],shade=True,cmap="Reds", shade_lowest=False,alpha=0.75)
sns.kdeplot(df_ESI['OC'],df_ESI['HC'],shade=True,cmap="Blues", shade_lowest=False,alpha=0.75)
sns.kdeplot(df_LDI['OC'],df_LDI['HC'],shade=True,cmap="Blues", shade_lowest=False,alpha=0.75)


plt.scatter(df_APCI['OC'],df_APCI['HC'],color='g',alpha=0.75)
plt.scatter(df_APPI['OC'],df_APPI['HC'],color='r',alpha=0.75)
plt.scatter(df_ESI['OC'],df_ESI['HC'],color='b',alpha=0.75)
plt.scatter(df_LDI['OC'],df_LDI['HC'],color='k',alpha=0.75)
"""