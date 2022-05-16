import random

from implementacni_ukol.rw_samplers.rwsampler import RWSampler


class RWSMetropolisHasting(RWSampler):
    BATCH_SIZE = 200

    def _process_node_and_get_next(self, node):
        old_node = node
        new_node = super()._process_node_and_get_next(node)
        probability = random.uniform(0, 1)

        old_node_degree = len(self._data_interface.get_neighbors(old_node))
        new_node_degree = len(self._data_interface.get_neighbors(new_node))

        if old_node_degree/new_node_degree > probability:
            return new_node
        return old_node