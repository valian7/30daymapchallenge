import osmnx as ox
import matplotlib.pyplot as plt

place = "Yogyakarta, Indonesia"

G = ox.graph_from_place(place, network_type="drive")

fig, ax = ox.plot_graph(
    G,
    bgcolor="black",
    node_size=0,
    edge_color="white",
    edge_linewidth=0.6,
    show=False,
    close=False,
)

fig.savefig(
    "output_maps/day01_yogyakarta_roads.png",
    dpi=300,
    bbox_inches="tight"
)