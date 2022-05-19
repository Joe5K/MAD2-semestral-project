from analyticky_ukol.multilayer_graph import MultiLayerGraph

graph = MultiLayerGraph(filename="data/data.txt")

layer = graph.layers["1"]

print(layer.get_distribution("component_sizes"))
print(layer.get_distribution("component_sizes", "cumulative"))