import pandas as pd
import numpy as np
from math import pi, radians
import matplotlib.pyplot as plt

def plot_anom_cyclic(dfA, dfB = pd.DataFrame(), # one or two dataframes consisting of n rows for n bins and 4 columns: ['bin', 'value', 'reference', 'anomaly']
                     axA = 0, # the axes on which the diagram A is to be be plotted
                     axB = 0, # the axes on which the diagram B is to be be plotted
                     refTotal = 0, # a global maximum for reference, determines the size of the pie chart in the middle of the plot.
                     negColor = '#404040', # custom color for negative anomalies
                     posColor = '#1a9641', # custom color for positive anomalies
                     refColor = '#BFBFBF', # custom color for reference values
                     accentcolor = 'white', # custom color for accent ring
                     thetaOffset = -pi,
                     thetaDirection = -1,
                     pieOffset = pi/2, # theta offset for pipe chart, relative to thetaOffset
                     middleLabels = False, # deafult: the labels appear between the bars, like on a clock. If set to True, the labels and ticks are plotted in the middle of each bar.
                    ):
    
    ### set up axes if not given
    #################################
    ### determine whether it's one or two plots
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
    ### determine position of labels
    middleLabelOffset = 0.5 if middleLabels else 0
    #################################
    
    ### check columnnames in df
    #################################
    if not list(dfA.columns.values) == ['bin', 'value', 'reference', 'anomaly']:
        return "please name your dataframe columns ['bin', 'value', 'reference', 'anomaly']."
    if not singleDf and not list(dfB.columns.values) == ['bin', 'value', 'reference', 'anomaly']:
        return "please name your dataframe columns ['bin', 'value', 'reference', 'anomaly']."
    #################################
    
    ### get data from df
    #################################
    ### Column Names
    binNames = dfA.bin # Labels for bins (r tick labels)
    ### Max, Mins and Totals
    if singleDf:
        maxValue = dfA.value.max()
        maxReference = dfA.reference.max()
        maxBar = max(maxValue, maxReference)
        base = .6*maxBar
        ###
        maxAnomaly = dfA.anomaly.max()
        maxAnomalyIndex = list(dfA.anomaly).index(maxAnomaly)
        maxAnomalyBinName = dfA.bin[maxAnomalyIndex]
        ###
        minAnomaly = dfA.anomaly.min()
        minAnomalyIndex = list(dfA.anomaly).index(minAnomaly)
        minAnomalyBinName = dfA.bin[minAnomalyIndex]
        ###
        maxminAnomaly = max(maxAnomaly,-minAnomaly)
        maxminAnomalyIndex = maxAnomalyIndex if maxminAnomaly==maxAnomaly else minAnomalyIndex
        maxminAnomalyBinName = maxAnomalyBinName if maxminAnomaly==maxAnomaly else minAnomalyBinName
        ###
        totalValues = dfA.value.sum()
        totalReference = dfA.reference.sum()
        totalAnomaly = dfA.anomaly.sum()
    else:
        ### for dfA
        #############################
        maxValueA = dfA.value.max()
        maxReferenceA = dfA.reference.max()
        maxBarA = max(maxValueA, maxReferenceA)
        ###
        maxAnomalyA = dfA.anomaly.max()
        maxAnomalyIndexA = list(dfA.anomaly).index(maxAnomalyA)
        maxAnomalyBinNameA = dfA.bin[maxAnomalyIndexA]
        ###
        minAnomalyA = dfA.anomaly.min()
        minAnomalyIndexA = list(dfA.anomaly).index(minAnomalyA)
        minAnomalyBinNameA = dfA.bin[minAnomalyIndexA]
        ###
        maxminAnomalyA = max(maxAnomalyA,-minAnomalyA)
        maxminAnomalyIndexA = maxAnomalyIndexA if maxminAnomalyA==maxAnomalyA else minAnomalyIndexA
        maxminAnomalyBinNameA = maxAnomalyBinNameA if maxminAnomalyA==maxAnomalyA else minAnomalyBinNameA
        ###
        totalValuesA = dfA.value.sum()
        totalReferenceA = dfA.reference.sum()
        totalAnomalyA = dfA.anomaly.sum()
        ### for dfB
        #############################
        maxValueB = dfB.value.max()
        maxReferenceB = dfB.reference.max()
        maxBarB = max(maxValueB, maxReferenceB)
        ###
        maxAnomalyB = dfB.anomaly.max()
        maxAnomalyIndexB = list(dfB.anomaly).index(maxAnomalyB)
        maxAnomalyBinNameB = dfB.bin[maxAnomalyIndexB]
        ###
        minAnomalyB = dfB.anomaly.min()
        minAnomalyIndexB = list(dfB.anomaly).index(minAnomalyB)
        minAnomalyBinNameB = dfB.bin[minAnomalyIndexB]
        ###
        maxminAnomalyB = max(maxAnomalyB,-minAnomalyB)
        maxminAnomalyIndexB = maxAnomalyIndexB if maxminAnomalyB==maxAnomalyB else minAnomalyIndexB
        maxminAnomalyBinNameB = maxAnomalyBinNameB if maxminAnomalyB==maxAnomalyB else minAnomalyBinNameB
        ###
        totalValuesB = dfB.value.sum()
        totalReferenceB = dfB.reference.sum()
        totalAnomalyB = dfB.anomaly.sum()
        ### 
        ### joint max stuff (if necessary)
        ###
        maxBar = max(maxBarA, maxBarB)
        base = .6*maxBar
    #################################
    
    ### set up plot
    #################################
    xticks = []
    for i in range(len(binNames)):
        xticks.append(radians((i+middleLabelOffset)*360/len(binNames)))
    yticks = list(pd.Series([1.1, 1, .75, .5, .25])*maxBar)
    for subplot in subplots:
        subplot.set_theta_direction(thetaDirection)
        subplot.set_theta_offset(thetaOffset)
        if singleDf:
            subplot.set_rlabel_position((maxminAnomalyIndex+0.5)*(360/len(binNames)))
        subplot.yaxis.grid(linestyle = (0,(1,5)))
        subplot.spines['polar'].set_visible(False)
        subplot.set_rlim([-base,maxBar])
        subplot.set_xticks(xticks)
        subplot.set_xticklabels(binNames, color='gray', size=9)
        subplot.set_yticks(yticks)
    if not singleDf:
        axA.set_rlabel_position((maxminAnomalyIndexA+0.5)*(360/len(binNames)))
        axB.set_rlabel_position((maxminAnomalyIndexB+0.5)*(360/len(binNames)))
    ### widths and angles
    barAngles = [radians((b+.5)*360/len(binNames)) for b in range(len(binNames))] # angles to put bars at
    barWidth = radians(360/(len(binNames)+1)) # Width of individual bars - slighty slimmer than bins
    anomWidth = barWidth*3/4
    ### colors
    alpha = 1 # opacity of bars and pie chart
    PosNegCol = {True: posColor, False: negColor}
    #################################
    
    ### stack bars
    #################################
    if singleDf:
        ### reference values
        ax.bar(barAngles, dfA.reference, width=barWidth, alpha=alpha, color=refColor)
        ### anomalies
        ax.bar(barAngles, dfA.anomaly, width=anomWidth, alpha=alpha, color=(dfA.anomaly > 0).map(PosNegCol), bottom = dfA.reference)
    else:
        ### reference values A
        axA.bar(barAngles, dfA.reference, width=barWidth, alpha=alpha, color=refColor)
        ### anomalies A
        axA.bar(barAngles, dfA.anomaly, width=anomWidth, alpha=alpha, color=(dfA.anomaly > 0).map(PosNegCol), bottom = dfA.reference)
        ### reference values B
        axB.bar(barAngles, dfB.reference, width=barWidth, alpha=alpha, color=refColor)
        ### anomalies B
        axB.bar(barAngles, dfB.anomaly, width=anomWidth, alpha=alpha, color=(dfB.anomaly > 0).map(PosNegCol), bottom = dfB.reference)
    #################################
    
    ### pie chart
    #################################
    if not refTotal:
        refTotal = totalValues if singleDf else max(totalValuesA, totalValuesB)
    if singleDf:
        ### plot
        #############################
        anomColor = PosNegCol[True] if totalAnomaly>0 else PosNegCol[False]
        pieRadius = 0.95*base*totalValues/refTotal
        anomalyAngle = radians((totalAnomaly/totalValues)*360)
        ax.add_artist(plt.Circle((0, 0), pieRadius, transform=ax.transData._b,
                                 fill=True, color=refColor, alpha=1, zorder=8))
        ax.bar(pieOffset, pieRadius, width=anomalyAngle, alpha=alpha,
               color=anomColor, bottom=-base, zorder=10)
    else:
        ### plot A
        #############################
        anomColorA = PosNegCol[True] if totalAnomalyA>0 else PosNegCol[False]
        pieRadiusA = 0.95*base*totalValuesA/refTotal
        anomalyAngleA = radians((totalAnomalyA/totalValuesA)*360)
        axA.add_artist(plt.Circle((0, 0), pieRadiusA, transform=axA.transData._b,
                                  fill=True, color=refColor, alpha=1, zorder=8))
        axA.bar(pieOffset, pieRadiusA, width=anomalyAngleA, alpha=alpha,
                color=anomColorA, bottom=-base, zorder=10)
        ### plot B
        #############################
        anomColorB = PosNegCol[True] if totalAnomalyB>0 else PosNegCol[False]
        pieRadiusB = 0.95*base*totalValuesB/refTotal
        anomalyAngleB = radians((totalAnomalyB/totalValuesB)*360)
        axB.add_artist(plt.Circle((0, 0), pieRadiusB, transform=axB.transData._b,
                                  fill=True, color=refColor, alpha=1, zorder=8))
        axB.bar(pieOffset, pieRadiusB, width=anomalyAngleB, alpha=alpha,
                color=anomColorB, bottom=-base, zorder=10)
    #################################

    ### max circles and label
    #################################
    for subplot in subplots:
        subplot.add_artist(plt.Circle((0,0), base+maxBar, transform=subplot.transData._b,
                                      fill=False, edgecolor='gray', linewidth=1, alpha=1, zorder=15))
        subplot.add_artist(plt.Circle((0, 0), base, transform=subplot.transData._b,
                                      fill=True, color=accentcolor, alpha=1, zorder=5)) # accent color ring
        subplot.add_artist(plt.Circle((0, 0), .95*base, transform=subplot.transData._b,
                                      fill=True, color='#FFFFFF', alpha=1, zorder=6)) # white background
    if singleDf:
        ax.set_yticklabels([str(int(maxminAnomaly)),'','','',''],
                           color = PosNegCol[True] if maxAnomaly>-minAnomaly else PosNegCol[False])
    else:
        axA.set_yticklabels([str(int(maxminAnomalyA)),'','','',''],
                            color = PosNegCol[True] if maxAnomalyA>-minAnomalyA else PosNegCol[False])
        axB.set_yticklabels([str(int(maxminAnomalyB)),'','','',''],
                            color = PosNegCol[True] if maxAnomalyB>-minAnomalyB else PosNegCol[False])
    #################################
    
    ### legend
    #################################
    patches = [plt.Rectangle((0,0),1,1, color=refColor),
               plt.Rectangle((0,0),1,1, edgecolor=PosNegCol[True], facecolor=PosNegCol[False], linewidth=2.5)]
    if singleDf:
        legendLabels = ['Values: ' + str(np.round(totalValues, decimals=2))  +' total',
                        'Anomalies: ' + str(np.round(totalAnomaly, decimals=2))  +' total']
        ax.legend(patches, legendLabels, loc='upper left', bbox_to_anchor=(-0.2,1.1))
    else:
        legendLabelsA = ['Values: ' + str(np.round(totalValuesA, decimals=2))  +' total',
                         'Anomalies: ' + str(np.round(totalAnomalyA, decimals=2))  +' total']
        axA.legend(patches, legendLabelsA, loc='upper left', bbox_to_anchor=(-0.2,1.1))
        legendLabelsB = ['Values: ' + str(np.round(totalValuesB, decimals=2))  +' total',
                         'Anomalies: ' + str(np.round(totalAnomalyB, decimals=2))  +' total']
        axB.legend(patches, legendLabelsB, loc='upper left', bbox_to_anchor=(-0.2,1.1))
    #################################
    
    return ax if singleDf else axA, axB