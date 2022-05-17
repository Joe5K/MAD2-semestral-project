import random

from implementacni_ukol.rw_samplers.rwsampler import RWSampler
from implementacni_ukol.rws_original_graph.random_walk_sampling_original_graph import OriginalGraph


class RWSRandomJumps(RWSampler):
    def __init__(self, data: OriginalGraph, random_scenario_probability: float = 0.15):
        super().__init__(data)

        self.random_scenario_probability = random_scenario_probability

    @property
    def name(self):
        return "Random Jumps graph"

    def _should_connect(self, node, neighbor):
        return random.uniform(0, 1) > self.random_scenario_probability

    def _alternative_scenario(self):
        return self._get_new_initial_node()
