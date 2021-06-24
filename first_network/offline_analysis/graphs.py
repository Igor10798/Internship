import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "simple_white" # Sets the plotly default theme

def stacked_area(dead, constant, exploded, path = r"first_network/params_interaction"):

    fig = go.Figure()
    fig.add_trace(go.Scatter(x= dead.x, y= dead.y, fill= 'tozeroy')) # fill down to xaxis
    fig.add_trace(go.Scatter(x= constant.x, y= constant.y, fill='tonexty')) # fill to dead.y
    fig.add_trace(go.Scatter(x= exploded.x, y= exploded.y, fill='tonexty')) # fill to constant.y

    fig.show()
    fig.write_image('{}stacked.png'.format(path))
