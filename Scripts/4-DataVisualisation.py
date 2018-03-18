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


path = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
#path = "C:/Users/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"

inputdata = path +"ReformAssignments/"
outputdata = path+"Images/PanelPlots/"

df1 = pd.read_excel(path+"AllHits-Longform.xlsx")
norm = False
#df1 = pd.read_excel(path+"AllHits-Longform-Norm.xlsx")
#norm = True
df1 = df1[df1['Mass']<800]
df1 = df1[df1['O']<20]

sns.set_style("white")
sns.set_context("paper",font_scale=2)  
glocmap = cm.viridis_r


### THIS DOES THE SET/UNIQUE FORMULA COUNTING STEP ####
staticolumns = ['C','H','O','OC','HC','Mass','DBE','AImod']
df2 = df1.rename(columns={'id':'Count'}).groupby(['Polarity','Mode','Formula'],as_index=False)['Count'].count()
df2['Abundance'] = df1.groupby(['Polarity','Mode','Formula'],as_index=False)['Abundance'].median()['Abundance']
df2['HeteroClass'] = df1.groupby(['Polarity','Mode','Formula'],as_index=False)['HeteroClass'].first()['HeteroClass']
df2[staticolumns] = df1.groupby(['Polarity','Mode','Formula'],as_index=False)[staticolumns].mean()[staticolumns]
        

def panelplot2(plttype,modes,polarity,df,figsize):
    df = df.sort_values('Mass')
    scalefactor = 1E-6#1E4
    labelsize = 20
    #nbins = 3 #for ticker
    if plttype == 'VK':
        X = 'OC'
        Y = 'HC'
        S = 'Abundance'
        C = 'Mass'
        xlim = (0,1.5)
        ylim = (0,2.5)
        clim = (0,800)
        xlabel, ylabel, clabel = 'O/C','H/C', 'Mass'
    elif plttype == 'DBE':
        X = 'C'
        Y = 'DBE'
        S = 'Abundance'
        C = 'O'
        xlim = (0,60)
        ylim = (0,30)
        clim = (0,20)
        xlabel, ylabel, clabel = 'C','DBE','O'
    elif plttype == 'AImod':
        X = 'C'
        Y = 'AImod'
        S = 'Abundance'
        C = 'O'
        xlim = (0,60)
        ylim = (0,1)
        clim = (0,20)
        xlabel, ylabel, clabel = 'C','AImod','O'
    
    f, axarr = plt.subplots(2, 2,figsize=figsize)
    i = 0
    for mode in modes:
        ax = axarr.flat[i]
        conditions = (df['Mode']==mode) & (df['Polarity']==polarity)
        im = ax.scatter(
                x=df[conditions][X],
                y=df[conditions][Y],
                s=df[conditions][S]*scalefactor,
                c=df[conditions][C],cmap=glocmap,
                alpha=0.85,edgecolor='k',linewidth=0.25)
        ax.text(0.9*xlim[1],0.1*ylim[1],s='{0}'.format(int(len(df[conditions]['Formula']))),horizontalalignment='right')
        ax.set_title(mode,position=(0.5, 0.9),verticalalignment='center')
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.tick_params(axis="both",which="major",left="on",bottom="on",top="off",right="off",labelsize=labelsize)
        ax.tick_params(axis="both",which="minor",left="on",bottom="on",top="off",right="off")
        ax.xaxis.set_major_locator(ticker.MaxNLocator(3))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(3))
        ax.xaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
        ax.yaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
        i +=1
    for ax in axarr.flat[::2]:
        ax.set_ylabel(ylabel)
        #ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=nbins,prine='upper'))
    #xticklabels = []
    for ax in axarr.flat[2:]:
        ax.set_xlabel(xlabel)
        #ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=nbins+1,prine='upper'))
        #ax.set_xticklabels([])
        #xticklabels.append(ax.get_xticklabels())
        #plt.setp(xticklabels, visible=False)
        #ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=nbins,prune='upper')) # added 
        
    plt.subplots_adjust(hspace=0.1,wspace=0.08)
    #plt.suptitle(polarity,x=0.43)
    #divider = make_axes_locatable(plt.gca())
    #cax = divider.append_axes("right", "5%", pad="3%")
    color_bar = f.colorbar(im, alpha=1,ax=axarr.ravel().tolist())#,cax=cax)
    color_bar.set_label(clabel,size=labelsize)
    color_bar.set_alpha(1)
    color_bar.set_clim(clim)
    color_bar.draw_all()
    # Fine-tune figure; hide x ticks for top plots and y ticks for right plots
    plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)
    plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
    #plt.tight_layout()
    plt.savefig(outputdata+plttype+"_"+polarity+"_"+"panel.png",dpi=300) #saves the PNG (raster) at high DPI

figsize = (3.25*5,3*3)
plttypes = ['VK','DBE','AImod']
modes = df2['Mode'].value_counts().index.values.tolist() #['APCI','APPI','ESI','LDI']
modes.sort()
polarities = df2['Polarity'].value_counts().index.values.tolist()
polarities.sort()
df2 = df2.sort_values(by='Mass')
for plttype in plttypes:
    for polarity in polarities:
        panelplot2(plttype,modes,polarity,df2,figsize)



"""
#### For the panelled visualisation: ### 
### Sample, Polarity specific plots ###
def panelplot(plttype,modes,sample,polarity,df):
    df = df.sort_values('Mass')
    scalefactor = 1E-7#1E4
    labelsize = 20
    if plttype == 'VK':
        X = 'OC'
        Y = 'HC'
        S = 'Abundance'
        C = 'Mass'
        xlim = (0,1.5)
        ylim = (0,2.5)
        clim = (0,1000)
        xlabel, ylabel, clabel = 'O/C','H/C', 'Mass'
    elif plttype == 'DBE':
        X = 'C'
        Y = 'DBE'
        S = 'Abundance'
        C = 'O'
        xlim = (0,60)
        ylim = (0,30)
        clim = (0,20)
        xlabel, ylabel, clabel = 'C','DBE','O'
    elif plttype == 'AImod':
        X = 'C'
        Y = 'AImod'
        S = 'Abundance'
        C = 'O'
        xlim = (0,60)
        ylim = (0,1)
        clim = (0,20)
        xlabel, ylabel, clabel = 'C','AImod','O'
    
    f, axarr = plt.subplots(2, 2,figsize=(12,7))
    i = 0
    for mode in modes:
        ax = axarr.flat[i]
        conditions = (df['Mode']==mode) & (df['Polarity']==polarity) & (df['Sample']==sample)
        im = ax.scatter(
                x=df[conditions][X],
                y=df[conditions][Y],
                s=df[conditions][S]*scalefactor,
                c=df[conditions][C],cmap=glocmap,
                alpha=0.8,edgecolor='k',linewidth=0.25)
        ax.text(0.9*xlim[1],0.1*ylim[1],s='{0}'.format(int(len(df[conditions]['Formula']))),horizontalalignment='right')
        ax.set_title(mode)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.tick_params(axis="both",which="major",left="on",bottom="on",top="off",right="off",labelsize=labelsize)
        ax.tick_params(axis="both",which="minor",left="on",bottom="on",top="off",right="off")
        ax.xaxis.set_major_locator(ticker.MaxNLocator(3))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(3))
        ax.xaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
        ax.yaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
        i +=1
    for ax in axarr.flat[::2]:
        ax.set_ylabel(ylabel)
    for ax in axarr.flat[2:]:
        ax.set_xlabel(xlabel)
        
    plt.subplots_adjust(hspace=0.4)
    plt.suptitle(sample+" "+polarity,x=0.43)
    color_bar = f.colorbar(im, ax=axarr.ravel().tolist(),alpha=1)
    color_bar.set_label(clabel,size=labelsize)
    color_bar.set_alpha(1)
    color_bar.set_clim(clim)
    color_bar.draw_all()
    # Fine-tune figure; hide x ticks for top plots and y ticks for right plots
    plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)
    plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
    #plt.tight_layout()
    plt.savefig(outputdata+plttype+"_"+sample+"_"+polarity+"_"+"panel.png",dpi=300) #saves the PNG (raster) at high DPI

plttypes = ['VK','DBE','AImod']
modes = df1['Mode'].value_counts().index.values.tolist() #['APCI','APPI','ESI','LDI']
samples = df1['Sample'].value_counts().index.values.tolist()
polarities = df1['Polarity'].value_counts().index.values.tolist()

for plttype in plttypes:
    for polarity in polarities:
        for sample in samples:
            panelplot(plttype,modes,sample,polarity,df1)
            
"""    