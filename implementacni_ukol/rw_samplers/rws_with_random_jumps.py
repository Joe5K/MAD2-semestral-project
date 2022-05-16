import random

from implementacni_ukol.rw_samplers.rwsampler import RWSampler
from implementacni_ukol.rws_data_interface.random_walk_sampling_interface import RWDataInterface


class RWSRandomJumps(RWSampler):
    def __init__(self, expected_size: int, data: RWDataInterface, jump_probability: float = 0.15):
        super().__init__(expected_size, data)

        self._jump_probability = jump_probability

    def _process_node_and_get_next(self, node):
        next_node = super()._process_node_and_get_next(node)
        if random.uniform(0, 1) < self._jump_probability:
            next_node = self._get_random_scenario_node()
        return next_node

    def _get_random_scenario_node(self):
        return self._get_random_node()
