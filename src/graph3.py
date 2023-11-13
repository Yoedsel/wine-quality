from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral11
import pandas as pd
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.resources import CDN

# Load data
data = pd.read_csv("Wine quality dataset.csv", index_col=0)

# Group by 'Type' and find the wine with the highest alcohol content in each group
highest_alcohol = data.groupby('Type')['alcohol'].idxmax()
highest_alcohol_data = data.loc[highest_alcohol, ['Type', 'alcohol']]

# Create a Bokeh figure
fig = figure(x_range=highest_alcohol_data['Type'].unique(), height=350, width =1190, title='Wine with Highest Alcohol Content',
           toolbar_location=None, tools='')

# Use factor_cmap for color mapping
colors = factor_cmap('Type', palette=Spectral11, factors=highest_alcohol_data['Type'].unique())
source = ColumnDataSource(highest_alcohol_data)

# Plot the bar chart
fig.vbar(x='Type', top='alcohol', width=0.9, source=source, line_color="white", fill_color=colors)

# Customize the plot
fig.title.text_font_size = '16pt'
fig.xaxis.major_label_text_font_size = '14pt'
fig.yaxis.major_label_text_font_size = '14pt'
fig.xaxis.axis_label_text_font_size = '14pt'
fig.yaxis.axis_label_text_font_size = '14pt'



# Show the plot
f = gridplot([[fig]])

# Embed components
js2, div2 = components(f)
cdn_jss2 = CDN.js_files[0]
