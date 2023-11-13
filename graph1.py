import pandas as pd
import numpy as np
from math import pi
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256
from bokeh.models import ColorBar
# from bokeh.layouts import layout
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt 
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, ColorBar
from bokeh.io import output_file
# from bokeh.models import FactorRange
from bokeh.models.tools import HoverTool
from bokeh.models import Range1d
from bokeh.transform import cumsum, factor_cmap, linear_cmap
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.resources import CDN

data=pd.read_csv("Wine quality dataset.csv",index_col=0)

wine_cnt = data.groupby(by=["Type"]).count()[['alcohol']].rename(columns={"alcohol":"Count"}).reset_index()
wine_cnt['angle'] = wine_cnt['Count'] / wine_cnt['Count'].sum() * 2 * pi


a = data.groupby(['pH'])['alcohol'].sum()


# Graph 1

output_file("histogram.html")

# Aggregate alcohol by pH
aggregated_data = data.groupby('pH')['alcohol'].sum().reset_index()

# Calculate histogram
hist, edges = np.histogram(data['pH'], bins=20)

# Create a ColumnDataSource for the hover tool
source = ColumnDataSource(data=dict(
    left=edges[:-1],
    right=edges[1:],
    hist=hist
))

# Create figure
fig1 = figure(title='Histogram of Relationship between pH values and Frequency',
              x_axis_label='pH', y_axis_label='Frequency',
              height=500, width=600)

# Plot histogram
hist_renderer = fig1.quad(top='hist', bottom=0, left='left', right='right', source=source, fill_color='#b541cc', line_color='black')

# Customize axis and labels
fig1.yaxis.major_label_orientation = "vertical"
fig1.xaxis.minor_tick_line_color = "black"
fig1.xaxis.minor_tick_in = 2
fig1.xaxis.axis_label = "pH"
fig1.yaxis.axis_label = "Frequency"
fig1.axis.axis_label_text_color = "black"
fig1.axis.major_label_text_color = "black"
fig1.title.align = "center"

# Create hover tool
hover = HoverTool(renderers=[hist_renderer],
                  tooltips=[('pH Range', '@left{0.00} to @right{0.00}'), ('Frequency', '@hist')],
                  mode='vline')

# Add hover tool to the figure
fig1.add_tools(hover)

# Graph 2

output_file("line.html")
Y = list(a.index)

fig2 = figure(x_range=Range1d(start=min(a.index), end=max(a.index)), width=570, height=500, title="Alcohol content based on volatile acid")
fig2.title.text_font_size = '16pt'
fig2.title.align = "center"

fig2.yaxis.major_label_orientation = "vertical"
fig2.xaxis.visible = True

fig2.xaxis.minor_tick_line_color = "black"
fig2.yaxis.major_label_orientation = "horizontal"
fig2.xaxis.minor_tick_in = 2
fig2.xaxis.axis_label = "Volatile acid"
fig2.yaxis.axis_label = "Alcohol"
fig2.axis.axis_label_text_color = "black"
fig2.axis.major_label_text_color = "black"
# fig2.axis.axis_label_text_font = "Fantasy"
hover_tool = HoverTool(
    tooltips=[
        ('Volatile Acid', '@x{0.2f}'),  # Display volatile acid with two decimal places
        ('Alcohol Content', '@y{0.2f}')  # Display alcohol content with two decimal places
    ],
    mode='vline'  # Show tooltips only when the mouse is vertically over a point
)

# Add the hover tool to the figure
fig2.add_tools(hover_tool)
fig2.yaxis.formatter.use_scientific = False

# Use line instead of vbar for line graph
fig2.line(x=Y, y=a, line_width=2, line_color='#83c5be')

#Graph 3

output_file("pie.html")
colors = ['#e31a1c', '#1f78b4']  # Red and Blue

# Create a ColumnDataSource
source = ColumnDataSource(wine_cnt)

# Create a Bokeh figure
fig3 = figure(height=500, title="Wine Samples Distribution Per Type", toolbar_location=None,
              tools="hover", tooltips="@Type: @Count", x_range=(-1, 1))

# Plot the wedge chart using ColumnDataSource
fig3.wedge(x=0, y=1, radius=0.4,
           start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
           line_color="white",line_width = 2, fill_color=factor_cmap('Type', palette=colors, factors=wine_cnt['Type']),
           legend_field='Type', source=source)

# Customize axis and grid
fig3.axis.axis_label = None
fig3.axis.visible = False
fig3.grid.grid_line_color = None

# Add legend
fig3.legend.title = 'Wine Type'

# Add hover tool
hover = HoverTool()
hover.tooltips = [("Type", "@Type"), ("Count", "@Count")]
fig3.add_tools(hover)

# graph 4

# Convert 'quality' to string to avoid ValueError
data['quality'] = data['quality'].astype(str)

# Create a ColumnDataSource from the DataFrame
source = ColumnDataSource(data)

# Create a linear color map based on the 'quality' column
color_mapper = linear_cmap(field_name='quality', palette=Viridis256, low=min(data['quality'].astype(int)), high=max(data['quality'].astype(int)))

# Create a Bokeh figure
fig = figure(x_range=data['quality'].unique(), y_range=(0, 1.3), height=500, width=600, title='Relationship between Density and Quality')

# Create vertical bars using the vbar glyph
bars = fig.vbar(x='quality', top='density', width=0.9, source=source, line_color="white", fill_color=color_mapper)

# Set labels and title
fig.xaxis.axis_label = 'Quality'
fig.yaxis.axis_label = 'Density'

# Add color bar
color_bar = ColorBar(color_mapper=color_mapper['transform'], width=8, location=(0, 0))
fig.add_layout(color_bar, 'right')

# Add hover tool
# hover = HoverTool()
# hover.tooltips = [("Quality", "@quality"), ("Density", "@density{0.00}")]
# fig.add_tools(hover)

# Graph 5

correlation_matrix = data.corr()

# Convert correlation matrix to long format
corr_data = correlation_matrix.unstack().reset_index(name='value')
corr_data.columns = ['variable1', 'variable2', 'value']

# Create a Bokeh figure
fig5 = figure(
    width=600, height=600,
    x_range=list(correlation_matrix.index),
    y_range=list(correlation_matrix.columns),
    toolbar_location=None,
    tools='',
    title='Correlation'
)

# Create a color mapper
colors = linear_cmap(field_name='value', palette=Viridis256, low=-1, high=1)
source = ColumnDataSource(corr_data)

# Create rectangles for the heatmap
rects = fig5.rect(
    x='variable2', y='variable1', width=1, height=1,
    source=source, line_color=None,
    fill_color=colors, fill_alpha=0.6
)

# Add hover tool
fig5.add_tools(
    HoverTool(
        tooltips=[('Variables', '@variable1, @variable2'), ('Correlation', '@value')],
        mode='mouse', point_policy='follow_mouse'
    )
)

# Add color bar
color_bar = ColorBar(color_mapper=colors['transform'], width=8, location=(0, 0))
fig5.add_layout(color_bar, 'right')

# Customize plot aesthetics
fig5.xaxis.major_label_orientation = 45
fig5.xaxis.axis_label_text_font_size = "14pt"
fig5.yaxis.axis_label_text_font_size = "14pt"
fig5.title.text_font_size = '16pt'


# graph 6
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Viridis256
import pandas as pd

# Assuming your data is stored in a DataFrame named 'df'
# You may need to replace 'df' with your actual DataFrame name

# Create a ColumnDataSource
source = ColumnDataSource(data)

# Create a Bokeh figure
output_file("acidity_perception.html")
fig6 = figure(width=600, height=600, title='Impact of pH on Acidity Perception by Wine Quality',
             x_axis_label='pH', y_axis_label='Volatile Acidity')

# Use factor_cmap for color mapping
colors = factor_cmap('quality', palette=Viridis256, factors=sorted(data['quality'].unique()))

# Create a scatter plot
fig6.scatter(x='pH', y='volatile acidity', size=8, color=colors, legend_field='quality', source=source, fill_alpha=0.6)

# Set labels and title
fig6.legend.title = 'Wine Quality'
fig6.xaxis.axis_label = 'pH'
fig6.yaxis.axis_label = 'Volatile Acidity'

# Add hover tool
hover = HoverTool()
hover.tooltips = [("pH", "@pH{0.00}"), ("Volatile Acidity", "@{volatile acidity}{0.00}"), ("Quality", "@quality")]
fig6.add_tools(hover)
# Show the plot
# show(p)


# Create grid layout
# f = gridplot([[fig1, fig2], [fig3, fig], [fig5]])
f = gridplot([[fig1, fig3],[fig, fig2], [fig5, fig6]])


# Embed components
js, div = components(f)
cdn_jss = CDN.js_files[0]


















