import pandas as pd
from typing import List
from math import pi
import matplotlib.pyplot as plt

from .plot_cyclic import plot_cyclic
from .plot_horizontal import plot_horizontal

def cyclebars(data: pd.DataFrame, # a dataframe containing all data to be plotted
              labels: str = None, # the name of the column containig the labels for the bins. default will be the first column of your dataframe.
              columns_a: List[str] = None, # a list of column names for n sub series
              columns_b: List[str] = None, # a list of column names for m sub series
              
              ax_cyclic_a: plt.Axes = 0, # the axes on which the cyclic diagram showing sub series a is to be be plotted
              ax_cyclic_b: plt.Axes = 0, # the axes on which the cyclic diagram showing sub series b is to be be plotted
              ax_horizontal: plt.Axes = 0, # the axes on which the horizontal diagram is to be be plotted
              
              colors: dict = {}, # a dict of colours, indexed by the sub series names
              colormap: str = 'tab10', # the name of a colormap (see matplotlib.cm package)
              accentcolor: str = 'gray', # colour for max lines and label
              middle_labels: bool = False, # deafult: the labels appear between the bars, like on a clock. If set to True, the labels and ticks are plotted in the middle of each bar.
              
              theta_offset = -pi,
              theta_direction = -1,
              pie_offset = pi, # theta offset for pie chart, relative to thetaOffset
              
              ref_total: float = 0, # a global maximum for reference, determines the size of the pie chart in the middle of the plot.
              ref_max_a: float = None, # a reference maximum, to determine the limits of the upper axis and the radial scale
              ref_max_b: float = None, # a reference maximum, to determine the limits of the lower axis and the radial scale
              
              plot_cyclic_only = False, # if True, only a cyclic plot is returned. Only set True if plot_horizontal_only is False!
              plot_horizontal_only = False, # if True, only a horizontal plot is given. Only set True if plot_cyclic_only is False!
              
              plot_legends = True, # if False, the legend or legends will not be plotted.
             ):
    
    ############################################
    ### prepare dataframe(s)
    ############################################
    
    if not labels:
        labels = data.columns[0]
    if not columns_a:
        columns_a = data.columns[1:].tolist()
    
    df_a = data[[labels]+columns_a]
    
    if columns_b:
        df_b = data[[labels]+columns_b]
        dual = True
    else:
        df_b = pd.DataFrame()
        dual = False
    
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
        cyclic_plots = plot_cyclic(
            dfA = df_a,
            dfB = df_b,
            axA = ax_cyclic_a,
            axB = ax_cyclic_b,
            refTotal = ref_total,
            refMaxA = ref_max_a,
            refMaxB = ref_max_b,
            colors = colors,
            colormap = colormap,
            thetaOffset = theta_offset,
            thetaDirection = theta_direction,
            pieOffset = pie_offset,
            middleLabels = middle_labels,
            accentcolor = accentcolor,
            plot_legend = plot_legends,
        )
        axes.append(cyclic_plots)
    
    if not plot_cyclic_only:
        horizontal_plot = plot_horizontal(
            dfA = df_a,
            dfB = df_b,
            ax = ax_horizontal,
            refMaxA = ref_max_a,
            refMaxB = ref_max_b,
            colors = colors,
            colormap = colormap,
            middleLabels = middle_labels,
            accentcolor = accentcolor,
            plot_legend = plot_legends,
        )
        axes.append(horizontal_plot)
    
    return axes