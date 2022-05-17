import random

from implementacni_ukol.rw_samplers.rwsampler import RWSampler


class RWSMetropolisHasting(RWSampler):
    CHECK_STUCK_DISTANCE = 200

    @property
    def name(self):
        return "Metropolis-Hasting graph"

    def _should_connect(self, node, neighbor):
        probability = random.uniform(0, 1)

        old_node_degree = len(self._data_interface.get_neighbors(node))
        new_node_degree = len(self._data_interface.get_neighbors(neighbor))

        return old_node_degree/new_node_degree > probability
