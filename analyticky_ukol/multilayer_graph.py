from typing import Dict

from implementacni_ukol.graph.graph import Graph


class MultiLayerGraph:
    def __init__(self, filename: str, separator: str = " "):
        self.layers: Dict[str, Graph] = {}

        self._load_graph(filename, separator)

    def _load_graph(self, filename:str, separator: str):
        with open(filename, "r") as reader:
            for line in reader.readlines():
                layer, node_a, node_b, _ = line[:-1].split(separator)
                if not self.layers.get(layer):
                    self.layers[layer] = Graph()
                self.layers[layer].add_edge(node_a, node_b)

    def save_graph(self, folder):
        for name, graph in self.layers.items():
            graph.save_to_file(f"{folder}/{name}.csv", separator=";")

    def degree(self, actor, layer_names=None):
        if not layer_names:
            layer_names = self.layers.keys()
        return sum(self.layers[layer_name].node_degree(actor) for layer_name in layer_names)

    def neighbors(self, actor, layer_names=None):
        if not layer_names:
            layer_names = self.layers.keys()
        neighbors = set()
        for layer_name in layer_names:
            neighbors.update(self.layers[layer_name].get_neighbors(actor))
        return neighbors

    def neighborhood(self, actor, layer_names=None):
        return len(self.neighbors(actor, layer_names))

    def connective_redundancy(self, actor, layer_names=None):
        degree = self.degree(actor, layer_names)
        if degree == 0:
            return 0
        return 1 - self.neighborhood(actor, layer_names) / degree

    def exclusive_neighbors(self, actor, layers):
        return self.neighbors(actor, layers) - self.neighbors(actor, set(self.layers.keys()) - set(layers))

    def exclusive_neighborhood(self, actor, layers):
        return len(self.exclusive_neighbors(actor, layers))

