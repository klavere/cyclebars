# Cyclebars

This package holds two different plotting functions built on matplotlib and pandas.
Both functions return a set of horizontal and circular bar charts.
They were developed for time-series of origin-destination (OD) data, i.e. data with an inherent bidirectionality and therefore also feature visual duality:
horizontal charts can be split horizontally (bars go up and down) and two circular charts are juxtaposed correspondingly.
`cyclebars()` is made for a set of time-series which are plotted as stacked bars.
`cyclebars_anomalies()` is made for analizing anomalies within a given time-series. Bars representing positive and negative anomalies are plotted on top of bars representing reference values.

## Installation

To install from github, run `pip install git+https://github.com/klavere/cyclebars.git#egg=cyclebars`

Instead, you may also download the code and run `pip install path/to/your/folder/cyclebars`

A conda install will be available eventually.

## cyclebars()

Returns a set of stacked bar charts in circular and horizontal manner.

`cyclebars(data, labels=None, columns_a=None, columns_b=None, ax_cyclic_a=0, ax_cyclic_b=0, ax_horizontal=0, colors={}, colormap='tab10', accentcolor='gray', middle_labels=False, theta_offset=-pi, theta_direction=-1, pie_offset=pi, ref_total=0, ref_maximum=None, plot_cyclic_only=False, plot_horizontal_only=False, plot_legends=True)`

### **Parameters:**

* **data** (pandas.DataFrame) - A dataframe containing all data to be plotted. The data frame should be sorted.

optional:

* **labels** (string) - The name of the column containig the labels for the bins. By default, the first column of your dataframe is taken.
* **columns_a** (List[string]) - A list of column names for n sub series. If none is given, `data.columns[1:]` are taken.
* **columns_b** (List[string]) - A list of column names for m sub series. If none is given, the plot will only feature one set of sub series, defined by `columns_a`.

* **ax_cyclic_a** (matplotlib.pyplot.Axes) - The axes on which the cyclic diagram showing sub series a is to be be plotted. The projection has to be polar.
* **ax_cyclic_b** (matplotlib.pyplot.Axes) - The axes on which the cyclic diagram showing sub series b is to be be plotted. The projection has to be polar.
* **ax_horizontal** (matplotlib.pyplot.Axes) - The axes on which the horizontal diagram is to be be plotted.

* **colors** (dict) - A dict of colours, indexed by the sub series column names.
* **colormap** (string) - The name of a colormap (please refer to the [`matplotlib.cm` package](https://matplotlib.org/stable/gallery/color/colormap_reference.html))
* **accentcolor** (string) - A colour for maximum lines and labels

* **middle_labels** (boolean) - Default: the labels appear between the bars, like on a clock. If set to True, the labels and ticks are plotted in the middle of each bar.
* **theta_offset** (radians) – Theta offset for bar chart.
* **theta_direction** (-1 or +1) – Theta direction for bar chart.
* **pie_offset** (radians) – Theta offset for pie chart, relative to theta_offset.

* **ref_total** (float) - A global maximum for reference. It determines the size of the pie chart in the middle of the plot.
* **ref_maximum** (float) - A global reference maximum, determines the scale of the bar plots.

* **plot_cyclic_only** (boolean) - If set `True`, only cyclic plots are returned. Only set `True` if `plot_horizontal_only` is `False`!
* **plot_horizontal_only** (boolean) - If set `True`, only horizontal plots are returned. Only set `True` if `plot_cyclic_only` is `False`!
* **plot_legends** (boolean) - If set `False`, no legends will be plotted.

## cyclebars_anomalies()

Returns a set of bar charts showing anomalies in circular and horizontal manner.

`cyclebars_anomalies(data, labels=None, values_a=None, reference_values_a=None, values_b=None, reference_values_b=None, ref_total=0, ref_maximum=None, ax_cyclic_a=0, ax_cyclic_b=0, ax_horizontal=0, color_negative_anomalies='#404040', color_positive_anomalies='#1a9641', color_reference_values='#BFBFBF', accentcolor='white', middle_labels=False, theta_offset=-pi, theta_direction=-1, pie_offset=pi/2, plot_cyclic_only=False, plot_horizontal_only=False, plot_legends=True`

### **Parameters:**

* **data** (pandas.DataFrame) - A dataframe containing all data to be plotted.

optional:

* **labels** (string) - The name of the column containig the labels for the bins. By default, the first column of your dataframe is taken.
* **values_a** (string) - The name of the column containig the values of time searies (a). Anomalies will be calculated as the difference between values and reference_values. By default, column 1 of your dataframe is taken.
* **reference_values_a** (string) - The name of the column containing the reference values for time series (a). Anomalies will be calculated as the difference between values and reference_values. By default, column 2 of your dataframe is taken.
* **values_b** (string) - The name of the column containig the values of time series (b). Anomalies will be calculated as the difference between values and reference_values. If none is given, only one time series (a) is plotted.
* **reference_values_b** (string) - The name of the column containing the reference values for time series (b). Anomalies will be calculated as the difference between values and reference_values. If none is given, only one time series (a) is plotted.

* **ref_total** (float) - A global maximum for reference. It determines the size of the pie chart in the middle of the plot.
* **ref_maximum** (float) - A reference maximum to determine the scale of the bar plots.

* **ax_cyclic_a**: (matplotlib.pyplot.Axes) - The axes on which the cyclic diagram showing sub series (a) is to be be plotted. The projection has to be polar.
* **ax_cyclic_b**: (matplotlib.pyplot.Axes) - The axes on which the cyclic diagram showing sub series (b) is to be be plotted. The projection has to be polar.
* **ax_horizontal** (matplotlib.pyplot.Axes) - The axes on which the horizontal diagram is to be be plotted.

* **color_negative_anomalies** (string) - A custom color for negative anomalies.
* **color_positive_anomalies** (string) - A custom color for positive anomalies.
* **color_reference_values** (string) - A custom color for reference values.
* **accentcolor** (string) - A custom color for accent lines.

* **middle_labels** (boolean) - By deafult, the labels appear between the bars, like on a clock. If set to `True`, the labels and ticks are plotted in the middle of each bar.

* **theta_offset** (radians) – Theta offset for bar chart.
* **theta_direction** (-1 or +1) – Theta direction for bar chart.
* **pie_offset** (radians) – Theta offset for pie chart, relative to theta_offset.

* **plot_cyclic_only** (boolean) - If set `True`, only cyclic plots are returned. Only set `True` if `plot_horizontal_only` is `False`!
* **plot_horizontal_only** (boolean) - If set `True`, only horizontal plots are returned. Only set `True` if `plot_cyclic_only` is `False`!
* **plot_legends** (boolean) - If set `False`, no legends will be plotted.

## Example data frames

### for `cyclebars()`:

|hour|A        |B       |C       |D      |E       |
|----|---------|--------|--------|-------|--------|
|0   |25031.61 |3843.39 |1307.99 |987.17 |2222.02 |
|1   |18924.31 |2517.40 |660.73  |753.59 |1690.69 |
|2   |21888.48 |2079.82 |378.35  |805.62 |2154.40 |
|3   |21036.61 |3193.61 |875.24  |679.59 |1757.61 |
|4   |39879.07 |8913.32 |3429.39 |1201.33|3275.44 |
|5   |77563.31 |16102.90|4705.14 |2202.66|5015.16 |
|6   |130171.66|23102.26|9027.68 |5055.05|9133.46 |
|7   |141516.26|19776.16|15000.62|8195.30|9713.37 |
|8   |138702.71|14202.19|9991.45 |6336.69|6804.40 |
|9   |142033.20|12094.38|7454.88 |4785.45|6405.72 |
|10  |157665.96|12374.43|7731.49 |4952.82|6966.78 |
|11  |178675.84|12960.96|9223.82 |5637.00|7826.98 |
|12  |184261.01|15173.89|10921.86|6171.69|8019.06 |
|13  |180940.24|15192.59|11008.57|5978.19|8020.28 |
|14  |186300.11|16737.27|12668.27|6680.34|8678.54 |
|15  |190704.98|19555.45|14212.09|7119.03|9529.78 |
|16  |185540.20|20771.32|15000.73|7293.66|11891.24|
|17  |169488.29|17886.29|14260.53|7124.84|10206.76|
|18  |136484.32|13517.53|10466.71|5753.31|8000.28 |
|19  |102844.19|10764.17|7935.59 |4069.98|5957.87 |
|20  |78359.46 |8886.99 |5417.82 |3291.62|4576.63 |
|21  |65456.94 |7837.54 |4373.37 |2727.74|4008.94 |
|22  |52841.36 |6822.65 |4076.25 |2190.18|3651.24 |
|23  |36917.88 |4808.17 |2515.86 |1616.39|2916.09 |

![An example plot made with the example dataframe](https://github.com/klavere/cyclebars/blob/version_1/exampledata/examplefigure.png?raw=true)

### for `cyclebars_anomalies()`:

|bins|val_a|val_b|ref_a|ref_b|
|----|-----|-----|-----|-----|
|0|14674.0|10481.43|17566.83|12547.74|
|1|8674.0|6195.71|12821.5|9158.21|
|2|12542.0|8958.57|17195.33|12282.38|
|3|12919.0|9227.86|19320.5|13800.36|
|4|35717.0|25512.14|50594.5|36138.93|
|5|85749.0|61249.29|108139.17|77242.26|
|6|177783.0|126987.86|201551.17|143965.12|
|7|198932.0|142094.29|228861.0|163472.14|
|8|168602.0|120430.0|191531.5|136808.21|
|9|152906.0|109218.57|174936.83|124954.88|
|10|167394.0|119567.14|136264.5|134390.71|
|11|130010.67|139297.14|109831.33|153710.95|
|12|132602.0|142073.57|109408.17|158640.6|
|13|129138.0|138362.14|110175.83|151906.55|
|14|208369.0|148835.0|177850.0|163367.86|
|15|226764.0|161974.29|246091.0|175779.29|
|16|235538.0|168241.43|244927.5|174948.21|
|17|216345.0|154532.14|221016.33|157868.81|
|18|168512.0|120365.71|163041.67|116458.33|
|19|122347.0|87390.71|112343.67|80245.48|
|20|77911.0|55650.71|86210.33|61578.81|
|21|65176.0|46554.29|67083.0|47916.43|
|22|61650.0|44035.71|45754.67|32681.9|
|23|30686.0|21918.57|28436.83|20312.02|

![An example plot made with the example dataframe](https://github.com/klavere/cyclebars/blob/version_1/exampledata/examplefigure_anomalies.png?raw=true)