class ConstraintViolatedException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Constraint:
    def __init__(self, variables):
        self.variables = variables

    def prime(self, domain_map):
        pass

    def prune(self, domain_map) -> dict:
        pass

def get_pruned_values(domain_map, new_domains):
    all_pruned_values = {}
    for var, domain in new_domains.items():
        pruned_domain = domain_map[var] - domain
        if len(pruned_domain) > 0:
            all_pruned_values[var] = pruned_domain
    return all_pruned_values

class IntegerSumConstraint(Constraint):
    def __init__(self, variables, val):
        super().__init__(variables)
        self._variables = variables[::-1]
        self.val = val

    def _possible_configurations(self, domain_map):
        c_min_max_bounds = []
        c_var_min, c_var_max = 0, 0
        for var in self.variables:
            c_min_max_bounds.append((c_var_min, c_var_max))
            c_var_min += min(domain_map[var])
            c_var_max += max(domain_map[var])

        c_min_max_bounds.reverse()
        all_configs = []
        
        def _helper(cur_idx, cur_config, target):
            cur_var = self._variables[cur_idx]
            var_domain = domain_map[cur_var]
            if cur_idx == len(self._variables) - 1:
                # Last one
                if target in var_domain:
                    complete_config = cur_config + [target]
                    all_configs.append(complete_config)
                    return
            else:
                c_min, c_max = c_min_max_bounds[cur_idx]
                for candidate in var_domain:
                    next_target = target - candidate
                    if next_target > c_max or next_target < c_min:
                        continue
                    cur_config.append(candidate)
                    _helper(cur_idx + 1, cur_config, next_target)
                    cur_config.pop()
        config = []
        _helper(0, config, self.val)
        return all_configs

    def prune(self, domain_map):
        valid_configs = self._possible_configurations(domain_map)
        if len(valid_configs) == 0:
            raise ConstraintViolatedException(
                'No valid configuration found for IntegerSumConstraint.'
            )

        valid_domains = {var : set() for var in self.variables}
        for config in valid_configs:
            for var, val in zip(self._variables, config):
                valid_domains[var].add(val)
        return get_pruned_values(domain_map, valid_domains)
