import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Viridis256
from bokeh.models import HoverTool
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.resources import CDN

# Load data
data = pd.read_csv("Wine quality dataset.csv", index_col=0)

# Find the most acidic wine
most_acidic_wine = data.loc[data['pH'].idxmin()]

# Create a ColumnDataSource
source = ColumnDataSource(data)

# Create a Bokeh figure
output_file("most_acidic_wine.html")
fig = figure(x_range=data['Type'].unique(), height=400, width=1190, title='Most Acidic Wine by Type')

# Create bars using the vbar glyph
bars = fig.vbar(x='Type', top='pH', width=0.9, source=source, line_color="white", fill_color=factor_cmap('Type', palette=Viridis256, factors=data['Type'].unique()))

# Set labels and title
fig.xaxis.axis_label = 'Wine Type'
fig.yaxis.axis_label = 'pH'

# Add hover tool
hover = HoverTool()
hover.tooltips = [("Type", "@Type"), ("pH", "@pH{0.00}")]
fig.add_tools(hover)

# Show the plot
# show(fig)



# Show the plot
f = gridplot([[fig]])


# Embed components
js1, div1 = components(f)
cdn_jss1 = CDN.js_files[0]
