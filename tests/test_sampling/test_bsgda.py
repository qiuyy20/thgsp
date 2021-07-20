import pytest
import time
import numpy as np
import torch as th
from ..utils4t import float_dtypes
from thgsp.sampling.bsgda import bsgda, greedy_sampling, computing_sets, solving_set_covering, greedy_gda_sampling
from thgsp.graphs import rand_udg

np.set_printoptions(precision=5)
th.set_printoptions(precision=5)
N = 20
T = 0.001
K = 4
max_hops = 3


@pytest.mark.parametrize('dtype', float_dtypes)
def test_computing_sets(dtype):
    g = rand_udg(N, 0.1, dtype=dtype)
    sets, lengths = computing_sets(g, T=8e-5, p_hops=3)
    print(sets)
    print(lengths)

    sets, lengths = computing_sets(g.set_value_(None), T=8e-5, p_hops=3)
    print(sets)
    print(lengths)


def test_solving_set_cover():
    sets = {0: [0, 4, 1, 3],
            1: [2, 1],
            2: [1, 4, 4, 2],
            3: [1, 4, 3, 0],
            4: [1, 0, 3]}

    lengths = [len(sets[s]) for s in range(5)]
    s = time.time()
    S, vf = solving_set_covering(sets, lengths, K)
    print(f"{time.time() - s} seconds elapsed")
    assert S == [3, 2]
    assert vf


@pytest.mark.parametrize('dtype', float_dtypes)
def test_consistency_greedy_sampling(dtype):
    g = rand_udg(N, 0.3, dtype=dtype).set_value_(None)
    selected_pebbles, vf = greedy_sampling(g, K, T, p_hops=max_hops)

    sets, lengths = computing_sets(g, T, p_hops=max_hops)
    s1, vf1 = solving_set_covering(sets, lengths, K)

    s2, vf2 = greedy_gda_sampling(g, K, T, p_hops=max_hops)

    print(selected_pebbles)
    print(s1)
    print(s2)
    print(vf)
    print(vf1)
    print(vf2)

    assert s1 == selected_pebbles
    assert vf1 == vf

    assert s1 == s2
    assert vf1 == vf2


@pytest.mark.parametrize('dtype', float_dtypes)
def test_bsgda(dtype):
    g = rand_udg(N, 0.1, dtype=dtype).fill_value_(1.)
    sampled_nodes, thresh = bsgda(g, K*2)
    print("sampled nodes: ", sampled_nodes)
    print("thresh(T):     ", thresh)
