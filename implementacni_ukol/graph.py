from collections import OrderedDict
from math import floor, log
from typing import Dict, Set
import numpy
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self._nodes_adjs: Dict[str, Set] = {}

    def _add_node(self, node):
        if not self._nodes_adjs.get(node):
            self._nodes_adjs[node] = set()

    def _add_edge(self, node1, node2):
        if not self._nodes_adjs.get(node1):
            self._nodes_adjs[node1] = set()
        if not self._nodes_adjs.get(node2):
            self._nodes_adjs[node2] = set()
        self._nodes_adjs[node1].add(node2)
        self._nodes_adjs[node2].add(node1)

    @property
    def name(self):
        return "Graph"

    def get_component_sizes(self):
        class Visitor:
            def __init__(self):
                self.cache = set()
                self.counter = 0

            def push(self, node):
                self.counter += 1
                self.cache.add(node)

            def pop(self):
                if self.cache:
                    return self.cache.pop()

        nodes = self._nodes_adjs.keys()
        visited = {i: False for i in nodes}
        component_sizes = []

        for node in nodes:
            if not visited[node]:
                size = 0
                visitor = Visitor()
                visitor.push(node)
                while current_node := visitor.pop():
                    size += 1
                    visited[current_node] = True
                    for neighbor in self._nodes_adjs[current_node]:
                        if not visited[neighbor]:
                            visitor.push(neighbor)

                component_sizes.append(size)

        return component_sizes



    def clustering_coefficients(self):
        return 1
        coefficients = {}
        for node, neighbors in self._nodes_adjs.items():
            neighborhood = len(neighbors)
            neighbors = list(neighbors)
            number_of_links = 0
            for i in range(neighborhood):
                for j in range(i):
                    if neighbors[j] in self._nodes_adjs[neighbors[i]]:
                        number_of_links += 1

            coefficients[node] = 2*number_of_links/neighborhood*(neighborhood-1)
        return coefficients

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

    @property
    def degree_distribution(self):
        deg_distribution = OrderedDict()

        for i in range(0, self.max_degree + 1):
            deg_distribution[i] = 0

        for i in self.degrees.values():
            deg_distribution[i] += 1

        return deg_distribution

    @property
    def cumulative_degree_distribution(self):
        cumulative_deg = OrderedDict()
        for degree, count in self.degree_distribution.items():
            cumulative_deg[degree] = 0 if degree == 0 else cumulative_deg.get(degree-1) + count

        return cumulative_deg

    def normalize(self, parameter_str: str, logaritmize=True):
        parameter = getattr(self, parameter_str, "cumulative_degree_distribution")

        normalized = OrderedDict()

        maximum_x = max(parameter.keys())
        maximum_y = max(parameter.values())

        if logaritmize:
            maximum_x = log(maximum_x)

        for key, value in parameter.items():
            if logaritmize:
                if key <= 0:
                    continue
                key = log(key)

            normalized[key/maximum_x] = value/maximum_y

        return normalized

    def compare(self, other, parameter: str = "cumulative_degree_distribution"):
        normalized_sample = self.normalize(parameter)
        normalized_other = other.normalize(parameter)

        plt.plot(normalized_other.keys(), normalized_other.values(), color="red", label=other.name)
        plt.plot(normalized_sample.keys(), normalized_sample.values(), color="blue", label=self.name)

        plt.title(f"Comparison of normalized {parameter.replace('_', ' ')}")
        plt.xlabel("Normalized log(x)")
        plt.ylabel("Normalized f(x)")
        plt.legend(loc="best")
        plt.savefig(f"images/{parameter}.png")
        plt.clf()

    '''
    @staticmethod
    def normalize_x(sample, original):
        length = len(sample)-1
        delta = len(original)/length

        normalized_original = OrderedDict()
        for i in range(length+1):
            normalized_original[i] = []

        for number, value in enumerate(original):
            index = round(number/delta)
            normalized_original[index].append(value)

        for index in range(length+1):
            normalized_original[index] = sum(normalized_original[index]) / len(normalized_original[index])

        return normalized_original
        
        @property
        def normalized_cumulative_degree_distribution(self):
            normalized_cumulative_deg = OrderedDict()

            maximum_value = max(self.cumulative_degree_distribution.values())

            for degree, value in self.cumulative_degree_distribution.items():
                normalized_cumulative_deg[math.log(degree) if degree > 0 else degree] = value/maximum_value

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
    '''
