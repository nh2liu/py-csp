from constraints import IntegerSumConstraint

constraint = IntegerSumConstraint([1,2,4], 4)

domain = {
    1 : {1,2,3},
    2 : {-2,3,4},
    3 : {4,5,2},
    4 : {0,-1},
    5 : {100, 200, -300}
}

print(constraint._possible_configurations(domain))
