import pandas as pd
import numpy as np
from math import pi, radians
import matplotlib.pyplot as plt
from matplotlib import cm

def plot_cyclic(dfA, dfB = pd.DataFrame(), # one or two dataframes consisting of n rows for n bins and m+1 columns, the first containig bin labels, the rest values of m sub series.
                axA = 0, # the axes on which the diagram A is to be be plotted
                axB = 0, # the axes on which the diagram B is to be be plotted
                refTotal = 0, # a global maximum for reference, determines the size of the pie chart in the middle of the plot.
                refMaxA = None, # a reference maximum, determines the scale of the radial axis
                refMaxB = None, # a reference maximum, determines the scale of the radial axis
                colors = {}, # a dict of colours, indexed by the sub series names (
                colormap = 'tab10', # the name of a colormap (see matplotlib.cm package)
                thetaOffset = -pi,
                thetaDirection = -1,
                pieOffset = pi, # theta offset for pie chart, relative to thetaOffset
                middleLabels = False, # deafult: the labels appear between the bars, like on a clock. If set to True, the labels and ticks are plotted in the middle of each bar.
                accentcolor = 'red', # colour for max label
                plot_legend = True, # if False, no legends will be plotted.
               ):
    
    singleDf = True if dfB.empty else False
    
    if singleDf:
        if not axA:
            fig = plt.figure(figsize=(8,8))
            ax = fig.add_subplot(projection='polar')
        else:
            ax = axA
        subplots = [ax] 
    else:
        if not axA or not axB:
            fig = plt.figure(figsize=(16,8))
            axA = fig.add_subplot(121, projection='polar')
            axB = fig.add_subplot(122, projection='polar')
        subplots = [axA, axB]
    
    middleLabelOffset = 0.5 if middleLabels else 0
    
    ### get data from df
    #################################
    ### Column Names
    cycleName = dfA.columns[0]
    binNames = dfA[cycleName] # Labels for bins (r tick labels)
    if singleDf:
        subSeriesNames = [] # Column names of time subseries
        for k in range(len(dfA.columns)-1):
            subSeriesNames.append(dfA.columns[k+1])
    else:
        subSeriesNamesA = [] # Column names of time subseries
        for k in range(len(dfA.columns)-1):
            subSeriesNamesA.append(dfA.columns[k+1])
        subSeriesNamesB = [] # Column names of time subseries
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
        base = .6*(maxBinTotal if not refMaxA else refMaxA) # base value needed for scales and sizes
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
        base = .6*maxBinTotal
        if refMaxA:
            base = .6*(max(refMaxA, refMaxB) if refMaxB else refMaxA)
    #################################
    
    ### set up plot
    #################################
    xticks = []
    for i in range(len(binNames)):
        xticks.append(radians((i+middleLabelOffset)*360/len(binNames)))
    yticks = list(pd.Series([1.1, 1, .75, .5, .25])*maxBinTotal)
    for subplot in subplots:
        subplot.set_theta_direction(thetaDirection)
        subplot.set_theta_offset(thetaOffset)
        if singleDf:
            subplot.set_rlabel_position((maxBinIndex+0.5)*(360/len(binNames)))
        subplot.yaxis.grid(linestyle = (0,(1,5)))
        subplot.spines['polar'].set_visible(False)
        subplot.set_rlim([-base,maxBinTotal])
        subplot.set_xticks(xticks)
        subplot.set_xticklabels(binNames, color='gray', size=9)
        subplot.set_yticks(yticks)
    if not singleDf:
        axA.set_rlabel_position((maxBinIndexA+0.5)*(360/len(binNames)))
        axB.set_rlabel_position((maxBinIndexB+0.5)*(360/len(binNames)))

    barAngles = [radians((b+.5)*360/len(binNames)) for b in range(len(binNames))] # angles to put bars at
    barWidth = radians(360/(len(binNames)+1)) # Width of individual bars - slighty slimmer than bins
    alpha = 1 # opacity of bars and pie chart
    if not colors:
        colors = {subSeriesNames[i]: cm.get_cmap(colormap)(i) for i in range(len(subSeriesNames))} # colors for sub series, implement config option
    #################################
    
    ### stack bars
    #################################
    if singleDf:
        bottomBarValues = [0]*len(binNames)
        for subSeriesName in subSeriesNames:
            ax.bar(barAngles,
                   dfA[subSeriesName],
                   width=barWidth,
                   alpha=alpha,
                   color=colors[subSeriesName],
                   bottom = bottomBarValues
                  )
            bottomBarValues = [a + b for a, b in zip(bottomBarValues, dfA[subSeriesName])]
    else:
        bottomBarValuesA = [0]*len(binNames)
        for subSeriesName in subSeriesNamesA:
            axA.bar(barAngles,
                    dfA[subSeriesName],
                    width=barWidth,
                    alpha=alpha,
                    color=colors[subSeriesName],
                    bottom = bottomBarValuesA
                   )
            bottomBarValuesA = [a + b for a, b in zip(bottomBarValuesA, dfA[subSeriesName])]
        bottomBarValuesB = [0]*len(binNames)
        for subSeriesName in subSeriesNamesB:
            axB.bar(barAngles,
                    dfB[subSeriesName],
                    width=barWidth,
                    alpha=alpha,
                    color=colors[subSeriesName],
                    bottom = bottomBarValuesB
                   )
            bottomBarValuesB = [a + b for a, b in zip(bottomBarValuesB, dfB[subSeriesName])]
    #################################
    
    ### pie chart
    #################################
    if not refTotal:
        refTotal = cycleTotal if singleDf else max(cycleTotalA, cycleTotalB)
    if singleDf:
        ### plot
        #############################
        pieRadius = 0.95*base*cycleTotal/refTotal
        pieAngles = {subSeriesNames[i]: radians((subSeriesTotals[i]/cycleTotal)*(360)) for i in range(len(subSeriesNames))}
    
        ax.add_artist(plt.Circle((0, 0), base, transform=ax.transData._b,
                             fill=True, color='#FFFFFF', alpha=1, zorder=5)) # white background
        bottomAngle = pieOffset
        for subSeriesName in subSeriesNames:
            ax.bar((bottomAngle+pieAngles[subSeriesName]/2), pieRadius, width=pieAngles[subSeriesName], alpha=alpha,
                   color=colors[subSeriesName], bottom=-base, zorder=10)
            bottomAngle += pieAngles[subSeriesName]
    else:
        ### plot A
        #############################
        pieRadiusA = 0.95*base*cycleTotalA/refTotal
        pieAnglesA = {subSeriesNamesA[i]: radians((subSeriesTotalsA[i]/cycleTotalA)*(360)) for i in range(len(subSeriesNamesA))}
    
        axA.add_artist(plt.Circle((0, 0), base, transform=axA.transData._b,
                                  fill=True, color='#FFFFFF', alpha=1, zorder=5)) # white background
        bottomAngleA = pieOffset
        for subSeriesName in subSeriesNamesA:
            axA.bar((bottomAngleA+pieAnglesA[subSeriesName]/2), pieRadiusA, width=pieAnglesA[subSeriesName], alpha=alpha,
                    color=colors[subSeriesName], bottom=-base, zorder=10)
            bottomAngleA += pieAnglesA[subSeriesName]
        ### plot B
        #############################
        pieRadiusB = 0.95*base*cycleTotalB/refTotal
        pieAnglesB = {subSeriesNamesB[i]: radians((subSeriesTotalsB[i]/cycleTotalB)*(360)) for i in range(len(subSeriesNamesB))}
    
        axB.add_artist(plt.Circle((0, 0), base, transform=axB.transData._b,
                                  fill=True, color='#FFFFFF', alpha=1, zorder=5)) # white background
        bottomAngleB = pieOffset
        for subSeriesName in subSeriesNamesB:
            axB.bar((bottomAngleB+pieAnglesB[subSeriesName]/2), pieRadiusB, width=pieAnglesB[subSeriesName], alpha=alpha,
                    color=colors[subSeriesName], bottom=-base, zorder=10)
            bottomAngleB += pieAnglesB[subSeriesName]
    #################################

    ### max circles and label
    #################################
    for subplot in subplots:
        subplot.add_artist(plt.Circle((0,0), base+maxBinTotal, transform=subplot.transData._b,
                                      fill=False, edgecolor='gray', linewidth=1, alpha=1, zorder=15))
    if singleDf:
        ax.set_yticklabels(['* max '+str(int(maxBinTotal)),'','','',''],color=accentcolor)
    else:
        axA.set_yticklabels(['* max '+str(int(maxBinTotalA)),'','','',''],color=accentcolor)
        axB.set_yticklabels(['* max '+str(int(maxBinTotalB)),'','','',''],color=accentcolor)
    #################################
    
    ### adapt plot scales if ref_max_a (and b) are given
    #################################
    if singleDf:
        if refMaxA:
            ax.set_ylim(top=refMaxA)
            ax.add_artist(plt.Circle((0,0), base+refMaxA, transform=ax.transData._b,
                                     fill=False, edgecolor='gray', linewidth=1, alpha=1, zorder=15))
    else:
        if refMaxA:
            axA.set_ylim(top=refMaxA)
            axA.add_artist(plt.Circle((0,0), base+refMaxA, transform=axA.transData._b,
                                      fill=False, edgecolor='gray', linewidth=1, alpha=1, zorder=15))
        if refMaxB:
            axB.set_ylim(top=refMaxB)
            axB.add_artist(plt.Circle((0,0), base+refMaxA, transform=axB.transData._b,
                                      fill=False, edgecolor='gray', linewidth=1, alpha=1, zorder=15))
    #################################
    
    ### legend
    #################################
    if plot_legend:
        if singleDf:
            legendTitle = 'Cycle total: '+str(np.round(cycleTotal, decimals=2))
            legendLabels = [subSeriesName + ': ' + str(np.round(subSeriesTotal, decimals=2))  +' total' for subSeriesName, subSeriesTotal in zip(subSeriesNames, subSeriesTotals)]
            patches = [plt.Rectangle((0,0),1,1, color=colors[subSeriesName]) for subSeriesName in subSeriesNames]
            ax.legend(patches, legendLabels, title=legendTitle, loc='upper left', bbox_to_anchor=(-0.2,1.3))
        else:
            legendTitleA = 'Cycle total: '+str(np.round(cycleTotalA, decimals=2))
            legendLabelsA = [subSeriesName + ': ' + str(np.round(subSeriesTotal, decimals=2))  +' total' for subSeriesName, subSeriesTotal in zip(subSeriesNamesA, subSeriesTotalsA)]
            patchesA = [plt.Rectangle((0,0),1,1, color=colors[subSeriesName]) for subSeriesName in subSeriesNamesA]
            axA.legend(patchesA, legendLabelsA, title=legendTitleA, loc='upper left', bbox_to_anchor=(-0.2,1.3))
                    
            legendTitleB = 'Cycle total: '+str(np.round(cycleTotalB, decimals=2))
            legendLabelsB = [subSeriesName + ': ' + str(np.round(subSeriesTotal, decimals=2))  +' total' for subSeriesName, subSeriesTotal in zip(subSeriesNamesB, subSeriesTotalsB)]
            patchesB = [plt.Rectangle((0,0),1,1, color=colors[subSeriesName]) for subSeriesName in subSeriesNamesB]
            axB.legend(patchesB, legendLabelsB, title=legendTitleB, loc='upper left', bbox_to_anchor=(-0.2,1.3))
    #################################
    
    return ax if singleDf else axA, axB
