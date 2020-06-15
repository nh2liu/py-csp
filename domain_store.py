from collections import deque, namedtuple, defaultdict
from constraints import Constraint, ConstraintViolatedException
from copy import deepcopy

DT = namedtuple('domain_transaction', ['var', 'val', 'pruned'])

class DomainStore:
    @staticmethod
    def _propagate_domain_map(all_pruned_values, domain_map, new_pruned_values):
        for var, pruned_values in new_pruned_values.items():
            if var not in all_pruned_values:
                all_pruned_values[var] = set()
            all_pruned_values[var].update(pruned_values)
            domain_map[var].difference_update(pruned_values)

    @staticmethod
    def _revert_domain_map(all_pruned_values, domain_map):
        for var, values_pruned in all_pruned_values.items():
            domain_map[var].update(values_pruned)

    def __init__(self, variables, domain_map):
        self.variables = variables
        self.constraints = []
        self.original_domain_map = domain_map

        self._domain_map = deepcopy(domain_map)
        self._unassigned_variables = set(variables)
        self._var_constraints = defaultdict(list)

    def add_constraint(self, constraint: Constraint):
        for var in constraint.variables:
            self._var_constraints[var].append(len(self.constraints))

        self.constraints.append(constraint)

    def get_state(self):
        return self._unassigned_variables, self._domain_map

    def revert_transaction(self, domain_transaction):
        var, val, pruned = domain_transaction
        DomainStore._revert_domain_map(pruned, self._domain_map)
        for var in pruned:
            if len(self._domain_map[var]) > 1:
                self._unassigned_variables.add(var)

    def assign_value(self, variable, value):
        if variable not in self.variables:
            raise AssertionError('Variable is not valid!')

        if variable not in self._unassigned_variables:
            raise AssertionError('Variable already assigned!')

        all_pruned_values = {}
        new_pruned_values = {variable: self._domain_map[variable] - set([value])}
        DomainStore._propagate_domain_map(
            all_pruned_values,
            self._domain_map,
            new_pruned_values
        )
        propagated_constraints = set(self._var_constraints[variable])
        while len(propagated_constraints) > 0:
            idx = propagated_constraints.pop()
            constraint = self.constraints[idx]
            try:
                new_pruned_values = constraint.prune(self._domain_map)
            except ConstraintViolatedException as e:
                self._revert_domain_map(all_pruned_values, self._domain_map)
                # Constraint violated.
                return False, None
            DomainStore._propagate_domain_map(
                all_pruned_values,
                self._domain_map,
                new_pruned_values
            )
            for var in new_pruned_values.keys():
                propagated_constraints.update(self._var_constraints[var])

        for var in all_pruned_values:
            if len(self._domain_map[var]) == 1:
                # Singule cardinality domains are considered assigned.
                self._unassigned_variables.remove(var)

        domain_transaction = DT(variable, value, all_pruned_values)
        # Successful addition
        return True, domain_transaction
