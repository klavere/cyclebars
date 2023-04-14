import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_anom_horizontal(dfA, dfB = pd.DataFrame(), # one or two dataframes consisting of n rows for n bins and 4 columns, the first containig bin labels, the second containing absolute values, the third containing reference values and the forth containing anomalies with respect to those reference values.
                         ax = 0, # the axes on which the diagram is to be be plotted
                         refMax = None, # a reference maximum, determines the scale.
                         negColor = '#404040', # custom color for negative anomalies
                         posColor = '#1a9641', # custom color for positive anomalies
                         refColor = '#BFBFBF', # custom color for reference values
                         accentcolor = 'white', # custom color for accent line
                         sdColor = 'grey', # custom color for standard deviation
                         middleLabels = False, # deafult: the labels appear between the bars, like on a clock. If set to True, the labels and ticks are plotted in the middle of each bar.
                         plot_legend = True, # if False, no legends will be plotted.
                        ):

    ### set up axes if not given
    #################################
    ### determine whether it's one or two plots
    singleDf = True if dfB.empty else False
    if not ax:
        fig = plt.figure()
        ax = fig.add_subplot()    
    ### determine position of labels
    middleLabelOffset = 0 if middleLabels else -0.5
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
            ref_sd_bars = [r + s for r, s in zip(dfA.reference, dfA.sd)]
            maxReference = max(ref_sd_bars)
        maxBar = max(maxValue, maxReference)
        base = -.03*(maxBar if not refMax else refMax)
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
        if with_sd:
            ref_sd_bars_a = [r + s for r, s in zip(dfA.reference, dfA.sd)]
            maxReferenceA = max(ref_sd_bars_a)
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
        if with_sd:
            ref_sd_bars_b = [r + s for r, s in zip(dfB.reference, dfB.sd)]
            maxReferenceB = max(ref_sd_bars_b)
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
        base = -.03*((maxBarA+maxBarB) if not refMax else (2*refMax))
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
    ### widths and angles
    barWidth=0.9
    anomWidth=0.9*3/4
    sdWidth=0.9/4
    ### colors
    alpha=1
    PosNegCol = {True: posColor, False: negColor}
    #################################
    
    ### stack bars
    #################################
    if singleDf:
        ### reference values
        ax.bar(xticks, dfA.reference, width=barWidth, alpha=alpha, color=refColor)
        ### anomalies
        ax.bar(xticks, dfA.anomaly, width=anomWidth, alpha=alpha, color=(dfA.anomaly > 0).map(PosNegCol), bottom=dfA.reference)
        if with_sd:
            ### standard deviations
            ax.bar(xticks, 2*dfA.sd, width=sdWidth, alpha=alpha, color=sdColor, bottom=dfA.reference-dfA.sd)
    else:
        ### reference values A
        ax.bar(xticks, dfA.reference, width=barWidth, alpha=alpha, color=refColor)
        ### anomalies A
        ax.bar(xticks, dfA.anomaly, width=anomWidth, alpha=alpha, color=(dfA.anomaly > 0).map(PosNegCol), bottom=dfA.reference)
        if with_sd:
            ### standard deviations A
            ax.bar(xticks, 2*dfA.sd, width=sdWidth, alpha=alpha, color=sdColor, bottom=dfA.reference-dfA.sd)
        ### reference values B
        bottomBarValues = [base]*len(binNames)
        negReferences = [bValue*(-1) for bValue in dfB.reference]
        ax.bar(xticks, negReferences, width=barWidth, alpha=alpha, color=refColor, bottom=bottomBarValues)
        ### anomalies B
        negAnoms = [bValue*(-1) for bValue in dfB.anomaly]
        bottomBarValuesAnom = [base+bValue*(-1) for bValue in dfB.reference]
        ax.bar(xticks, negAnoms, width=anomWidth, alpha=alpha, color=(dfB.anomaly > 0).map(PosNegCol), bottom=bottomBarValuesAnom)
        if with_sd:
            ### standard deviations B
            ax.bar(xticks, (-2)*dfB.sd, width=sdWidth, alpha=alpha, color=sdColor, bottom=bottomBarValuesAnom+dfB.sd)
    #################################
        
    ### max lines and yticks
    #################################
    if singleDf:
        ax.set_yticks([maxBar, .75*maxBar, .5*maxBar, .25*maxBar, 0])
        ax.set_yticklabels([str(np.round(maxBar, 2)),'','','',0], color='gray', size=9)
        ax.axhline(y=maxBar, color='gray', linewidth=1)
        ax.axhline(y=.5*base, color=accentcolor, linewidth=12, zorder=0)
    else:
        negticks = [base, base-.25*maxBarB, base-.5*maxBarB, base-.75*maxBarB, base-maxBarB]
        negticklabels = [0,'','','',str(np.round(maxBarB, 2))]
        ax.set_yticks([maxBarA, .75*maxBarA, .5*maxBarA, .25*maxBarA, 0] + negticks)
        ax.set_yticklabels([str(np.round(maxBarA, 2)),'','','',0] + negticklabels, color='gray', size=9)
        ax.axhline(y=maxBarA, color='gray', linewidth=1)
        ax.axhline(y=base-maxBarB, color='gray', linewidth=2)
        ax.axhline(y=.5*base, color=accentcolor, linewidth=12, zorder=0)
    #################################
    
    ### adapt plot scale if ref_max_a (and b) are given
    #################################
    if refMax:
        ax.set_ylim(top=refMax)
        ax.axhline(y=refMax, color='gray', linewidth=2)
        if not singleDf:
            ax.set_ylim(bottom=base-refMax)
            ax.axhline(y=base-refMax, color='gray', linewidth=2)
    #################################
    
    ### legends
    #################################
    if plot_legend:
        patches = [plt.Rectangle((0,0),1,1, edgecolor=PosNegCol[True], facecolor=PosNegCol[False], linewidth=2.5),
                plt.Rectangle((0,0),1,1, fill=False, edgecolor='none', visible=False),
                plt.Rectangle((0,0),1,1, fill=False, edgecolor='none', visible=False)]
        if singleDf:
            legendLabels = ['Anomalies: ' + str(np.round(totalAnomaly, decimals=2)) + ' total',
                            'Values: ' + str(np.round(totalValues, decimals=2)) + ' total',
                            str(100+(np.round((totalAnomaly/totalReference)*100, decimals=2))) + '% of reference values']
            axtwin = ax.twinx()
            axtwin.set_yticks([])
            axtwin.set_yticklabels([])
            for spine in ['left','right','top','bottom']:
                axtwin.spines[spine].set_visible(False)
            axtwin.legend(patches, legendLabels,
                        loc='lower center',
                        bbox_to_anchor=(0.5,-0.1),
                        ncol=3)
        else:
            ### legendA
            legendLabelsA = ['Anomalies: ' + str(np.round(totalAnomalyA, decimals=2)) + ' total',
                            'Values: ' + str(np.round(totalValuesA, decimals=2)) + ' total',
                            str(100+(np.round((totalAnomalyA/totalReferenceA)*100, decimals=2))) + '% of reference values']
            ax.legend(patches, legendLabelsA,
                    loc='upper center',
                    bbox_to_anchor=(0.5,1.1),
                    ncol=3)
            ### legendB
            legendLabelsB = ['Anomalies: ' + str(np.round(totalAnomalyB, decimals=2)) + ' total',
                            'Values: ' + str(np.round(totalValuesB, decimals=2)) + ' total',
                            str(100+(np.round((totalAnomalyB/totalReferenceB)*100, decimals=2))) + '% of reference values']
            axtwin = ax.twinx()
            for spine in ['left','right','top','bottom']:
                axtwin.spines[spine].set_visible(False)
            axtwin.set_yticks([])
            axtwin.set_yticklabels([])
            axtwin.legend(patches, legendLabelsB,
                        loc='lower center',
                        bbox_to_anchor=(0.5,-0.1),
                        ncol=3)
        return ax, axtwin
    #################################
    else:
        return ax