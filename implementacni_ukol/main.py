from datetime import datetime

from implementacni_ukol.rw_samplers.rws_metropolis_hasting import RWSMetropolisHasting
from implementacni_ukol.rw_samplers.rws_with_random_jumps import RWSRandomJumps
from implementacni_ukol.rw_samplers.rwsampler import RWSampler
from implementacni_ukol.rw_samplers.rws_with_restarts import RWSRestarts
from implementacni_ukol.rws_data_interface.random_walk_sampling_interface import SampledGraph

sampled_graph = SampledGraph(filename="data/data1.txt")
expected_size = 10000

params = {"expected_size": expected_size, "data": sampled_graph}
samplers = [
    RWSampler(**params),
    RWSRandomJumps(**params),
    RWSRestarts(**params),
    RWSMetropolisHasting(**params)
]

start = datetime.now()
for sampler in samplers:
    sampler.random_walk()
    print(f"{sampler.__class__.__name__} Degree distribution distance: {sampler.kolmogorov_smirnov(sampled_graph)}")
end = datetime.now()

print(f"Processing took {(end-start).total_seconds()} seconds")