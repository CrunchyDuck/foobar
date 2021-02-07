class MapNode:
    def __init__(self):
        self.src_distance = 0  # How far from the end, if all walls were ignored.
        self.dest_distance = 0  # Jumps from the starting position.
        self.closed = False
        self.neighbours = []
        self.pos = []  # debug thing


def in_list_bounds(list_size, pos):
    """
    Check if an position falls out of the bounds of a list's dimensions.

    Arguments:
        list_size - [width, height] of the list.
        pos - [x, y] of the position in the list
    Returns:
        True if in bounds, False if not.
    """
    if pos[0] < 0 or\
       pos[1] < 0 or\
       pos[0] >= list_size[0] or\
       pos[1] >= list_size[1]:
        return False
    return True


def solution(map):
    map_size = {
        "height": len(map),
        "width": len(map[0])
    }
    dest_x = dest_y = 0
    src_x = map_size["width"]
    src_y = map_size["height"]

    open_set = []
    map_grid = [[MapNode() for _ in range(map_size["height"])] for _ in range(map_size["width"])]

    neighbour_pos = [
        [1, 0],   # Right
        [-1, 0],  # Left
        [0, 1],   # Down
        [0, -1],  # Up
    ]

    # Fill node neighbours
    for y in range(map_size["height"]):
        for x in range(map_size["width"]):
            this_node = map_grid[x][y]
            this_node.pos = [x, y]

            # Locate neighbours
            for move in neighbour_pos:
                target_x = x + move[0]
                target_y = y + move[1]
                # Check if neighbour is within the board.
                if in_list_bounds([map_size["width"], map_size["height"]], [target_x, target_y]):
                    this_node.neighbours.append(map_grid[target_x][target_y])


    open_set.append(map_grid[src_x][src_y])
    target_node = map_grid[dest_x][dest_y]

    # Run through the full maze, documenting the distances of each cell.
    while len(open_set):
        # As I'm documenting all nodes, I don't need to set up a heap, just check all of them eventually.
        current_node = open_set[0]

        open_set.remove(current_node)
        current_node.closed = True

        neighbour_distance = current_node.distance + 1  # How far the neighbour node is from src.
        for neighbour in current_node.neighbours:
            if neighbour.closed: continue

            neighbour_open = neighbour in open_set
            if not neighbour_open or neighbour.distance > neighbour_distance:
                neighbour.distance = current_node.distance + 1
                if not neighbour_open:
                    open_set.append(neighbour)




# solution([[0, 1, 1, 0],
#           [0, 0, 0, 1],
#           [1, 1, 0, 0],
#           [1, 1, 1, 0]])

solution([[0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1],
          [0, 1, 1, 1, 1, 1],
          [0, 0, 0, 0, 0, 0]])