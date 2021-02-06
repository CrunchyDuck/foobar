class ChessBoardNode():
    def __init__(self, posx, posy):
        self.distance = 0  # Jumps from the starting position.
        self.closed = False
        self.neighbours = []

        self.pos = [posx, posy]  # Debugging purposes.


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



def solution(src, dest):
    """
    Finds the fewest number of moves for a knight at src moving to dest.
    Uses a modified A* pathfinding algorithm.

    Arguments:
        src: The index on the board the knight starts at.
        dest: The destination for the knight.

    Returns:

    """
    board_size = 8
    src_y, src_x = divmod(src, board_size)
    dest_y, dest_x = divmod(dest, board_size)

    open = []
    board = [[ChessBoardNode(x, y) for x in range(board_size)] for y in range(board_size)]
    # All possible moves relative to the current position.
    neighbour_pos = [
        # Right
        [2, -1],
        [2, 1],
        # Down
        [1, 2],
        [-1, 2],
        # Left
        [-2, -1],
        [-2, 1],
        # Up
        [1, -2],
        [-1, -2]
    ]

    # Fill node neighbours
    # As this is specifically for the knight, neighbours are calculated on its moveset.
    for y in range(len(board)):
        for x in range(len(board[0])):
            this_node = board[x][y]

            # Locate neighbours
            for move in neighbour_pos:
                target_x = x + move[0]
                target_y = y + move[1]
                # Check if neighbour is within the board.
                if in_list_bounds([board_size, board_size], [target_x, target_y]):
                    this_node.neighbours.append(board[target_x][target_y])

    open.append(board[src_x][src_y])
    target_node = board[dest_x][dest_y]

    while len(open):
        current_node = open[0]

        # Find node with lowest distance from start.
        for i in range(1, len(open)):
            if open[i].distance < current_node.distance:
                current_node = open[i]

        open.remove(current_node)
        current_node.closed = True

        if current_node == target_node:
            return current_node.distance

        neighbour_distance = current_node.distance + 1  # How far the neighbour node is from src.
        for neighbour in current_node.neighbours:
            if neighbour.closed: continue

            neighbour_open = neighbour in open
            if not neighbour_open or neighbour.distance > neighbour_distance:
                neighbour.distance = current_node.distance + 1
                if not neighbour_open:
                    open.append(neighbour)


print solution(19, 36)