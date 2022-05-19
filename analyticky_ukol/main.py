from analyticky_ukol.multilayer_graph import MultiLayerGraph

graph = MultiLayerGraph(filename="data/data.txt")

layer = graph.layers["1"]

layer.plot_distribution("component_sizes")
layer.plot_distribution("component_sizes", "cumulative")