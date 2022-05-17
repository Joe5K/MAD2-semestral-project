import random
from typing import Dict, Set

from implementacni_ukol.graph import Graph
from implementacni_ukol.rws_original_graph.random_walk_sampling_original_graph import OriginalGraph


class RWSampler(Graph):
    CHECK_STUCK_DISTANCE = 100

    def __init__(self, data: OriginalGraph):
        super().__init__()
        self._data_interface = data

    @property
    def name(self):
        return "Sampled graph"

    @property
    def node_adjs(self):
        return self._nodes_adjs

    def random_walk(self, expected_size):
        node = self._get_new_initial_node()
        while self.nodes_count < expected_size:
            last_size = self.nodes_count

            for count in range(self.CHECK_STUCK_DISTANCE):
                neighbors = self._data_interface.get_neighbors(node)
                neighbor = random.choice(list(neighbors))

                if self._should_connect(node, neighbor):
                    self._add_edge(node, neighbor)
                    node = neighbor
                elif alternative_node := self._alternative_scenario():
                    self._add_node(alternative_node)
                    node = alternative_node

                if self.nodes_count >= expected_size:
                    break

            if self.nodes_count == last_size:
                node = self._get_new_initial_node()

                # print(f"{self.name} is stuck on number {last_size}, choosing new random node {node}")
        # print(f"{self.name}: Finished sampling {expected_size} samples! Actual size: {self.nodes_number}")

    def _should_connect(self, node, neighbor):
        return True

    def _alternative_scenario(self):
        return False

    def _get_new_initial_node(self):
        return self._data_interface.get_random_node()
