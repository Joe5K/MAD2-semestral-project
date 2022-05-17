from implementacni_ukol.form import generate_form


generate_form().mainloop()

"""
from implementacni_ukol.rw_samplers.rws_metropolis_hasting import RWSMetropolisHasting
from implementacni_ukol.rw_samplers.rws_with_random_jumps import RWSRandomJumps
from implementacni_ukol.rw_samplers.rwsampler import RWSampler
from implementacni_ukol.rw_samplers.rws_with_restarts import RWSRestarts
from implementacni_ukol.rws_original_graph.random_walk_sampling_original_graph import OriginalGraph

original_graph = OriginalGraph(filename="data/data1.txt")

samples = [
    RWSampler(original_graph),
    #RWSRandomJumps(original_graph),
    #RWSRestarts(original_graph),
    #RWSMetropolisHasting(original_graph)
]

expected_size = 2000
for sample in samples:
    sample.random_walk(expected_size)

for graph in (original_graph, *samples):
    component_sizes = graph.get_component_sizes()
    number_of_components = len(list(filter(lambda x: x >= 2, component_sizes)))
    print(f"Graph {graph.name} has {number_of_components} component with the size at least 2", end="")
    print(f", size of the biggest component is {max(component_sizes)}", end="")
    print(f", graph contains {len(list(filter(lambda x: x == 2, component_sizes)))} isolated nodes", end="")
    print(".")

for sample in samples:
    sample.compare(original_graph, "cumulative_degree_distribution")
    sample.compare(original_graph, "degree_distribution")

"""