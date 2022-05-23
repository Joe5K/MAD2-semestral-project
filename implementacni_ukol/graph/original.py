import random
import sys

from implementacni_ukol.graph.graph import Graph


class OriginalGraph(Graph):
    def __init__(self, filename: str, separator: str = " "):
        super().__init__()

        self._load_file(filename, separator)

    @property
    def name(self):
        return "Original graph"

    def _load_file(self, filename: str, separator: str) -> None:
        with open(filename, "r") as reader:
            for line in reader.readlines():
                node_a, node_b = line[:-1].split(separator)
                self.add_edge(node_a, node_b)

    def get_random_node(self) -> str:
        return random.choice(list(self._nodes_adjs.keys()))
