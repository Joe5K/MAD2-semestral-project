from analyticky_ukol.multilayer_graph import MultiLayerGraph

graph = MultiLayerGraph(filename="data/data.txt")

for index, (name, layer) in enumerate(graph.layers.items()):
    if index > 2:
        break

    layer.save_to_file(f"layers/{name}.csv", separator=";")

    layer.plot_distribution(f"Layer {name}", "degrees")
    layer.plot_distribution(f"Layer {name}", "degrees", "cumulative")

    layer.plot_distribution(f"Layer {name}", "component_sizes")
    layer.plot_distribution(f"Layer {name}", "component_sizes", "cumulative")
