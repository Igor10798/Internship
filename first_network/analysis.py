import pickle
import modules.graphs as graph

with open("offline_analysis/chart.pkl", "rb") as f:
    data = pickle.load(f)
graph.stacked_area(data["dead"], data["constant"], data["exploded"], "params_interaction/")

# with open("offline_analysis/chart.pkl", "rb") as f:
#     raw_data = pickle.load(f)
# graph.plot_raw(raw_data, "params_interaction/")