def rotate_string(string, offset):
    """
    Rotate a string an amount of times.
    Arguments:
        string - String to rotate
        offset - How much to rotate the string.

    Returns:
        String after rotation has been applied.
    """
    size = len(string)
    offset = offset % size  # Stops string slicing messing up.
    rotated_string = string[-offset:] + string[:size-offset]
    return rotated_string


def get_factors(number):
    """
    Returns a list of all of the positive factors of this number.
    Arguments:
        number - The number to get factors of.

    Returns:
        list of positive integers
    """
    factors = []
    for num in range(1, number+1):
        if number % num == 0:
            factors.append(num)
    return factors


def solution(s):
    string_size = len(s)
    factors = get_factors(string_size)  # As the pattern must span the whole string, the answer must be a factor.

    # The factor is the length of pattern we're going to attempt.
    for factor in factors:
        # We'll want to "rotate" the string/cake enough to make sure that every viable pattern
        # of this size is tried.
        for offset in range(factor):
            s_rotated = rotate_string(s, offset)
            pattern = s_rotated[0:factor]
            pattern_fits = True
            pattern_parts = string_size / factor
            # Check if this pattern repeats through the string.
            for i in range(pattern_parts):
                start = i * factor
                end = (i + 1) * factor
                if s_rotated[start:end] != pattern:
                    # If the pattern doesn't match up with any part of the string, it doesn't fit.
                    pattern_fits = False
                    break

            if pattern_fits:
                return pattern_parts


print solution("abcabc")
print solution("abcabcabcabcabcabcabcabc")
print solution("bcabca")
print solution("abccba")