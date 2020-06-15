from domain_store import DomainStore
from constraints import IntegerSumConstraint
from search import search, min_varname_selection, random_value_assignment

VARIABLES = [(i,j) for i in range(5) for j in range(5)]
VOLTORB_VAL = -500
VARIABLE_MAP = {var : set([VOLTORB_VAL, 1, 2, 3]) for var in VARIABLES}

'''
Board Representation
[(0, 0), (1, 0), ..., (4, 0)]
[(0, 1), (1, 1), ..., (4, 1)]
[(0, 2), (1, 2), ..., (4, 2)]
[(0, 3), (1, 3), ..., (4, 3)]
[(0, 4), (1, 4), ..., (4, 4)]
'''
def get_domain_store(horizontal, vertical):
    domain_store = DomainStore(VARIABLES, VARIABLE_MAP)
    for i, (point_sum, n_voltorbs) in enumerate(horizontal):
        target_sum = n_voltorbs * VOLTORB_VAL + point_sum
        domain_store.add_constraint(
            IntegerSumConstraint([(i, j) for j in range(5)], target_sum)
        )

    for j, (point_sum, n_voltorbs) in enumerate(vertical):
        target_sum = n_voltorbs * VOLTORB_VAL + point_sum
        domain_store.add_constraint(
            IntegerSumConstraint([(i, j) for i in range(5)], target_sum)
        )
    return domain_store

def print_solution(horizontal, vertical, domain_map):
    for j in range(5):
        row = [domain_map[(i, j)] for i in range(5)]
        print(f'{[0 if v == VOLTORB_VAL else v for v in row]} | {vertical[j]}')
    print('---------------')
    print(tuple(point_sum for point_sum, n_voltorbs in horizontal))
    print(tuple(n_voltorbs for point_sum, n_voltorbs in horizontal))

import time
start_time = time.time()

if __name__ == '__main__':
    horizontal = [(5, 2), (7, 1), (4, 3), (5, 1), (4, 1)]
    vertical = [(4, 2), (7, 1), (5, 2), (3, 2), (6, 1)]

    horizontal = [(7, 0), (6, 1), (4, 2), (4, 1), (4, 2)]
    domain_store = get_domain_store(horizontal, vertical)
    start_time = time.time()
    solutions = search(domain_store, min_varname_selection, random_value_assignment, True)
    print("--- Search: {:.2f} seconds ---".format(time.time() - start_time))
    print(len(solutions))
    print_solution(horizontal, vertical, solutions[0])
