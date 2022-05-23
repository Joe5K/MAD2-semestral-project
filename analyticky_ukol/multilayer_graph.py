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
