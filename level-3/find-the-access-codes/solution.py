from functools import reduce
import cProfile


class LuckyNumber:
    """
    Stores numbers in the lock access code that are factors of this number.
    This allows to me solve for lucky number triples (i, j, k)
    k = this lucky number
    j = any child of k
    i = any child of j

    Attributes:
        number - The number this object represents.
        factors - All of the possible positive factors of this number.
        children - A list of LuckyNumber objects that are factors of this object.
    """
    def __init__(self, number, index):
        self.number = number
        self.index = index
        self.factors = factors(number)
        self.children = []

    def __repr__(self):
        return str(self.number)

    def get_unique_chains(self, chain_length):
        """
        Gets all unique chains this number and its children can create at the specified length.

        Arguments:
            chain_length - How long the chain must be, including this number.

        Returns:
            Set of all unique chains that can be constructed.
        """
        if chain_length == 1:
            return [[self.number]]

        chains = []
        for num in self.children:
            children_chains = num.get_unique_chains(chain_length-1)
            for child_chain in children_chains:
                chains.append([self.number] + child_chain)

        return chains


def factors(n):
    """
    Gets facts of a positive number and returns them in a set. But fast!

    Returns:
        Set containing all factors.
    """
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def index_lucky_children(lucky_list, lucky_dict):
    """
    Fills the children entries in a LuckyNumbers list.
    Arguments:
        lucky_list - A list of LuckyNumbers
        lucky_dict - A dictionary that will be consumed to generate the children for lucky_list.
    """
    for num in reversed(lucky_list):
        factor_entries = []  # All numbers that would match, before considering indices.
        for factor in num.factors:
            if factor in lucky_dict:
                factor_entries += lucky_dict[factor]

        my_index = num.index
        for entry in factor_entries:
            if entry.index < my_index:
                num.children.append(entry)


def create_lucky_number_dict(lucky_number_list):
    """
    Converts a list of lucky numbers into a dictionary ordered as {number: [object]}
    This preserves the amount of times an item appears in the list,
    while still functioning at the speed of a lookup table.
    """
    lucky_number_dict = {}
    for lucky_number in lucky_number_list:
        number = lucky_number.number
        if number not in lucky_number_dict:
            lucky_number_dict[number] = [lucky_number]
        else:
            lucky_number_dict[number].append(lucky_number)

    return lucky_number_dict


def solution(l):
    lucky_number_list = []
    for i in range(len(l)):
        lucky_number_list.append(LuckyNumber(l[i], i))

    lucky_number_dict = create_lucky_number_dict(lucky_number_list)
    index_lucky_children(lucky_number_list, lucky_number_dict)
    lucky_triples = []

    for lucky_number in reversed(lucky_number_list):  # Going from top down handles duplicate numbers.
        lucky_triples += lucky_number.get_unique_chains(3)

    #lucky_triples = set(lucky_triples)
    return len(lucky_triples)


#cProfile.run("solution_test()", sort="cumtime")

#test_list = [999999 for _ in range(1, 2000)]
#print solution(test_list)
#print solution([1, 2, 3, 4, 5, 6])
#print solution([6, 5, 4, 3, 2, 1])

# print solution([1, 5, 9])
# print solution([1, 2, 3, 4, 5, 6])
print solution([1, 1, 1, 1])
#print solution([1, 1, 1, 1, 1, 1, 1])