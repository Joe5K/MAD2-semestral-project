import random
import sys
from itertools import count
from typing import Dict, Set, List


class RandomWalkSamplingData:
    def __init__(self, filename: str, separator: str = " "):
        self._keys: List = []
        self._node_adjs: Dict[str, Set] = {}

        self._load_file(filename, separator)

    def _load_file(self, filename: str, separator: str) -> None:
        with open(filename, "r") as reader:
            for line in reader.readlines():
                node_a, node_b = line[:-1].split(separator)
                if not self._node_adjs.get(node_a):
                    self._node_adjs[node_a] = set()
                if not self._node_adjs.get(node_b):
                    self._node_adjs[node_b] = set()
                self._node_adjs[node_a].add(node_b)
                self._node_adjs[node_b].add(node_a)
        self._keys = self._node_adjs.keys()

    def get_random_node(self) -> Dict[str, Set]:
        key = random.choice(self._keys)
        value = self._node_adjs[key]
        return {key: value}

    def get_neighbors(self, node):
        try:
            return self._node_adjs[node]
        except KeyError:
            print(f"{self.__name__}.get_neighbors({node}): Invalid node number. Program halted.")
            sys.exit(1)

class RandomWalkSampling:
    def __init__(self, expected_size: int):
        self.node_adjs: Dict[str, Set] = {}
        self.expected_size = expected_size

    def start_random_walk(self, data: RandomWalkSamplingData):
        while len(self.node_adjs) < self.expected_size:
            current_node = data.get_random_node()
            last_size = 0




data = RandomWalkSamplingData(filename="data/data1.txt")

sampler = RandomWalkSampling(expected_size=100)
sampler.start_random_walk(data)
