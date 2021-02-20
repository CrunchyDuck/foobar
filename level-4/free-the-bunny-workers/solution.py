from itertools import combinations


def solution(num_bunnies, num_required):
    """
    Calculate which keys each bunny should get.

    Arguments:
        num_bunnies - How many bunnies there are
        num_required - The minimum amount of bunnies required to open all doors.

    Returns:
        [[keys_to_doors] * num_bunnies]
    """
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