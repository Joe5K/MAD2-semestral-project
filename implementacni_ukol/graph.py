from collections import OrderedDict
from typing import Dict, Set


class Graph:
    def __init__(self):
        self._nodes_adjs: Dict[str, Set] = {}

    @property
    def nodes_number(self):
        return len(self._nodes_adjs)

    @property
    def degrees(self):
        return {node: len(neighbors) for node, neighbors in self._nodes_adjs.items()}

    @property
    def average_degree(self):
        return sum(self.degrees.values()) / self.nodes_number

    @property
    def min_degree(self):
        return min(self.degrees.values())

    @property
    def max_degree(self):
        return max(self.degrees.values())

    @property
    def degrees_distribution(self):
        deg_distribution = OrderedDict()

        for i in range(0, self.max_degree + 1):
            deg_distribution[i] = 0

        for i in self.degrees.values():
            deg_distribution[i] += 1

        return deg_distribution

    @property
    def cumulative_degree_distribution(self):
        cumulative_deg = OrderedDict()
        for degree, count in self.degrees_distribution.items():
            cumulative_deg[degree] = 0 if degree == 0 else cumulative_deg.get(degree-1) + count

        return cumulative_deg

    @property
    def normalized_cumulative_degree_distribution(self):
        normalized_cumulative_deg = OrderedDict()

        maximum_value = max(self.cumulative_degree_distribution.values())

        for degree, value in self.cumulative_degree_distribution.items():
            normalized_cumulative_deg[degree] = value/maximum_value

        return normalized_cumulative_deg

    @staticmethod
    def normalize_cumulative_degree_distribution(first, second):
        lower, bigger = sorted([first, second], key=lambda x: len(x.normalized_cumulative_degree_distribution))
        distance = len(bigger.normalized_cumulative_degree_distribution) / len(lower.normalized_cumulative_degree_distribution)
        if distance == 1:
            return first.normalized_cumulative_degree_distribution, second.normalized_cumulative_degree_distribution

        normalized_distribution = OrderedDict()

        for degree, value in bigger.normalized_cumulative_degree_distribution.items():
            new_degree = round(degree/distance)
            if not normalized_distribution.get(new_degree):
                normalized_distribution[new_degree] = list()
            normalized_distribution[new_degree].append(value)

        for degree, value in normalized_distribution.items():
            normalized_distribution[degree] = sum(normalized_distribution[degree]) / len(normalized_distribution[degree])

        return lower.normalized_cumulative_degree_distribution, normalized_distribution


    def kolmogorov_smirnov(self, other):
        a, b = self.normalize_cumulative_degree_distribution(self, other)
        maximum = 0

        for i, j in zip(a.values(), b.values()):
            dist = abs(i-j)
            if dist > maximum:
                maximum = dist

        return maximum
