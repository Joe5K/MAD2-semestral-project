from analyticky_ukol.multilayer_graph import MultiLayerGraph

graph = MultiLayerGraph(filename="data/data.txt")

for index, (name, layer) in enumerate(graph.layers.items()):
    if index > 2:
        break

    print(f"Layer {name}")

    print(f"Pocet vrcholu: {layer.nodes_count}")
    print(f"Pocet hran: {layer.edges_count}")
    print(f"Hustota: {layer.density}")

    print(f"Priemerny stupen: {layer.average_degree}")
    print(f"Maximalny stupen: {layer.max_degree}")
    print(f"Distribucia: obrazky")

    print(f"Priemerny shlukovaci koeficient: {layer.get_average_clustering_coefficient()}")

    print(f"Pocet komponent: {len(layer.get_component_sizes())}")
    print(f"Distribucia velkosti komponent: obrazky")

    print("Vizualizace: obrazky")

    print("")

    layer.save_to_file(f"layers/{name}.csv", separator=";")

    layer.plot_distribution(f"Layer {name}", "degrees")
    layer.plot_distribution(f"Layer {name}", "degrees", "cumulative")

    layer.plot_distribution(f"Layer {name}", "component_sizes")
    layer.plot_distribution(f"Layer {name}", "component_sizes", "cumulative")
