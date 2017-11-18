def _tuple_to_score(t):
    ch, fitness = t
    return fitness


def _tuple_to_chromosome(t):
    ch, algoscore = t
    return ch


def sort(population, inv=False):
    return sorted(population, key=_tuple_to_score, reverse=inv)


def sort_extract(population, inv=False):
    return map(_tuple_to_chromosome, sort(population, inv))
