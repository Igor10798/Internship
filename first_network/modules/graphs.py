import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "simple_white" # Sets the plotly default theme

def stacked_area(dead, constant, exploded):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x= dead.x, y= dead.y, mode='lines+markers', line_color= 'rgba(255, 16, 0, .8)', fill= 'tozeroy')) # fill down to xaxis
    fig.add_trace(go.Scatter(x= constant.x, y= constant.y, mode='lines+markers', line_color='rgba(250, 220, 0, .8)', fill='tonexty')) # fill to dead.y
    fig.add_trace(go.Scatter(x= exploded.x, y= exploded.y, mode='lines+markers', line_color='rgba(38, 250, 1, .8)', fill='tonexty')) # fill to constant.y
    fig.update_layout(xaxis_title="weight (pS)", yaxis_title= "connection probability")
    fig.show()
    return fig

def raw_histogram(x_axis, y_axis):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x= x_axis, y = y_axis, name="spike/s"))
    fig.update_layout(xaxis_title="Time (ms)", yaxis_title= "spike frequency (Hz)")
    return fig