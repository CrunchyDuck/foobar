def f(a):
    res = [a, 1, a + 1, 0]
    return res[a % 4]

def get_xor(start, end):
    """
    Gets the XOR of a range of numbers from start to end.
    Solution inspired by:
    https://stackoverflow.com/questions/10670379/find-xor-of-all-numbers-in-a-given-range

    Arguments:
        start - The first number in the range
        end - The last number in the range.

    Returns:
        The XOR of all of the numbers in the range.
    """
    return f(end) ^ f(start - 1)

def solution(start, length):
    """
    Calculates the security checksum for a checkpoint with the given values.
    Arguments:
        start - First number in the queue
        length - The length of the queue

    Returns:
        (int) Checksum for this checkpoint.
    """
    cap = length
    checksum = 0

    while cap > 0:
        checksum ^= get_xor(start, start + cap - 1)
        start = start + length
        cap -= 1

    return checksum

print solution(17, 4)
#print solution(5, 500)
#print solution(200000000, 2)
print solution(2, 2000000)