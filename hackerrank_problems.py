from collections import Counter
from itertools import combinations_with_replacement


# non-divisible-subset problem
def nonDivisibleSubset(iterable, k):
    rests_from_division = [i % k for i in iterable]
    c = Counter(rests_from_division)
    divisible_tuples = set()
    for first, second in combinations_with_replacement(set(rests_from_division), 2):
        if (first + second) % k == 0:
            divisible_tuples.add((first, second))
    for pair in divisible_tuples:
        if pair[0] == pair[1]:
            c[pair[0]] = 1
        elif c[pair[0]] >= c[pair[1]]:
            del c[pair[1]]
        else:
            del c[pair[0]]
    return sum((c[i] for i in c))
