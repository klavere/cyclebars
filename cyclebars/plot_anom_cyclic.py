import pandas as pd
import numpy as np
from math import pi, radians
import matplotlib.pyplot as plt

def plot_anom_cyclic(dfA, dfB = pd.DataFrame(), # one or two dataframes consisting of n rows for n bins and 4 columns: ['bin', 'value', 'reference', 'anomaly']
                     axA = 0, # the axes on which the diagram A is to be be plotted
                     axB = 0, # the axes on which the diagram B is to be be plotted
                     refTotal = 0, # a global maximum for reference, determines the size of the pie chart in the middle of the plot.
                     refMax = None, # a reference maximum, determines the scale of the radial axis
                     negColor = '#404040', # custom color for negative anomalies
                     posColor = '#1a9641', # custom color for positive anomalies
                     refColor = '#BFBFBF', # custom color for reference values
                     accentcolor = 'white', # custom color for accent ring
                     sdColor = 'grey', # custom color for standard deviation
                     thetaOffset = -pi,
                     thetaDirection = -1,
                     pieOffset = 0, # theta offset for pie chart, relative to thetaOffset
                     middleLabels = False, # deafult: the labels appear between the bars, like on a clock. If set to True, the labels and ticks are plotted in the middle of each bar.
                     plot_legend = True, # if False, no legends will be plotted.
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
    if not list(dfA.columns.values) in [['bin', 'value', 'reference', 'anomaly'], ['bin', 'value', 'reference', 'anomaly', 'sd']]:
        return "please name your dataframe columns ['bin', 'value', 'reference', 'anomaly'] or ['bin', 'value', 'reference', 'anomaly', 'sd']."
    if not singleDf and not list(dfB.columns.values) in [['bin', 'value', 'reference', 'anomaly'], ['bin', 'value', 'reference', 'anomaly', 'sd']]:
        return "please name your dataframe columns ['bin', 'value', 'reference', 'anomaly'] or ['bin', 'value', 'reference', 'anomaly', 'sd']."
    #################################

    with_sd = False
    if 'sd' in list(dfA.columns.values):
        if singleDf:
            with_sd = True
        elif 'sd' in list(dfB.columns.values):
            with_sd = True
    
    ### get data from df
    #################################
    ### Column Names
    binNames = dfA.bin # Labels for bins (r tick labels)
    ### Max, Mins and Totals
    if singleDf:
        maxValue = dfA.value.max()
        maxReference = dfA.reference.max()
        if with_sd:
            dfA['ref_sd_bars'] = [r + s for r, s in zip(dfA.reference, dfA.sd)]
            maxReference = dfA.ref_sd_bars.max()
        maxBar = max(maxValue, maxReference)
        base = .6*(maxBar if not refMax else refMax)
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
        totalPositiveAnomaly = dfA[dfA['anomaly']>0].anomaly.sum()
        totalNegativeAnomaly = dfA[dfA['anomaly']<0].anomaly.abs().sum()
    else:
        ### for dfA
        #############################
        maxValueA = dfA.value.max()
        maxReferenceA = dfA.reference.max()
        if with_sd:
            dfA['ref_sd_bars'] = [r + s for r, s in zip(dfA.reference, dfA.sd)]
            maxReferenceA = dfA.ref_sd_bars.max()
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
        totalPositiveAnomalyA = dfA[dfA['anomaly']>0].anomaly.sum()
        totalNegativeAnomalyA = dfA[dfA['anomaly']<0].anomaly.abs().sum()
        ### for dfB
        #############################
        maxValueB = dfB.value.max()
        maxReferenceB = dfB.reference.max()
        if with_sd:
            dfB['ref_sd_bars'] = [r + s for r, s in zip(dfB.reference, dfB.sd)]
            maxReferenceB = dfB.ref_sd_bars.max()
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
        totalPositiveAnomalyB = dfB[dfB['anomaly']>0].anomaly.sum()
        totalNegativeAnomalyB = dfB[dfB['anomaly']<0].anomaly.abs().sum()
        ### 
        ### joint max stuff (if necessary)
        ###
        maxBar = max(maxBarA, maxBarB)
        base = .6*(maxBar if not refMax else refMax)
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
    sdWidth=barWidth/6
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
        if with_sd:
            ### standard deviations
            ax.bar(barAngles, 2*dfA.sd, width=sdWidth, alpha=alpha, color=sdColor, bottom=dfA.reference-dfA.sd)
    else:
        ### reference values A
        axA.bar(barAngles, dfA.reference, width=barWidth, alpha=alpha, color=refColor)
        ### anomalies A
        axA.bar(barAngles, dfA.anomaly, width=anomWidth, alpha=alpha, color=(dfA.anomaly > 0).map(PosNegCol), bottom = dfA.reference)
        if with_sd:
            ### standard deviations A
            axA.bar(barAngles, 2*dfA.sd, width=sdWidth, alpha=alpha, color=sdColor, bottom=dfA.reference-dfA.sd)
        ### reference values B
        axB.bar(barAngles, dfB.reference, width=barWidth, alpha=alpha, color=refColor)
        ### anomalies B
        axB.bar(barAngles, dfB.anomaly, width=anomWidth, alpha=alpha, color=(dfB.anomaly > 0).map(PosNegCol), bottom = dfB.reference)
        if with_sd:
            ### standard deviations B
            axB.bar(barAngles, 2*dfB.sd, width=sdWidth, alpha=alpha, color=sdColor, bottom=dfB.reference-dfB.sd)
    #################################
    
    ### pie chart
    #################################
    if not refTotal:
        refTotal = max(totalValues, totalReference) if singleDf else max(totalValuesA, totalReferenceA, totalValuesB, totalReferenceB)
    if singleDf:
        ### plot
        pieRadius = 0.95*base*max(totalReference, totalValues)/refTotal
        referenceValuesRadius = 0.95*base*totalReference/refTotal
        valuesRadius = 0.95*base*totalValues/refTotal
        posAnomalyAngle = radians((totalPositiveAnomaly/totalValues)*180)
        negAnomalyAngle = radians((totalNegativeAnomaly/totalReference)*180)
        #############################
        ### plot left half-circle for reference values
        ax.bar(pieOffset-(pi/2), referenceValuesRadius, width=pi, alpha=alpha,
               color=refColor, bottom=-base, zorder=10)
        ### plot bar on bottom left with angle showing negative anomalies
        ax.bar(pieOffset-pi+(negAnomalyAngle/2), referenceValuesRadius, width=negAnomalyAngle, alpha=alpha,
               color=negColor, bottom=-base, zorder=11)
        ### plot right half-circle for values
        ax.bar(pieOffset+(pi/2), valuesRadius, width=pi, alpha=alpha,
               color=refColor, bottom=-base, zorder=10)
        ### plot bar on top right with angle showing positive anomalies
        ax.bar(pieOffset+(posAnomalyAngle/2), valuesRadius, width=posAnomalyAngle, alpha=alpha,
               color=posColor, bottom=-base, zorder=11)
    else:
        ### plot
        pieRadius = 0.95*base*max(totalReferenceA, totalValuesA, totalReferenceB, totalValuesB)/refTotal
        referenceValuesRadiusA = 0.95*base*totalReferenceA/refTotal
        valuesRadiusA = 0.95*base*totalValuesA/refTotal
        referenceValuesRadiusB = 0.95*base*totalReferenceB/refTotal
        valuesRadiusB = 0.95*base*totalValuesB/refTotal
        posAnomalyAngleA = radians((totalPositiveAnomalyA/totalValuesA)*180)
        negAnomalyAngleA = radians((totalNegativeAnomalyA/totalReferenceA)*180)
        posAnomalyAngleB = radians((totalPositiveAnomalyB/totalValuesB)*180)
        negAnomalyAngleB = radians((totalNegativeAnomalyB/totalReferenceB)*180)
        ### plot A
        #############################
        ### plot left half-circle for reference values
        axA.bar(pieOffset-(pi/2), referenceValuesRadiusA, width=pi, alpha=alpha,
               color=refColor, bottom=-base, zorder=10)
        ### plot bar on bottom left with angle showing negative anomalies
        axA.bar(pieOffset-pi+(negAnomalyAngleA/2), referenceValuesRadiusA, width=negAnomalyAngleA, alpha=alpha,
               color=negColor, bottom=-base, zorder=11)
        ### plot right half-circle for values
        axA.bar(pieOffset+(pi/2), valuesRadiusA, width=pi, alpha=alpha,
               color=refColor, bottom=-base, zorder=10)
        ### plot bar on top right with angle showing positive anomalies
        axA.bar(pieOffset+(posAnomalyAngleA/2), valuesRadiusA, width=posAnomalyAngleA, alpha=alpha,
               color=posColor, bottom=-base, zorder=11)
        ### plot B
        #############################
        ### plot left half-circle for reference values
        axB.bar(pieOffset-(pi/2), referenceValuesRadiusB, width=pi, alpha=alpha,
               color=refColor, bottom=-base, zorder=10)
        ### plot bar on bottom left with angle showing negative anomalies
        axB.bar(pieOffset-pi+(negAnomalyAngleB/2), referenceValuesRadiusB, width=negAnomalyAngleB, alpha=alpha,
               color=negColor, bottom=-base, zorder=11)
        ### plot right half-circle for values
        axB.bar(pieOffset+(pi/2), valuesRadiusB, width=pi, alpha=alpha,
               color=refColor, bottom=-base, zorder=10)
        ### plot bar on top right with angle showing positive anomalies
        axB.bar(pieOffset+(posAnomalyAngleB/2), valuesRadiusB, width=posAnomalyAngleB, alpha=alpha,
               color=posColor, bottom=-base, zorder=11)
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
        ax.set_yticklabels([str(np.round(maxminAnomaly, 2)),'','','',''],
                           color = PosNegCol[True] if maxAnomaly>-minAnomaly else PosNegCol[False])
    else:
        axA.set_yticklabels([str(np.round(maxminAnomalyA, 2)),'','','',''],
                            color = PosNegCol[True] if maxAnomalyA>-minAnomalyA else PosNegCol[False])
        axB.set_yticklabels([str(np.round(maxminAnomalyB, 2)),'','','',''],
                            color = PosNegCol[True] if maxAnomalyB>-minAnomalyB else PosNegCol[False])
    #################################
    
    ### adapt plot scales if ref_max is given
    #################################
    if refMax:
        for subplot in subplots:
            subplot.set_ylim(top=refMax)
            subplot.add_artist(plt.Circle((0,0), base+refMax, transform=subplot.transData._b,
                fill=False, edgecolor='gray', linewidth=1, alpha=1, zorder=15))
    #################################
    
    ### legend
    #################################
    if plot_legend:
        patches = [plt.Rectangle((0,0),1,1, edgecolor=PosNegCol[True], facecolor=PosNegCol[False], linewidth=2.5),
                plt.Rectangle((0,0),1,1, fill=False, edgecolor='none', visible=False),
                plt.Rectangle((0,0),1,1, fill=False, edgecolor='none', visible=False)]
        if singleDf:
            legendLabels = ['Anomalies: ' + str(np.round(totalAnomaly, decimals=2)) + ' total',
                            'Values: ' + str(np.round(totalValues, decimals=2)) +' total',
                            str(100+(np.round((totalAnomaly/totalReference)*100, decimals=2))) + '% of reference values']
            ax.legend(patches, legendLabels, loc='upper left', bbox_to_anchor=(-0.2,1.1))
        else:
            legendLabelsA = ['Anomalies: ' + str(np.round(totalAnomalyA, decimals=2)) + ' total',
                            'Values: ' + str(np.round(totalValuesA, decimals=2)) + ' total',
                            str(100+(np.round((totalAnomalyA/totalReferenceA)*100, decimals=2))) + '% of reference values']
            axA.legend(patches, legendLabelsA, loc='upper left', bbox_to_anchor=(-0.2,1.1))
            legendLabelsB = ['Anomalies: ' + str(np.round(totalAnomalyB, decimals=2)) + ' total',
                            'Values: ' + str(np.round(totalValuesB, decimals=2)) + ' total',
                            str(100+(np.round((totalAnomalyB/totalReferenceB)*100, decimals=2))) + '% of reference values']
            axB.legend(patches, legendLabelsB, loc='upper left', bbox_to_anchor=(-0.2,1.1))
    #################################
    
    return ax if singleDf else axA, axB