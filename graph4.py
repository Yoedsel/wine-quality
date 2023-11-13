from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.resources import CDN
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20c
from bokeh.transform import factor_cmap

# Load data
data = pd.read_csv("Wine quality dataset.csv", index_col=0)

# Count the number of occurrences for each wine type
wine_counts = data['Type'].value_counts()

# Create a ColumnDataSource
source = ColumnDataSource(pd.DataFrame(wine_counts).reset_index().rename(columns={'index': 'Type', 'Type': 'Count'}))

# Create a Bokeh figure
output_file("wine_consumption.html")
fig = figure(x_range=data['Type'].unique(), height=400, width=1190, title='Wine Consumption by Type')

# Use factor_cmap for color mapping directly in the vbar glyph
# Use factor_cmap for color mapping directly in the vbar glyph
# Use a constant color for all bars
colors = 'skyblue'
bars = fig.vbar(x='Type', top='Count', width=0.9, source=source,
                line_color="white", fill_color=colors)



# Set labels and title
fig.xaxis.axis_label = 'Wine Type'
fig.yaxis.axis_label = 'Number of Occurrences'

f = gridplot([[fig]])

# Embed components
js3, div3 = components(f)
cdn_jss3 = CDN.js_files[0]


