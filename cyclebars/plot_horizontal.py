import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def plot_horizontal(dfA, dfB = pd.DataFrame(), # one or two dataframes consisting of n rows for n bins and m+1 columns, the first containig bin labels, the rest values of m sub series.
                    ax = 0, # the axes on which the diagram is to be be plotted
                    # refMax = 0, # a global maximum for reference, determines the size of the pie chart in the middle of the plot.
                    colors = {}, # a dict of colours, indexed by the sub series names (
                    colormap = 'tab10', # the name of a colormap (see matplotlib.cm package)
                    middleLabels = False, # deafult: the labels appear between the bars, like on a clock. If set to True, the labels and ticks are plotted in the middle of each bar.
                    accentcolor = 'gray', # colour for max lines
                    plot_legend = True, # if False, no legends will be plotted.
                   ):

    singleDf = True if dfB.empty else False

    if not ax:
        fig = plt.figure()
        ax = fig.add_subplot()
        
    middleLabelOffset = 0 if middleLabels else -0.5
    
    ### get data from dfs
    #################################
    ### Column Names
    cycleName = dfA.columns[0]
    binNames = dfA[cycleName] # Labels for bins (y tick labels)
    if singleDf:
        subSeriesNames = [] # Column names of time subseries
        for k in range(len(dfA.columns)-1):
            subSeriesNames.append(dfA.columns[k+1])
    else:
        subSeriesNamesA = []
        for k in range(len(dfA.columns)-1):
            subSeriesNamesA.append(dfA.columns[k+1])
        subSeriesNamesB = []
        for k in range(len(dfB.columns)-1):
            subSeriesNamesB.append(dfB.columns[k+1])
        subSeriesNames = subSeriesNamesA + subSeriesNamesB
        subSeriesNames = list(pd.unique(subSeriesNames))
    #################################
    
    ### Maxs and Totals
    #################################
    if singleDf:
        subSeriesTotals = [] # Cycle totals of subSeries (slices in pie chart)
        for subSeries in subSeriesNames:
            subSeriesTotals.append(dfA[subSeries].sum())
        cycleTotal = sum(subSeriesTotals) # Total quantity of cycle (sum of totals of subseries) for size of pie chart
        binTotals = [] # Total sizes of bars in bins
        for binName in binNames:
            binTotals.append((dfA.loc[dfA[cycleName] == binName]).iloc[:,1:].sum(axis=1).values[0])
        maxBinTotal = max(binTotals) # Max bin total
        maxBinIndex = binTotals.index(maxBinTotal) # index of bin with max bin total
        maxBinName = binNames[maxBinIndex] # name of bin with max bin total (only first occurence if there are more than one)
        base = -.04*(maxBinTotal)
    else:
        ### for dfA
        #############################
        subSeriesTotalsA = [] # Cycle totals of subSeries
        for subSeries in subSeriesNamesA:
            subSeriesTotalsA.append(dfA[subSeries].sum())
        cycleTotalA = sum(subSeriesTotalsA) # Total quantity of cycle (sum of totals of subseries) for size of pie chart
        binTotalsA = [] # Total sizes of bars in bins
        for binName in binNames:
            binTotalsA.append((dfA.loc[dfA[cycleName] == binName]).iloc[:,1:].sum(axis=1).values[0])
        maxBinTotalA = max(binTotalsA) # Max bin total
        maxBinIndexA = binTotalsA.index(maxBinTotalA) # index of bin with max bin total
        maxBinNameA = binNames[maxBinIndexA] # name of bin with max bin total (only first occurence if there are more than one)
        ### for dfB
        #############################
        subSeriesTotalsB = [] # Cycle totals of subSeries
        for subSeries in subSeriesNamesB:
            subSeriesTotalsB.append(dfB[subSeries].sum())
        cycleTotalB = sum(subSeriesTotalsB) # Total quantity of cycle (sum of totals of subseries) for size of pie chart
        binTotalsB = [] # Total sizes of bars in bins
        for binName in binNames:
            binTotalsB.append((dfB.loc[dfB[cycleName] == binName]).iloc[:,1:].sum(axis=1).values[0])
        maxBinTotalB = max(binTotalsB) # Max bin total
        maxBinIndexB = binTotalsB.index(maxBinTotalB) # index of bin with max bin total
        maxBinNameB = binNames[maxBinIndexB] # name of bin with max bin total (only first occurence if there are more than one)
        ###
        ### joint max stuff (if necessary)
        ###
        maxBinTotal = max(maxBinTotalA, maxBinTotalB)
        base = -.04*(maxBinTotalA+maxBinTotalB)
    #################################
    
    ### set up plot
    #################################
    ax.yaxis.grid(linestyle = (0,(1,5)))
    for spine in ['left','right','top']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['bottom'].set_edgecolor(None)
    xticks = []
    xtickPos = []
    for i in range(len(binNames)):
        xticks.append(i)
        xtickPos.append(i+middleLabelOffset)
    ax.set_xticks(xtickPos)
    ax.set_xticklabels(binNames, color='gray', size=9)
    ax.tick_params(axis='both', which='both', length=0)
    ### width
    barWidth=0.9
    ### color
    alpha=1
    if not colors:
        colors = {subSeriesNames[i]: cm.get_cmap(colormap)(i) for i in range(len(subSeriesNames))} # colors for sub series, implement config option
    #################################
    
    ### stack bars
    #################################
    if singleDf:
        bottomBarValues = [0]*len(binNames)
        for subSeriesName in subSeriesNames:
            ax.bar(xticks,
                   dfA[subSeriesName],
                   width=barWidth,
                   alpha=alpha,
                   color=colors[subSeriesName],
                   bottom = bottomBarValues
                  )
            bottomBarValues = [a + b for a, b in zip(bottomBarValues, dfA[subSeriesName])]
    else:
        ### A bars
        bottomBarValues = [0]*len(binNames)
        for subSeriesName in subSeriesNamesA:
            ax.bar(xticks,
                   dfA[subSeriesName],
                   width=barWidth,
                   alpha=alpha,
                   color=colors[subSeriesName],
                   bottom = bottomBarValues
                  )
            bottomBarValues = [a + b for a, b in zip(bottomBarValues, dfA[subSeriesName])]
        ### B bars
        bottomBarValues = [base]*len(binNames)
        for subSeriesName in subSeriesNamesB:
            negValues = []
            negValues = [bValue*(-1) for bValue in dfB[subSeriesName]]
            ax.bar(xticks,
                   negValues,
                   width=barWidth,
                   alpha=alpha,
                   color=colors[subSeriesName],
                   bottom = bottomBarValues
                  )
            bottomBarValues = [a + b for a, b in zip(bottomBarValues, negValues)]
    #################################
    
    ### max lines and yticks
    #################################
    if singleDf:
        ax.set_yticks([maxBinTotal, .75*maxBinTotal, .5*maxBinTotal, .25*maxBinTotal, 0])
        ax.set_yticklabels([str(int(maxBinTotal)),'','','',0], color='gray', size=9)
        ax.axhline(y=maxBinTotal, color=accentcolor, linewidth=1)
    else:
        negticks = [base, base-.25*maxBinTotalB, base-.5*maxBinTotalB, base-.75*maxBinTotalB, base-maxBinTotalB]
        negticklabels = [0,'','','',str(int(maxBinTotalB))]
        ax.set_yticks([maxBinTotalA, .75*maxBinTotalA, .5*maxBinTotalA, .25*maxBinTotalA, 0] + negticks)
        ax.set_yticklabels([str(int(maxBinTotalA)),'','','',0] + negticklabels, color='gray', size=9)
        ax.axhline(y=maxBinTotalA, color=accentcolor, linewidth=1)
        ax.axhline(y=base-maxBinTotalB, color=accentcolor, linewidth=1)
    #################################

    ### legends
    #################################
    if plot_legend:
        if singleDf:
            legendTitle = 'Series total: '+str(np.round(cycleTotal, decimals=2))
            legendLabels = [subSeriesName + ': ' + str(np.round(subSeriesTotal, decimals=2))  +' total' for subSeriesName, subSeriesTotal in zip(subSeriesNames, subSeriesTotals)]
            patches = [plt.Rectangle((0,0),1,1, color=colors[subSeriesName]) for subSeriesName in subSeriesNames]
            axtwin = ax.twinx()
            axtwin.set_yticks([])
            axtwin.set_yticklabels([])
            for spine in ['left','right','top','bottom']:
                axtwin.spines[spine].set_visible(False)
            axtwin.legend(patches, legendLabels,
                    title=legendTitle,
                    loc='lower center',
                    bbox_to_anchor=(0.5,-0.1),
                    ncol=len(subSeriesNames))
        else:
            ### legendA
            legendTitleA = 'Series total: '+str(np.round(cycleTotalA, decimals=2))
            legendLabelsA = [subSeriesName + ': ' + str(np.round(subSeriesTotal, decimals=2))  +' total' for subSeriesName, subSeriesTotal in zip(subSeriesNamesA, subSeriesTotalsA)]
            patches = [plt.Rectangle((0,0),1,1, color=colors[subSeriesName]) for subSeriesName in subSeriesNamesA]
            ax.legend(patches, legendLabelsA,
                    title=legendTitleA,
                    loc='upper center',
                    bbox_to_anchor=(0.5,1.1),
                    ncol=len(subSeriesNamesA))

            ### legendB
            legendTitleB = 'Series total: '+str(np.round(cycleTotalB, decimals=2))
            legendLabelsB = [subSeriesName + ': ' + str(np.round(subSeriesTotal, decimals=2))  +' total' for subSeriesName, subSeriesTotal in zip(subSeriesNamesB, subSeriesTotalsB)]
            patches = [plt.Rectangle((0,0),1,1, color=colors[subSeriesName]) for subSeriesName in subSeriesNamesB]
            axtwin = ax.twinx()
            for spine in ['left','right','top','bottom']:
                axtwin.spines[spine].set_visible(False)
            axtwin.set_yticks([])
            axtwin.set_yticklabels([])
            axtwin.legend(patches, legendLabelsB,
                        title=legendTitleB,
                        loc='lower center',
                        bbox_to_anchor=(0.5,-0.1),
                        ncol=len(subSeriesNamesB))
    #################################
    
    return ax