import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#import seaborn as sns
#import os



sample = "S14-1944"
path = "G:/DATA/FTICRMS/KEW-20160915-MixedIonization/Good-Data/"

inpath = path +"XYData/"+sample+"/"
outpath = path+"Figures/"

assignments = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
assignments = assignments+"ReformAssignments/"


labelsize = 14
modes = ['APCI','APPI','ESI','LDI']
#polarities = ['Negative','Positive']
polarities = ['Negative']
xlims = [(100,1000),
         (363.0,376.3),
         (364.94,365.35)]

xlims = [(100,1000),
         (325,335),
         (333,333.2)]
#xlim = xlims[0]
#mode = modes[0]
#polarity = polarities[0]
for polarity in polarities:
    fig,axarr = plt.subplots(4,3,sharex='col',figsize=(10,6))
    i,j=0,0  
    for mode in modes:
        j= 0
        file = sample+"-"+mode+"-"+polarity
        df = pd.read_csv(inpath+file+".xy",sep=" ",index_col=0,names=["I"])
        df["I"] = df["I"]/df["I"].max()*100
        if polarity == "Positive":
            shmode = "(+)"
        else:
            shmode = "(-)"
        for xlim in xlims:
            axarr[i,j].plot(df[xlim[0]:xlim[1]],c='k',linewidth=1.1)
            axarr[i,j].set_xlim(xlim)
            ymax = float(df[(df.index > xlim[0]) & (df.index < xlim[1])].max().values)
            axarr[i,j].set_ylim(0-ymax*0.05,ymax*1.05)
            """
            axarr[i,j].text(0.95,0.9,mode+" "+shmode,
                    size=labelsize,
                    horizontalalignment = "right",
                    verticalalignment = "top",
                    transform=axarr[i,j].transAxes,
                    bbox=dict(facecolor='w', alpha=0.5))
            """
            if j ==2:
                axarr[i,j].xaxis.set_major_locator(ticker.LinearLocator(3))
                sample2= mode+"-"+polarity[:3]+"-"+sample
                df2= pd.read_excel(assignments+sample2+".xlsx")
                df2["NormAbun"] = df2[sample2]/df2[sample2].max()*100
                df2 = df2[df2['C']!=0]
                df2=df2[(df2['Mass']<xlim[1])&(df2['Mass']>xlim[0])]
                for index,data in df2.iterrows():
                    if data['C13']>0:
                        symbol = "+"
                    else:
                        symbol = "•"#"▼"#"•"
                    axarr[i,j].text(data['Mass']-0.0006,data['NormAbun'],symbol,
                         size=int(labelsize*1.1), color='red',
                         horizontalalignment = "center",
                         verticalalignment = "center")
                axarr[i,j].text(1.05,0.5,mode+" "+shmode,
                size=labelsize,
                horizontalalignment = "center",
                verticalalignment = "center",
                transform=axarr[i,j].transAxes,
                bbox=dict(facecolor='w', alpha=0.5))
            j = j+1
        i = i+1
    
    for i in axarr[-1]:
        i.set_xlabel("$\itm/z$",size=labelsize)
    for i in axarr.T[0]:
        i.set_ylabel("%",size=labelsize)
    j = 0
    sublabels = ['a)','b)','c)','d)']
    for i in axarr.T[0]:
        i.text(0.1,0.95,sublabels[j],
               size=labelsize,
               horizontalalignment = "center",
               verticalalignment = "center",
               transform=i.transAxes)
        j=j+1
        
    for x in axarr:
        for y in x:
            y.spines['right'].set_visible(False)
            y.spines['top'].set_visible(False)
            
    
    fig.subplots_adjust(hspace=0.1)
    fig.savefig(outpath+sample+"/"+sample+"-"+polarity+".eps",dpi=300)
    fig.savefig(outpath+sample+"/"+sample+"-"+polarity+"highres.png",dpi=600)
    fig.savefig(outpath+sample+"/"+sample+"-"+polarity+".png",dpi=300)


"""
def subplot(data,xlim,file,source,shmode):
    labelsize = 20
    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot(111)
    ax.plot(data,c='k',linewidth=1.5)
    ax.set_xlim(xlim)
    ymax = float(df[(df.index > xlim[0]) & (df.index < xlim[1])].max().values)
    ax.set_ylim(0-ymax*0.05,ymax*1.05)
    #ax.set_title(source+" "+shmode)
    ax.text(0.9,0.9,source+" "+shmode,
            size=labelsize,
            horizontalalignment = "right",
            verticalalignment = "top",
            transform=ax.transAxes)
    ax.set_xlabel("$\itm/z$",size=labelsize)
    ax.set_ylabel("%",size=labelsize)
    ax.tick_params(axis="both",which="major",left="on",bottom="on",top="off",right="off",labelsize=labelsize)
    ax.tick_params(axis="both",which="minor",left="on",bottom="on",top="off",right="off")
    #ax.xaxis.set_major_locator(ticker.MaxNLocator(3))
    #ax.yaxis.set_major_locator(ticker.MaxNLocator(3))
    ax.xaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
    ax.yaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
    fig.tight_layout()
    fig.savefig(outpath+str(file)[:-3]+"_"+str(xlim[0])+"_"+str(xlim[1])+".png",dpi=300)


files = os.listdir(inpath)

#file = files[0]
xlims = [(100,1000),
         (363.0,376.3),
         (364.94,365.35)]


for file in files:
    source = str(file)[:-3].split(sep='-')[2]
    mode = str(file)[:-3].split(sep='-')[3]
    if mode == "Positive":
        shmode = "(+)"
    else:
        shmode = "(-)"
    df = pd.read_csv(inpath+file,sep=" ",index_col=0,names=["I"])
    df["I"] = df["I"]/df["I"].max()*100
    for xlim in xlims:
        subplot(df,xlim,file,source,shmode)
"""




#axarr[0,0].set_ylabel("%",size=labelsize)
"""
i,j=0,0    
for x in modes:
    j= 0
    for y in xlims: 
        print(i,j)
        j = j+1
    i = i+1
"""

"""
xlim = (100,1000)

fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111)
line = ax.plot(df)
ax.set_xlim(xlim)
ax.set_ylim((0-100*0.05,100*1.05))
ax.set_title(str(file)[:-3])
ax.set_xlabel("$\itm/z$")
ax.set_ylabel("%")

xlim = (353.0,353.3)
xlim = (363.0,376.3)
"""



