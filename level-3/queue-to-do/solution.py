def solution(start, length):
    """
    Calculates the security checksum for a checkpoint with the given values.
    Arguments:
        start - First number in the queue
        length - The length of the queue

    Returns:
        (int) Checksum for this checkpoint.
    """
    row = 0
    cap = length
    checksum = 0

    while cap > 0:
        row_start = start + (length * row)  # First number in row.
        for i in range(cap):
            checksum ^= (row_start + i)
        row += 1
        cap -= 1
    return checksum