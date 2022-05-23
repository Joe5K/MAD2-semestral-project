from itertools import combinations
from analyticky_ukol.multilayer_graph import MultiLayerGraph

graph = MultiLayerGraph(filename="data/data.txt")

all_actors = set()
for layer in graph.layers.values():
    all_actors.update(layer._nodes_adjs.keys())

layer_combinations = []
for i in range(len(graph.layers)):
    layer_combinations.extend(list(combinations(graph.layers.keys(), i+1)))


class Property:
    def __init__(self, name):
        self.name = name
        self.actor = None
        self.layers = None
        self.value = -float("inf")


biggest = [
    Property("degree"),
    Property("neighborhood"),
    Property("connective_redundancy"),
    Property("exclusive_neighborhood"),
]

for count, layer_combination in enumerate(layer_combinations):
    for actor in all_actors:
        for prop in biggest:
            value = getattr(graph, prop.name)(actor, layer_combination)
            if value > prop.value:
                prop.value = value
                prop.actor = actor
                prop.layers = layer_combination
    print(f"Done {count} out of {len(layer_combinations)}")

for prop in biggest:
    print(f"Biggest {prop.name} has the actor {prop.actor} on layers {str(prop.layers)}. It's value is {prop.value}")


'''print(graph.degree("1", ["1", "2"]))
print(graph.neighbors("1", ["1", "2"]))
print(graph.connective_redundancy("1", ["1", "2"]))
print(graph.exclusive_neighbors("1", ["1", "2"]))'''
'''for index, (name, layer) in enumerate(graph.layers.items()):
    if index > 2:
        break

    print(f"Layer {name}")

    print(f"Počet vrcholov: {layer.nodes_count}")
    print(f"Počet hrán: {layer.edges_count}")
    print(f"Hustota: {layer.density}")

    print(f"Priemerný stupeň: {layer.average_degree}")
    print(f"Maximálny stupeň: {layer.max_degree}")

    print(f"Priemerný zhlukovací koeficient: {layer.get_average_clustering_coefficient()}")

    print(f"Počet komponent: {len(layer.get_component_sizes())}")

    print("")

    layer.save_to_file(f"layers/{name}.csv", separator=";")

    layer.plot_distribution(f"Layer {name}", "degree")
    layer.plot_distribution(f"Layer {name}", "degree", "cumulative")

    layer.plot_distribution(f"Layer {name}", "component_sizes")
    layer.plot_distribution(f"Layer {name}", "component_sizes", "cumulative")'''
