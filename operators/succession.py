import random
from heapq import nlargest

from utils import sort, _tuple_to_score


def rank_succession(population, k):
    weights_sum = sum(fitness for _, fitness in population)
    sorted_population = sort(population)

    result = list()
    for _ in xrange(k):
        pick = random.uniform(0, weights_sum)
        current = 0
        for t in sorted_population:
            current += _tuple_to_score(t)
            if current > pick:
                result.append(t)
                break

    return result


def _find_n_best_solutions(population, n=1):
    return nlargest(n, population, key=lambda (specimen, score): score.to_fitness())


def best(population, k):
    return _find_n_best_solutions(population, k)


def best_then_uniform_succession(population, k, perc_best=0.20):
    sorted_p = sort(population, inv=True)

    to_take = int(max(perc_best * k, 1))
    best_specimens = sorted_p[0:to_take]

    rest = sorted_p[to_take:]
    randomly_chosen_from_rest = random.sample(rest, k - to_take)

    return best_specimens + randomly_chosen_from_rest
