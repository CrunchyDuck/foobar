import cProfile


class LuckyNumber:
    """
    Attributes:
        number - The number this object represents.
        doubles - How many doubles this number can makes with numbers earlier in the list.
    """
    def __init__(self, number):
        """
        Arguments:
            number - The number this LuckyNumber represents
        """
        self.number = number
        self.doubles = 0  # Number of doubles that came before this.

    def __repr__(self):
        return str(self.number)


def solution(l):
    """
    Scan an access code for lucky triples to crack the LAMBCHOP doomsday device's code.

    Arguments:
        l: List of access codes to scan for lucky triples

    Returns:
        (int) The number of lucky triples in this list.
    """
    lucky_triple_count = 0
    lucky_number_list = []
    for i in range(len(l)):
        lucky_number_list.append(LuckyNumber(l[i]))

    for i in range(len(lucky_number_list)):
        current_lucky_number = lucky_number_list[i]
        for j in range(i):  # Index all doubles this number can create.
            target_num = lucky_number_list[j]

            if not current_lucky_number.number % target_num.number:
                # If the target num had any doubles,
                # they will combine with the current num to make triples.
                current_lucky_number.doubles += 1
                lucky_triple_count += target_num.doubles

    return lucky_triple_count


def solution_test():
    #test_list = [999999 for x in range(999999-2000, 999999-0)]
    test_list = [1, 1, 1, 1, 1, 1]
    print solution(test_list)



cProfile.run("solution_test()", sort="cumtime")

# test_list = [999999 for _ in range(1, 2000)]
# test_list_2 = []
# for i in range(20):
#     test_list_2 += [(i + 1) * 50 for _ in range(5)]
# print test_list_2

#print solution(test_list)
#print solution([1, 2, 3, 4, 5, 6])
#print solution([6, 5, 4, 3, 2, 1])

# print solution([1, 5, 9])
#print solution([1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6])
# print solution([1, 1, 1])
# print solution([1, 1, 1, 1])
# print solution([1, 1, 1, 1, 1])
# print solution([1, 1, 1, 1, 1, 1])
# print solution([1, 1, 1, 1, 1, 1, 1])
#
# num = 0
# for i in range(2000):
#     num += triangle_number(i)
# print num
