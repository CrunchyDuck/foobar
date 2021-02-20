from math import factorial as fac
from itertools import combinations
import cProfile


def test_union(num_required, bunny_keys, union):
    """

    Args:
        num_required: Number of bunnies to pick from the pile
        bunny_keys: A list of all the keys each bunny has
        union: What the union of the bunny keys should be.
    """
    union = set(union)

    # Create all different combinations of bunnies that can be picked,
    # and verify the union of their keys will always open all doors.
    tests = flatten_gen(combinations(bunny_keys, num_required))
    for test in tests:
        all_keys = []
        for this_bunny_keys in test:
            all_keys += this_bunny_keys
        all_keys = set(all_keys)

        if all_keys != union:
            return (False, test)

    # All of these tests should fail.
    tests_fail = flatten_gen(combinations(bunny_keys, num_required - 1))
    for test in tests_fail:
        all_keys = []
        for this_bunny_keys in test:
            all_keys += this_bunny_keys
        all_keys = set(all_keys)
        if all_keys == union:
            return (False, test)

    return (True, bunny_keys)


def num_doors(num_bunnies, num_required):
    """
    Calculates the number of doors there must be, given num_bunnies and num_required.
    Essentially a binomial coefficient calculator with offsets.
    Arguments:
        num_bunnies: Number of bunnies
        num_required: Number of bunnies required to open an amount of doors.

    Returns:
        Number of doors.
    """
    binomial = num_required - 1
    n = num_bunnies
    return binomial_coeff(n, binomial)


def num_bunny_keys(num_bunnies, num_required):
    """
    Calculates the number of doors there must be, given num_bunnies and num_required.
    Essentially a binomial coefficient calculator with offsets.
    Arguments:
        num_bunnies: Number of bunnies
        num_required: Number of bunnies required to open an amount of doors.

    Returns:
        Number of doors.
    """
    binomial = num_required - 1
    n = num_bunnies - 1
    return binomial_coeff(n, binomial)


def binomial_coeff(n, binomial):
    return fac(n) // fac(binomial) // fac(n - binomial)


def flatten_gen(generator):
    return [x for x in generator]


def solution(num_bunnies, num_required):
    bunny_keys = [[] for _ in range(num_bunnies)]

    door_keys = num_bunnies + 1 - num_required  # Number of keys to each door.
    i = 0
    for door_to_bunnies in combinations(range(num_bunnies), door_keys):
        for bunny in door_to_bunnies:
            bunny_keys[bunny].append(i)
        i += 1
    return bunny_keys


def tst():
    pass #print solution(4, 2)


#print tst()
#print num_doors(5, 3)
#cProfile.run("tst()", sort="cumtime")
#test_union(2, ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)))
#print solution(4, 3)
#print solution(4, 4)
#print solution(5, 3)