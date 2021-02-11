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
    def __init__(self, number):
        self.number = number
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
            return ((self.number,),)

        chains = []
        for num in self.children:
            children_chains = num.get_unique_chains(chain_length-1)
            for child_chain in children_chains:
                chains.append((self.number,) + child_chain)

        return set(chains)


def factors(n):
    """
    Gets facts of a positive number and returns them in a set. But fast!

    Returns:
        Set containing all factors.
    """
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def index_lucky_children(lucky_list):
    """
    Fills the children entries in a LuckyNumbers list.
    Arguments:
        lucky_list - A list of LuckyNumbers, sorted from smallest to largest.
    """
    for i in range(len(lucky_list)-1, 0, -1):  # Lucky indices list in reverse
        num = lucky_list[i]
        for lucky_num in lucky_list[:i]:
            if lucky_num.number in num.factors:
                num.children.append(lucky_num)


def solution(l):
    lucky_number_chain = [LuckyNumber(x) for x in l]
    index_lucky_children(lucky_number_chain)
    lucky_triples = []

    for lucky_number in reversed(lucky_number_chain):  # Going from top down handles duplicate numbers.
        lucky_triples += lucky_number.get_unique_chains(3)

    lucky_triples = set(lucky_triples)
    return len(lucky_triples)


print len(factors(999999))
test_list = [1 for _ in range(2000)]
#print solution(test_list)
print solution([1, 2, 3, 4, 5, 6])
print solution([1, 1, 1])
print solution([1, 1, 1, 1, 1, 1, 1])