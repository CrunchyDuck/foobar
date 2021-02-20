from math import factorial as fac
from itertools import combinations
import cProfile


def test_union(num_required, bunny_keys, union):
    """

    Args:
        num_required: Number of bunnies to pick from the pile
        bunny_keys: A list of all the keys each bunny has
        union: What the union of the bunny keys should be.

    Returns:

    """
    this_set = set()
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
    n = num_bunnies# + binomial
    return fac(n) // fac(binomial) // fac(n - binomial)


def flatten_gen(generator):
    return [x for x in generator]


def solution(num_bunnies, num_required):
    # short circuits
    if num_required == 0:  # I don't actually know what I should be returning for this one.
        return [[] for _ in range(num_required)]
    elif num_required == 1:
        return [[0] for _ in range(num_required)]
    elif num_required == num_bunnies:
        return [[x] for x in range(num_required)]

    door_num = num_doors(num_bunnies, num_required)
    doors = [x for x in range(door_num)]
    bunny_keys = 1  # How many keys each bunny has.

    while bunny_keys <= door_num:  # If this breaks due to condition, something has gone wrong.
        combins = flatten_gen(combinations(doors, bunny_keys))
        if len(combins) < num_bunnies:
            break
        for bunny_set in combinations(combins, num_bunnies):
            result = test_union(num_required, bunny_set, doors)
            if result[0]:
                return result
            else:
                pass #print result
        bunny_keys += 1

    raise Exception("Could not find a combination of bunny keys.\n"
                    "num bunnies:%s\n"
                    "num required:%s\n"
                    "door_num:%s" %
                    (num_bunnies, num_required, door_num))


def tst():
    print solution(9, 2)


#print num_doors(5, 3)

#cProfile.run("tst()", sort="cumtime")
#test_union(2, ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)))
#print solution(2, 1)
#print solution(4, 4)
print solution(5, 3)