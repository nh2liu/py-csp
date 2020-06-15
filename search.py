import constraints
from domain_store import DomainStore
from typing import Callable
import random
from copy import deepcopy

def min_varname_selection(unassigned_variables, domain_map):
    return min(unassigned_variables)

def random_value_assignment(unassigned_variables, domain_map, variable, possible_values):
    return random.sample(possible_values, k = 1)[0]

def extract_element_helper(d: dict):
    return {k : next(iter(s)) for k, s in d.items()}

def search(
        domain_store: DomainStore,
        selection_policy: Callable,
        value_assignment_policy: Callable,
        find_all: bool = False,
    ):
    all_solutions = []
    search_history = []
    transaction_history = []
    unassigned_variables, domain_map = domain_store.get_state()
    next_var = selection_policy(unassigned_variables, domain_map)
    next_possible_values = deepcopy(domain_map[next_var])
    search_history.append((next_var, next_possible_values))
    while True:
        if len(search_history) == 0:
            break
        var, possible_values = search_history[-1]
        if len(search_history) == len(transaction_history):
            domain_store.revert_transaction(transaction_history.pop())

        while len(possible_values) > 0:
            val = value_assignment_policy(
                unassigned_variables,
                domain_map,
                var,
                possible_values
            )
            possible_values.remove(val)
            is_valid_assignment, domain_transaction = domain_store.assign_value(var, val)
            if is_valid_assignment:
                transaction_history.append(domain_transaction)
                break
        else:
            search_history.pop()
            continue
        unassigned_variables, domain_map = domain_store.get_state()
        if len(unassigned_variables) == 0:
            # Solution_found
            sln = extract_element_helper(domain_map)
            all_solutions.append(sln)
            if not find_all:
                break
        else:
            # Assign a variable to an unassigned.
            next_var = selection_policy(unassigned_variables, domain_map)
            next_possible_values = deepcopy(domain_map[next_var])
            search_history.append((next_var, next_possible_values))
    return all_solutions
