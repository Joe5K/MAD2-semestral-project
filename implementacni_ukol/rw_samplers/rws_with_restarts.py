import random

from implementacni_ukol.rw_samplers.rws_with_random_jumps import RWSRandomJumps
from implementacni_ukol.rws_data_interface.random_walk_sampling_interface import RWDataInterface


class RWSRestarts(RWSRandomJumps):
    def __init__(self, expected_size: int, data: RWDataInterface, jump_probability: float = 0.15):
        super().__init__(expected_size, data, jump_probability)

        self._initial_node = None

    def _get_random_node(self):
        node = super()._get_random_node()
        self._initial_node = node
        return node

    def _get_random_scenario_node(self):
        if self._initial_node:
            return self._initial_node
        return super()._get_random_scenario_node()
