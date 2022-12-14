import pandas as pd
from math import pi
import matplotlib.pyplot as plt

from .plot_anom_cyclic import plot_anom_cyclic
from .plot_anom_horizontal import plot_anom_horizontal

def cyclebars_anomalies(data: pd.DataFrame, # a dataframe containing all data to be plotted
                        labels: str = None, # the name of the column containig the labels for the bins. Defaults to column 0 of your dataframe.
                        values_a:  str = None, # the name of the column containig the values (a). Anomalies will be calculated as the difference between values and reference_values. Defaults to column 1.
                        reference_values_a: str = None, # the name of the column containing the reference values (a). Anomalies will be calculated as the difference between values and reference_values. Defaults to column 2.
                        values_b:  str = None, # the name of the column containig the values (b). Anomalies will be calculated as the difference between values and reference_values.
                        reference_values_b: str = None, # the name of the column containing the reference values (b). Anomalies will be calculated as the difference between values and reference_values.
                        
                        ref_total: float = 0, # a global maximum for reference, determines the size of the pie chart in the middle of the plot.
                        ref_max_a: float = None, # a reference maximum, to determine the limits of the upper axis and the radial scale.
                        ref_max_b: float = None, # a reference maximum, to determine the limits of the lower axis and the radial scale. If none is given but ref_max_a is given, ref_max_b is set to ref_max_a. If ref_max_a is not given, ref_max_b will be ignored.
                        
                        ax_cyclic_a: plt.Axes = 0, # the axes on which the cyclic diagram showing sub series a is to be be plotted
                        ax_cyclic_b: plt.Axes = 0, # the axes on which the cyclic diagram showing sub series b is to be be plotted
                        ax_horizontal: plt.Axes = 0, # the axes on which the horizontal diagram is to be be plotted
                        
                        color_negative_anomalies = '#404040', # custom color for negative anomalies
                        color_positive_anomalies = '#1a9641', # custom color for positive anomalies
                        color_reference_values = '#BFBFBF', # custom color for reference values
                        accentcolor = 'white', # custom color for accent ring in cyclic plot #(and accent line in horizontal plot)
                        
                        middle_labels = False, # deafult: the labels appear between the bars, like on a clock. If set to True, the labels and ticks are plotted in the middle of each bar.
                        
                        theta_offset = -pi,
                        theta_direction = -1,
                        pie_offset = pi/2, # theta offset for pie chart, relative to thetaOffset
                        
                        plot_cyclic_only = False, # if True, only a cyclic plot is returned. Only set True if plot_horizontal_only is False!
                        plot_horizontal_only = False, # if True, only a horizontal plot is given. Only set True if plot_cyclic_only is False!
                        
                        plot_legends = True, # if False, no legends will be plotted.
                       ):
    
    ############################################
    ### prepare dataframe(s)
    ############################################
    
    if not labels:
        labels = data.columns[0]
    if not values_a:
        values_a = data.columns[1]
    if not reference_values_a:
        reference_values_a = data.columns[2]
    
    df_a = pd.DataFrame()    
    df_a['bin'] = data[[labels]].copy()
    df_a['value'] = data[[values_a]].copy()
    df_a['reference'] = data[[reference_values_a]].copy()
    df_a['anomaly'] = df_a.value - df_a.reference

    if values_b and reference_values_b:
        df_b = pd.DataFrame()    
        df_b['bin'] = data[[labels]].copy()
        df_b['value'] = data[[values_b]].copy()
        df_b['reference'] = data[[reference_values_b]].copy()
        df_b['anomaly'] = df_b.value - df_b.reference
        dual = True
    else:
        df_b = pd.DataFrame()
        dual = False
    
    ############################################
    ### set ref_max_b if only ref_max_a is given
    ############################################

    if ref_max_a:
        if not ref_max_b:
            ref_max_b = ref_max_a
    
    ############################################
    ### prepare figures where no axes are given:
    ############################################
    
    if plot_horizontal_only:
        fig = plt.figure(figsize=(20,10))
        if not ax_horizontal:
            ax_horizontal = fig.add_subplot()
    else:
        if dual:
            if plot_cyclic_only:
                fig = plt.figure(figsize=(20,10))
                if not ax_cyclic_a:
                    ax_cyclic_a = fig.add_subplot(121, projection='polar')
                if not ax_cyclic_b:
                    ax_cyclic_b = fig.add_subplot(122, projection='polar')
            else:
                fig = plt.figure(figsize=(20,20))
                if not ax_cyclic_a:
                    ax_cyclic_a = fig.add_subplot(221, projection='polar')
                if not ax_cyclic_b:
                    ax_cyclic_b = fig.add_subplot(222, projection='polar')
                if not ax_horizontal:
                    ax_horizontal = fig.add_subplot(2,2,(3,4))
        else:
            if plot_cyclic_only:
                fig = plt.figure(figsize=(10,10))
                if not ax_cyclic_a:
                    ax_cyclic_a = fig.add_subplot(projection='polar')
            else:
                fig = plt.figure(figsize=(30,10))
                if not ax_cyclic_a:
                    ax_cyclic_a = fig.add_subplot(1,3,(1,1), projection='polar')
                if not ax_horizontal:
                    ax_horizontal = fig.add_subplot(1,3,(2,3))
    
    ############################################
    ### call plotting functions
    ############################################    
    
    axes = []
    
    if not plot_horizontal_only:
        cyclic_plots = plot_anom_cyclic(
            dfA = df_a,
            dfB = df_b,
            axA = ax_cyclic_a,
            axB = ax_cyclic_b,
            refTotal = ref_total,
            refMaxA = ref_max_a,
            refMaxB = ref_max_b,
            negColor = color_negative_anomalies,
            posColor = color_positive_anomalies,
            refColor = color_reference_values,
            accentcolor = accentcolor,
            thetaOffset = theta_offset,
            thetaDirection = theta_direction,
            pieOffset = pie_offset,
            middleLabels = middle_labels,
            plot_legend = plot_legends,
        )
        axes.append(cyclic_plots)
    
    if not plot_cyclic_only:
        horizontal_plot = plot_anom_horizontal(
            dfA = df_a,
            dfB = df_b,
            ax = ax_horizontal,
            refMaxA = ref_max_a,
            refMaxB = ref_max_b,
            negColor = color_negative_anomalies,
            posColor = color_positive_anomalies,
            refColor = color_reference_values,
            accentcolor = accentcolor,
            middleLabels = middle_labels,
            plot_legend = plot_legends,
        )
        axes.append(horizontal_plot)

    return axes