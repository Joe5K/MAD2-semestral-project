from implementacni_ukol.rw_samplers.rws_metropolis_hasting import RWSMetropolisHasting
from implementacni_ukol.rw_samplers.rws_with_random_jumps import RWSRandomJumps
from implementacni_ukol.rw_samplers.rwsampler import RWSampler
from implementacni_ukol.rw_samplers.rws_with_restarts import RWSRestarts
from implementacni_ukol.rws_data_interface.random_walk_sampling_interface import RWDataInterface

data = RWDataInterface(filename="data/data1.txt")
expected_size = 200

params = {"expected_size": expected_size, "data": data}
samplers = [
#    RWSampler(**params),
#    RWSRandomJumps(**params),
#    RWSRestarts(**params),
    RWSMetropolisHasting(**params)
]

for sampler in samplers:
    sampler.random_walk()
    sampler.kolmogorov_smirnov(data)