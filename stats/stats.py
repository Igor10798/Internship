import scipy
from scipy.stats import linregress
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

class RegressionImage:
    def __init__(self, x, regression_info):
        xmin = min(x)
        xmax = max(x)
        y1 = calc_regression_point(regression_info, xmin)
        y_fin = calc_regression_point(regression_info, xmax)
        self.x = [xmin, xmax]
        self.y = [y1, y_fin]

def calc_regression_point(regression_info, x=0):
    return x * regression_info.slope + regression_info.intercept

def obtain_regression_image(regression_info, domain):
    return RegressionImage(domain, regression_info)

def plot_regression(plot, yaxis, regr, x, y, info_regression):
    plot.add_trace(go.Scatter(x= x, y= y, mode= "markers"))
    plot.add_trace(go.Scatter(x= regr.x, y= regr.y, mode= "lines+text", name= "Regression", text=info_regression.rvalue**2))
    plot.update_layout(xaxis_title="g_L", yaxis_title=yaxis)
    plot.show()

g_Ls = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0, 101.0])
rheobase_freqs = np.array([11, 11, 11, 11, 20, 20, 20, 20, 20, 91, 91, 91, 95, 95, 123, 143, 143, 143, 143, 143, 164, 164, 164, 164, 225, 225, 225, 225, 225, 260, 260, 260, 260, 260, 260, 260, 260, 260, 260, 263, 263, 263, 263, 263, 263, 263, 337, 337, 337, 337, 372, 372, 372, 372, 372, 372, 372, 372, 372, 372, 372, 372, 570, 570, 594, 594, 594, 594, 594, 594, 594, 712, 712, 712, 712, 712, 712, 712, 712, 712, 712, 712, 712, 712])
freqs_350 = np.array([12.0, 11.0, 10.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 8.0, 8.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
freqs_500 = np.array([13.0, 12.0, 13.0, 11.0, 11.0, 11.0, 10.0, 10.0, 10.0, 9.0, 9.0, 9.0, 9.0, 9.0, 8.0, 8.0, 8.0, 8.0, 8.0, 7.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 5.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
freqs_750 = np.array([16.0, 16.0, 14.0, 14.0, 14.0, 14.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 11.0, 11.0, 11.0, 11.0, 11.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.0, 9.0, 8.0, 8.0, 8.0, 8.0, 8.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 6.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
freqs_1000 = np.array([18.0, 18.0, 18.0, 17.0, 17.0, 17.0, 17.0, 17.0, 17.0, 16.0, 16.0, 16.0, 16.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 14.0, 14.0, 13.0, 13.0, 13.0, 12.0, 12.0, 11.0, 11.0, 11.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
g_Ls_for_rheobase = g_Ls[:len(rheobase_freqs)]
freqs_350_nonzero = freqs_350[:np.count_nonzero(freqs_350)]
g_Ls_350 = g_Ls[:len(freqs_350_nonzero)]
freqs_500_nonzero = freqs_500[:np.count_nonzero(freqs_500)]
g_Ls_500 = g_Ls[:len(freqs_500_nonzero)]
freqs_750_nonzero = freqs_750[:np.count_nonzero(freqs_750)]
g_Ls_750 = g_Ls[:len(freqs_750_nonzero)]
freqs_1000_nonzero = freqs_1000[:np.count_nonzero(freqs_1000)]
g_Ls_1000 = g_Ls[:len(freqs_1000_nonzero)]

""" i don't want to lose all this stuff :(
results_rheobase = scipy.stats.linregress(g_Ls_for_rheobase, rheobase_freqs)
results_350 = scipy.stats.linregress(g_Ls, freqs_350)
results_500 = scipy.stats.linregress(g_Ls, freqs_500)
results_750 = scipy.stats.linregress(g_Ls, freqs_750)
results_1000 = scipy.stats.linregress(g_Ls, freqs_1000)

regr_rheobase = obtain_regression_image(results_rheobase, g_Ls_for_rheobase)
regr_350 = obtain_regression_image(results_350, g_Ls)
regr_500 = obtain_regression_image(results_500, g_Ls)
regr_750 = obtain_regression_image(results_750, g_Ls)
regr_1000 = obtain_regression_image(results_1000, g_Ls)

pio.templates.default = "simple_white" # Sets the plotly default theme
plot1 = px.scatter()
plot2 = px.scatter()
plot3 = px.scatter()
plot4 = px.scatter()
plot5 = px.scatter()

plot_regression(plot1, "Rheobase frequency", regr_rheobase, g_Ls_for_rheobase, rheobase_freqs, results_rheobase)
plot_regression(plot2, "Spikes/s at 350Hz input", regr_350, g_Ls, freqs_350, results_350)
plot_regression(plot3, "Spikes/s at 500Hz input", regr_500, g_Ls, freqs_500, results_500)
plot_regression(plot4, "Spikes/s at 750Hz input", regr_750, g_Ls, freqs_750, results_750)
plot_regression(plot5, "Spikes/s at 1000Hz input", regr_1000, g_Ls, freqs_1000, results_1000)
"""

results_rheobase = scipy.stats.linregress(g_Ls_for_rheobase, rheobase_freqs)
results_350 = scipy.stats.linregress(g_Ls_350, freqs_350_nonzero)
results_500 = scipy.stats.linregress(g_Ls_500, freqs_500_nonzero)
results_750 = scipy.stats.linregress(g_Ls_750, freqs_750_nonzero)
results_1000 = scipy.stats.linregress(g_Ls_1000, freqs_1000_nonzero)

regr_rheobase = obtain_regression_image(results_rheobase, g_Ls_for_rheobase)
regr_350 = obtain_regression_image(results_350, g_Ls_350)
regr_500 = obtain_regression_image(results_500, g_Ls_500)
regr_750 = obtain_regression_image(results_750, g_Ls_750)
regr_1000 = obtain_regression_image(results_1000, g_Ls_1000)

pio.templates.default = "simple_white" # Sets the plotly default theme
plot1 = px.scatter()
plot2 = px.scatter()
plot3 = px.scatter()
plot4 = px.scatter()
plot5 = px.scatter()

plot_regression(plot1, "Rheobase frequency", regr_rheobase, g_Ls_for_rheobase, rheobase_freqs, results_rheobase)
plot_regression(plot2, "Spikes/s at 350Hz input", regr_350, g_Ls_350, freqs_350_nonzero, results_350)
plot_regression(plot3, "Spikes/s at 500Hz input", regr_500, g_Ls_500, freqs_500_nonzero, results_500)
plot_regression(plot4, "Spikes/s at 750Hz input", regr_750, g_Ls_750, freqs_750_nonzero, results_750)
plot_regression(plot5, "Spikes/s at 1000Hz input", regr_1000, g_Ls_1000, freqs_1000_nonzero, results_1000)

np.savetxt('rheobase.csv', np.c_[g_Ls_for_rheobase, rheobase_freqs])
np.savetxt('input_350.csv', np.c_[g_Ls_350, freqs_350_nonzero])
np.savetxt('input_500.csv', np.c_[g_Ls_500, freqs_500_nonzero])
np.savetxt('input_750.csv', np.c_[g_Ls_750, freqs_750_nonzero])
np.savetxt('input_1000.csv', np.c_[g_Ls_1000, freqs_1000_nonzero])