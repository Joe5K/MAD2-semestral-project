import random
import sys

from implementacni_ukol.graph import Graph


class SampledGraph(Graph):
    def __init__(self, filename: str, separator: str = " "):
        super().__init__()

        self._load_file(filename, separator)

    def _load_file(self, filename: str, separator: str) -> None:
        with open(filename, "r") as reader:
            for line in reader.readlines():
                node_a, node_b = line[:-1].split(separator)
                self._add_edge(node_a, node_b)

    def get_random_node(self) -> str:
        return random.choice(list(self._nodes_adjs.keys()))

    def get_neighbors(self, node):
        try:
            return self._nodes_adjs[node]
        except KeyError:
            print(f"{self.__name__}.get_neighbors({node}): Invalid node number. Program halted.")
            sys.exit(1)
