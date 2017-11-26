import selection as sel
import crossover as cs
import mutation as mut
import succession as suc

SELECTION = {
    "noop": None,
    "tournament": sel.tournament_selection,
    "roulette": sel.roulette_wheel_selection,
    "rank": sel.rank_selection,
}

CROSSOVER = {
    "noop": None,
    "cycle": cs.cycle_crossover,
    "injection": cs.injection_crossover,
    "multi_injection": cs.multiple_injection_crossover,
    "pmx": cs.pmx_crossover,
    "single_pmx": cs.pmx_with_single_crossover_point,
}

MUTATION = {
    "noop": None,
    "adjacent_swap": mut.adjacent_swap_mutation,
    "insertion": mut.insertion_mutation,
    "inversion": mut.inversion_mutation,
    "slide": mut.random_slide_mutation,
    "random_swap": mut.random_swap_mutation,
    "scramble": mut.scramble_mutation,
    "single_swap": mut.single_swap_mutation,
}

SUCCESSION = {
    "noop": None,
    "best": suc.best,
    "rank": suc.rank_succession,
    "best_then_random": suc.best_then_uniform_succession,
}
