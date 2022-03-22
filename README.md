# Cyclebars
This package currently holds four different plotting functions built on matplotlib and pandas

- [plot_horizontal()](#plot_horizontal())
- [plot_cyclic()](#plot_cyclic())
- [plot_anom_horizontal()](#plot_anom_horizontal())
- [plot_anom_cyclic()](#plot_anom_cyclic())

## Installation
To install from github, run `pip install git+https://github.com/klavere/cyclebars.git#egg=cyclebars`

Instead, you may also download the code and run `pip install path/to/your/folder/cyclebars`

A conda install will be available eventually.

## plot_horizontal()
Plots a stacked horizontal bar chart of one or two pandas DataFrames.

`cyclebars.plot_horizontal(dfA, dfB=pd.DataFrame(), ax=0, colors={}, colormap='Set1', middleLabels=False, accentcolor='gray')`

### **Parameters:**
- **dfA** (pandas.DataFrame) – a dataframe consisting of n rows for n bins and m+1 columns, the first containing bin labels, the others containing values of m sub series.
- **dfB** (pandas.DataFrame) – optional second data frame with n rows and k+1 columns, the first containing bin labels, the others containing values of k sub series. The sub series can but do not need to be identical with those of the first data frame.
- **ax** (matplotlib.Axes) – the axes on which the diagram is to be plotted
- **colors** (dict) – a dictionary of colours, indexed by the names of all sub series
- **colormap** (string) – the name of a colormap, see https://matplotlib.org/stable/gallery/color/colormap_reference.html
- **middleLabels** (bool) – by default, the labels appear between the bars. If set to True, the labels and ticks are plotted in the middle of each bar.
- **accentcolor** (string) – the name of a colour for lines representing maxima

## plot_cyclic()
Plots one or two stacked circular bar charts of one or two pandas DataFrames.

`cyclebars.plot_cyclic(dfA, dfB=pd.DataFrame(), axA=0, axB=0, refTotal=0, colors={}, colormap='Set1', thetaOffset=-pi, thetaDirection=-1, pieOffset=pi, middleLabels=False, accentcolor='red')`

### **Parameters:**
- **dfA** (pandas.DataFrame) – a dataframe consisting of n rows for n bins and m+1 columns, the first containing bin labels, the others containing values of m sub series.
- **dfB** (pandas.DataFrame) – optional second data frame with n rows and k+1 columns, the first containing bin labels, the others containing values of k sub series. The sub series can but do not need to be identical with those of the first data frame.
- **axA** (matplotlib.Axes) – the axes on which the diagram A is to be plotted
- **axB** (matplotlib.Axes) – the axes on which the diagram B is to be plotted
- **refTotal** (number) – a global maximum for reference. It determines the size of the pie chart in the middle of the plot.
- **colors** (dict) – a dictionary of colours, indexed by the names of all sub series
- **colormap** (string) – the name of a colormap, see https://matplotlib.org/stable/gallery/color/colormap_reference.html
- **thetaOffset** (radians) – theta offset for bar chart
- **thetaDirection** (-1 or +1) – theta direction for bar chart
- **pieOffset** (radians) – theta offset for pie chart, relative to thetaOffset
- **middleLabels** (bool) – by default, the labels appear between the bars. If set to True, the labels and ticks are plotted in the middle of each bar.
- **accentcolor** (string) – the name of a colour for maximum labels

## plot_anom_horizontal()
Plots a stacked horizontal bar chart of anomalies saved in one or two data frames.

`cyclebars.plot_anom_horizontal(dfA, dfB = pd.DataFrame(), ax=0, negColor='#404040', posColor='#1a9641', refColor='#BFBFBF', middleLabels=False)`

### **Parameters:**
- **dfA** (pandas.DataFrame) – a dataframe consisting of n rows for n bins and 4 columns, the first containig bin labels (labeled 'bin'), the second containing absolute values (labeled 'values'), the third containing reference values (labeled 'reference') and the forth containing anomalies with respect to those reference values (labeled 'anomaly'). The data frame should be sorted.
- **dfB** (pandas.DataFrame) –  an optional second dataframe consisting of n rows for n bins and 4 columns, the first containig bin labels (labeled 'bin'), the second containing absolute values (labeled 'values'), the third containing reference values (labeled 'reference') and the forth containing anomalies with respect to those reference values (labeled 'anomaly'). The data frame should be sorted.
- **ax** (matplotlib.Axes) – the axes on which the diagram is to be be plotted
- **negColor** (string) – custom color for negative anomalies
- **posColor** (string) – custom color for positive anomalies
- **refColor** (string) – custom color for reference values
- **middleLabels** (bool) – by default, the labels appear between the bars. If set to True, the labels and ticks are plotted in the middle of each bar.

## plot_anom_cyclic()
Plots one or two stacked cyclic bar chart of anomalies saved in one or two data frames.

`cyclebars.plot_anom_horizontal(dfA, dfB = pd.DataFrame(), ax=0, negColor='#404040', posColor='#1a9641', refColor='#BFBFBF', middleLabels=False)`

### **Parameters:**
- **dfA** (pandas.DataFrame) – a dataframe consisting of n rows for n bins and 4 columns (['bin', 'value', 'reference', 'anomaly']), the first containig bin labels (labeled 'bin'), the second containing absolute values (labeled 'values'), the third containing reference values (labeled 'reference') and the forth containing anomalies with respect to those reference values (labeled 'anomaly'). The data frame should be sorted.
- **dfB** (pandas.DataFrame) –  an optional second dataframe consisting of n rows for n bins and 4 columns (['bin', 'value', 'reference', 'anomaly']), the first containig bin labels (labeled 'bin'), the second containing absolute values (labeled 'values'), the third containing reference values (labeled 'reference') and the forth containing anomalies with respect to those reference values (labeled 'anomaly'). The data frame should be sorted.
- **axA** (matplotlib.Axes) – the axes on which diagram A is to be be plotted
- **axB** (matplotlib.Axes) – the axes on which diagram B is to be be plotted
- **negColor** (string) – custom color for negative anomalies
- **posColor** (string) – custom color for positive anomalies
- **refColor** (string) – custom color for reference values
- **accentcolor** (string) – custom color for accent ring
- **thetaOffset** (radians) – theta offset for bar charts
- **thetaDirection** (-1 or +1) – theta direction for bar charts
- **pieOffset** (radians) – theta offset for pie charts, relative to thetaOffset
- **middleLabels** (bool) – by default, the labels appear between the bars. If set to True, the labels and ticks are plotted in the middle of each bar.

## Example data frames

### for `plot_horizontal()` and `plot_cyclic()`:

|hour|A          |B          |C          |D          |E          |
|----|-----------|-----------|-----------|-----------|-----------|
|0   |25031.61429|3843.392857|1307.985714|987.1714286|2222.021429|
|1   |18924.3119 |2517.402381|660.7333333|753.5880952|1690.685714|
|2   |21888.47857|2079.816667|378.35     |805.6214286|2154.404762|
|3   |21036.60714|3193.614286|875.2428571|679.5857143|1757.607143|
|4   |39879.07143|8913.319048|3429.388095|1201.32619 |3275.435714|
|5   |77563.30714|16102.89762|4705.140476|2202.659524|5015.161905|
|6   |130171.6643|23102.2619 |9027.67619 |5055.045238|9133.464286|
|7   |141516.2571|19776.1619 |15000.62381|8195.304762|9713.366667|
|8   |138702.7143|14202.19286|9991.445238|6336.688095|6804.397619|
|9   |142033.1976|12094.37619|7454.878571|4785.452381|6405.716667|
|10  |157665.9595|12374.43333|7731.485714|4952.82381 |6966.780952|
|11  |178675.8429|12960.9619 |9223.819048|5637       |7826.97619 |
|12  |184261.0143|15173.89286|10921.85714|6171.688095|8019.057143|
|13  |180940.2429|15192.58571|11008.56905|5978.190476|8020.280952|
|14  |186300.1119|16737.27143|12668.27381|6680.340476|8678.542857|
|15  |190704.9786|19555.45   |14212.08571|7119.033333|9529.783333|
|16  |185540.1976|20771.31905|15000.72857|7293.661905|11891.23571|
|17  |169488.2929|17886.2881 |14260.52619|7124.838095|10206.76429|
|18  |136484.3167|13517.53095|10466.7119 |5753.314286|8000.280952|
|19  |102844.1905|10764.17143|7935.590476|4069.97619 |5957.866667|
|20  |78359.45952|8886.992857|5417.821429|3291.616667|4576.628571|
|21  |65456.94048|7837.540476|4373.366667|2727.738095|4008.940476|
|22  |52841.3619 |6822.647619|4076.247619|2190.180952|3651.235714|
|23  |36917.87857|4808.171429|2515.864286|1616.392857|2916.088095|

### for `plot_anom_horizontal()` and `plot_anom_cyclic`:

|bin|value |reference  |anomaly     |
|---|------|-----------|------------|
|0  |14674 |17566.83333|-2892.833333|
|1  |8674  |12821.5    |-4147.5     |
|2  |12542 |17195.33333|-4653.333333|
|3  |12919 |19320.5    |-6401.5     |
|4  |35717 |50594.5    |-14877.5    |
|5  |85749 |108139.1667|-22390.16667|
|6  |177783|201551.1667|-23768.16667|
|7  |198932|228861     |-29929      |
|8  |168602|191531.5   |-22929.5    |
|9  |152906|174936.8333|-22030.83333|
|10 |167394|188147     |-20753      |
|11 |195016|215195.3333|-20179.33333|
|12 |198903|222096.8333|-23193.83333|
|13 |193707|212669.1667|-18962.16667|
|14 |208369|228715     |-20346      |
|15 |226764|246091     |-19327      |
|16 |235538|244927.5   |-9389.5     |
|17 |216345|221016.3333|-4671.333333|
|18 |168512|163041.6667|5470.333333 |
|19 |122347|112343.6667|10003.33333 |
|20 |77911 |86210.33333|-8299.333333|
|21 |65176 |67083      |-1907       |
|22 |61650 |45754.66667|15895.33333 |
|23 |30686 |28436.83333|20000       |