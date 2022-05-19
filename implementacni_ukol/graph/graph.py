from collections import OrderedDict
from math import log
from typing import Dict, Set, Optional

import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self._nodes_adjs: Dict[str, Set] = {}

    @property
    def name(self):
        return "Graph"

    def _add_node(self, node):
        if not self._nodes_adjs.get(node):
            self._nodes_adjs[node] = set()

    def add_edge(self, node1, node2):
        self._add_node(node1)
        self._add_node(node2)
        self._nodes_adjs[node1].add(node2)
        self._nodes_adjs[node2].add(node1)

    def get_component_sizes(self):
        nodes = self._nodes_adjs.keys()
        visited = {i: False for i in nodes}
        component_sizes = []

        for node in nodes:
            if not visited[node]:
                size = 0
                visitor = set()
                visitor.add(node)
                while visitor:
                    current_node = visitor.pop()
                    size += 1
                    visited[current_node] = True
                    for neighbor in self._nodes_adjs[current_node]:
                        if not visited[neighbor]:
                            visitor.add(neighbor)

                component_sizes.append(size)

        return component_sizes

    # slow method
    def get_clustering_coefficients(self):
        coefficients = {}
        for node, neighbors in self._nodes_adjs.items():
            neighborhood = len(neighbors)
            neighbors = list(neighbors)
            number_of_links = 0
            for i in range(neighborhood):
                for j in range(i):
                    if neighbors[j] in self._nodes_adjs[neighbors[i]]:
                        number_of_links += 1

            coefficients[node] = (2*number_of_links/(neighborhood*(neighborhood-1))) if neighborhood > 1 else 0
            print(node)
        return coefficients

    @property
    def density(self):
        return self.edges_count/((self.nodes_count*(self.nodes_count-1))/2)

    @property
    def nodes_count(self):
        return len(self._nodes_adjs)

    @property
    def edges_count(self):
        return sum([len(i) for i in self._nodes_adjs.values()])/2

    @property
    def edges_nodes_ratio(self):
        return self.edges_count / self.nodes_count

    @property
    def degrees(self):
        return {node: len(neighbors) for node, neighbors in self._nodes_adjs.items()}

    @property
    def average_degree(self):
        return sum(self.degrees.values()) / self.nodes_count

    @property
    def min_degree(self):
        return min(self.degrees.values())

    @property
    def max_degree(self):
        return max(self.degrees.values())

    def get_distribution(self, parameter: str, type_: str = None):
        if not (data := getattr(self, parameter, None)):
            if callable(getattr(self, f"get_{parameter}", None)) and not (data := getattr(self, f"get_{parameter}")()):
                raise AttributeError(f"Pekne peklicko, ze? Ale {self.__class__.__name__} nevie nic o '{parameter}'")

        if isinstance(data, dict):
            data = list(data.values())

        distribution = OrderedDict()

        for i in range(0, max(data) + 1):
            distribution[i] = 0

        for i in data:
            distribution[i] += 1

        if type_ == "cumulative":
            cumulative_deg = OrderedDict()
            for number, count in distribution.items():
                cumulative_deg[number] = cumulative_deg.get(number - 1) + count if number != 0 else 0

            return cumulative_deg
        return distribution

    def normalize_distribution(self, parameter, type_: Optional[str], logarithmic=True):
        data = getattr(self, f"get_distribution")(parameter, type_)

        normalized = OrderedDict()

        maximum_x = max(data.keys())
        maximum_y = max(data.values())

        if logarithmic:
            maximum_x = log(maximum_x)

        for key, value in data.items():
            if logarithmic:
                if key <= 0:
                    continue
                key = log(key)

            normalized[key/maximum_x] = value/maximum_y

        return normalized

    def compare_distributions(self, other, parameter: str, type_: Optional[str] = None, logarithmic=True):
        normalized_sample = self.normalize_distribution(parameter, type_, logarithmic)
        normalized_other = other.normalize_distribution(parameter, type_, logarithmic)

        plt.plot(normalized_other.keys(), normalized_other.values(), color="red", label=other.name)
        plt.plot(normalized_sample.keys(), normalized_sample.values(), color="blue", label=self.name)

        plt.title(f"Comparison of normalized {type_ + ' ' if type_ else ''}{parameter.replace('_', ' ')} distribution")
        plt.xlabel("Normalized log(x)")
        plt.ylabel("Normalized f(x)")
        plt.legend(loc="best")
        plt.savefig(f"images/{type_ + '_' if type_ else ''}{parameter}_distribution.png")
        plt.clf()
