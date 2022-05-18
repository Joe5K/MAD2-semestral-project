from implementacni_ukol.samplers.rws_with_random_jumps import RWSRandomJumps
from implementacni_ukol.graph.original import OriginalGraph


class RWSRestarts(RWSRandomJumps):
    def __init__(self, data: OriginalGraph, random_scenario_probability: float = 0.15):
        super().__init__(data, random_scenario_probability)

        self._initial_node = None

    @property
    def name(self):
        return "RWR graph"

    def _get_new_initial_node(self):
        node = super()._get_new_initial_node()
        self._initial_node = node
        return node

    def _get_alternative_scenario_node(self):
        return self._initial_node

