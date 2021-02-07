def try_gear(radius, differences):
    """
    Tries a gear with a given radius.
    Arguments:
        radius - The radius of the first gear
        differences - The distance between each set of pegs.

    Returns the radius of the gears for each peg.
    """
    radiuses = [radius]
    for i in range(len(differences)):
        radius = differences[i] - radius
        radiuses.append(radius)

    return radiuses


def solution(pegs):
    unsolvable = [-1, -1]
    # Calculate the gap between each of the pegs.
    diff = []
    for i in range(1, len(pegs)):
        val_diff = abs(pegs[i] - pegs[i - 1])
        diff.append(val_diff)

    # Boundaries for the first gear.
    minimum = 2  # Gears must always be at least 1, and the last gear must be twice the first.
    last_maximum = diff[-1] - 1  # Maximum size of the last gear.
    maximum = min(diff[0] - 1, last_maximum * 2)

    a= try_gear(2, diff)
    b= try_gear(3, diff)
    c= try_gear(4, diff)

    # Try a dummy gear to figure out the difference between the first and last gear.
    dummy = try_gear(2, diff)
    number_distance = abs(dummy[0] - dummy[-1])  # The last gear should always be the distance to the first gear
    first_gear = number_distance * 2
    if first_gear > maximum:
        return unsolvable
    elif first_gear < minimum:
        return unsolvable

    # Check all gears are valid sizes.
    gear_configuration = try_gear(first_gear, diff)
    for gear in gear_configuration:
        if gear < 1:
            return unsolvable

    return [first_gear, 1]

print solution([0, 9, 12, 15])