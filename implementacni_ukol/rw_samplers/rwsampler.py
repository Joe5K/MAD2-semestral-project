import random
from typing import Dict, Set

from implementacni_ukol.graph import Graph
from implementacni_ukol.rws_data_interface.random_walk_sampling_interface import SampledGraph


class RWSampler(Graph):
    BATCH_SIZE = 100

    def __init__(self, expected_size: int, data: SampledGraph):
        super().__init__()

        self._expected_size = expected_size
        self._data_interface = data

    @property
    def node_adjs(self):
        return self._nodes_adjs

    @property
    def expected_size(self):
        return self._expected_size

    def random_walk(self):
        node = self._get_random_node()
        while self.nodes_number < self._expected_size:
            last_size = self.nodes_number

            for count in range(self.BATCH_SIZE):
                node = self._process_node_and_get_next(node)

            if self.nodes_number== last_size:
                node = self._get_random_node()
                #print(f"{self.__class__.__name__} is stuck on number {last_size}, choosing new random starting node {node}")

        #print(f"{self.__class__.__name__}: Finished sampling {self._expected_size} samples! Actual size: {self.nodes_number}")

    def _get_random_node(self):
        return self._data_interface.get_random_node()

    def _process_node_and_get_next(self, node): # TODO upravit logiku a nepridavat susedov
        neighbors = self._data_interface.get_neighbors(node)
        self._nodes_adjs[node] = neighbors
        return random.choice(list(neighbors))

