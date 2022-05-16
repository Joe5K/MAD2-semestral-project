import random

from implementacni_ukol.rw_samplers.rwsampler import RWSampler
from implementacni_ukol.rws_data_interface.random_walk_sampling_interface import SampledGraph


class RWSRandomJumps(RWSampler):
    def __init__(self, expected_size: int, data: SampledGraph, jump_probability: float = 0.15):
        super().__init__(expected_size, data)

        self._jump_probability = jump_probability

    def _get_next_node(self, node):
        if random.uniform(0, 1) < self._jump_probability:
            return self._get_random_scenario_node()
        return super()._process_node_and_get_next(node)

    def _get_random_scenario_node(self):
        return self._get_random_node()
