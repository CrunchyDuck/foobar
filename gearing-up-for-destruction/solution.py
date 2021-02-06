def try_gear(radius, differences):
    """
    Tries a gear with a given radius.
    Arguments:
        radius - The radius of the first gear
        differences - The space between each pair of pegs.

    Returns:
        The radius of the gears for each peg.
    """
    radii = [radius]
    for i in range(len(differences)):
        radius = differences[i] - radius
        radii.append(radius)

    return radii


def solution(pegs):
    """
    Calculates the size of the first gear for the LAMBCHOP doomsday device's axial orientation gears.
    The final gear must be half the size of the first gear.

    Arguments:
        pegs - A list of the positions of pegs in ascending order.

    Returns:
        [numerator, denominator] of the first gear to be placed.
        [-1, -1] if there is no valid configuration.
    """
    unsolvable = [-1, -1]
    number_of_pegs = len(pegs)

    # Calculate the space between each of the pegs.
    peg_spaces = []
    for i in range(1, len(pegs)):
        val_diff = pegs[i] - pegs[i - 1]
        peg_spaces.append(val_diff)

    # Figure out the numerator and denominator of the first gear, given that the last must be twice its size.
    dummy = try_gear(0, peg_spaces)  # A dummy configuration used to calculate the difference between first and last gear.
    if number_of_pegs % 2 == 1:
        # The relationship between first and last gear is linear.
        numerator = (dummy[0] - dummy[-1]) * 2
        denominator = 1
    else:
        # The relationship between the first and last gear is inverse.
        numerator = (dummy[0] + dummy[-1]) * 2
        denominator = 3

        # Simplify fraction
        if numerator % denominator == 0:
            numerator /= denominator
            denominator /= denominator

    # Check all gears are valid sizes given the size of the first gear.
    first_gear = numerator / denominator
    gear_configuration = try_gear(first_gear, peg_spaces)
    for gear in gear_configuration:
        if gear < 1:
            return unsolvable

    return [numerator, denominator]




ex1 = [0, 15, 25]  # 10, 5, 5
ex2 = [4, 30, 50]  # 12, 14, 6
ex3 = [0, 22, 48, 70]  # 12, 10, 16, 6
ex4 = [0, 5, 8, 11]  # 3.33, 1.66, 1.33, 1.66
print solution(ex4)