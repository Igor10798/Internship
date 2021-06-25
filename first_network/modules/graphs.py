import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "simple_white" # Sets the plotly default theme

def stacked_area(dead, constant, exploded, path):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x= dead.x, y= dead.y, mode='lines+markers', line_color= 'rgba(255, 16, 0, .8)', fill= 'tozeroy')) # fill down to xaxis
    fig.add_trace(go.Scatter(x= constant.x, y= constant.y, mode='lines+markers', line_color='rgba(250, 220, 0, .8)', fill='tonexty')) # fill to dead.y
    fig.add_trace(go.Scatter(x= exploded.x, y= exploded.y, mode='lines+markers', line_color='rgba(38, 250, 1, .8)', fill='tonexty')) # fill to constant.y
    fig.update_layout(xaxis_title="weight (pS)", yaxis_title= "connection probability")
    fig.show()
    fig.write_image('{}stacked.png'.format(path))
    fig.write_html('{}stacked.html'.format(path))

def plot_raw(*args, path):
    fig = go.Figure()
    for arg in args:
        fig.add_trace(go.Scatter(x= arg.dict["time_dead"], y= arg.dict["dead"], mode='lines', line_color= 'rgba(255, 16, 0, .8)'))
        fig.add_trace(go.Scatter(x= arg.dict["time_constant"], y= arg.dict["constant"], mode='lines', line_color='rgba(250, 220, 0, .8)'))
        fig.add_trace(go.Scatter(x= arg.dict["time_exploded"], y= arg.dict["exploded"], mode='lines', line_color='rgba(38, 250, 1, .8)'))
    fig.update_layout(xaxis_title="Time (ms)", yaxis_title= "spike frequency (Hz)")
    fig.show()
    fig.write_image('{}raw.png'.format(path))
    fig.write_html('{}raw.html'.format(path))