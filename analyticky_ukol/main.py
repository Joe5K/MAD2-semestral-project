from analyticky_ukol.multilayer_graph import MultiLayerGraph

graph = MultiLayerGraph(filename="data/data.txt")

graph.save_graph("layers")

layer = graph.layers["1"]

layer.plot_distribution("degrees")
layer.plot_distribution("degrees", "cumulative")