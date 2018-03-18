# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 22:33:27 2018

@author: Will
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
#import scipy.stats as stats

path = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
#path = "C:/Users/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"

outputdata = path+"Images/"

df = pd.read_excel(path+"AllHits-Errors-Longform.xlsx",sheet_name='Sheet1')

plt.rc('font', weight='bold')

xlim = (-0.5,0.5)
modes = ['APCI','APPI','ESI','LDI']
pal = sns.color_palette("Set1", len(modes))
labelsize = 14
polarity = "Neg"
poltext = "-(-)"


f, (ax1,ax2,ax3,ax4) = plt.subplots(4,sharex=True,figsize=(8,6))
axes = [ax1,ax2,ax3,ax4]

bins = list(np.linspace(xlim[0],xlim[1],50))
hist_kws={"alpha":0.75,
           "align":'mid',
           "range":xlim,
           "linewidth":2,
           "histtype": "bar"}
kde_kws={"alpha":0.75,
         'clip':xlim,
         'kernel':'gau',
           "linewidth":2,
           "color":'k'}

for i in range(len(axes)):
    data = df[(df['Polarity']==polarity) & (df['Mode']==modes[i])]['Error']
    sns.distplot(data,
                    ax=axes[i],bins=bins,color=pal[i],#label=modes[i],
                    kde=True,kde_kws=kde_kws,
                    hist_kws=hist_kws)
    axes[i].get_yaxis().set_visible(False)
    axes[i].set_xlim(xlim)
    axes[i].spines['right'].set_visible(False)
    axes[i].spines['top'].set_visible(False)
    axes[i].spines['left'].set_visible(False)
    axes[i].text(-0.4,axes[i].get_ylim()[1]*0.4,modes[i]+poltext,
                fontsize=labelsize,color='black',ha='left',va='center') 
    
for ax in axes[:3]:
    ax.get_xaxis().set_visible(False)
    
#ax4.set_xlabel("Error (ppm)",fontweight="bold", color='black')
ax4.tick_params(direction='out', length=6, width=2, colors='k',labelsize=labelsize)
ax4.set_xlabel("Error (ppm)",color='k',fontsize=labelsize,fontweight='bold')
f.text(0.09,0.5,'Relative Counts',va='center',rotation='vertical',color='k',fontsize=labelsize)

f.savefig(outputdata+"ErrorHistogram-"+polarity+".png",dpi=300)

plt.rcdefaults()