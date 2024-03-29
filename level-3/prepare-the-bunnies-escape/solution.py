from heapq import heapify, heappop, heappush
import cProfile


class MapNode:
    """
    A representation of a square in a grid.

    Attributes:
        pos - [x, y] position of this node on the map.
        src_distance - Distance from the start position using best path
        dest_distance - Distance from the end position, ignoring all walls.
        cell_cost - Higher cost makes a cell less desirable.
        closed - Whether this node have been directly updated.
        opened - Whether this node has been opened already.
        wall - Whether this node is a wall.
        neighbours - A list of nodes neighbouring this node.
    """
    def __init__(self, is_wall, x, y):
        """
        Arguments:
            is_wall - If this cell is a wall.
            x - x position in maze.
            y - y position in maze.
        """
        self.pos = [x, y]
        self.src_distance = 1  # Jumps from the starting position.
        self.dest_distance = x + y  # How far from the end, if all walls were ignored.
        self.cell_cost = 0
        self.closed = False
        self.opened = False  # This is much faster to check than iterating over the open list.
        self.wall = is_wall

        self.neighbours = []

    def __cmp__(self, other):
        return cmp(self.cell_cost, other.cell_cost)

    def set_distance(self, dist):
        """
        Updates the distance and cost of a cell.
        Arguments:
            dist - Distance from the source cell.
        """
        self.src_distance = dist
        # For some reason this value is always off by 1.
        # But, since all values are incorrect, it makes it correct again! Huzzah!
        # I think it might actually be off by 2, but due to the +1 to all src_distance values, reduces that gap.
        self.cell_cost = self.src_distance + self.dest_distance


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


def generate_map_grid(map, width, height):
    """
    Creates a map grid filled with map notes.
    Returns:
        mapgrid[x][y]
    """
    return [[MapNode(map[y][x], x, y) for y in range(height)] for x in range(width)]


def fill_neighbours(map_grid, neighbour_positions):
    """
    Takes in a map_grid filled with MapNodes, and updates the position and neighbours of each node.
    Arguments:
        map_grid - A grid of [x][y] filled with MapNodes
        neighbour_positions - An array of [[x,y],...] with the position of neighbours of each cell.
    """
    neighbour_pos = neighbour_positions
    width = len(map_grid)
    height = len(map_grid[0])

    for y in range(height):
        for x in range(width):
            this_node = map_grid[x][y]
            this_node.pos = [x, y]

            # Locate neighbours
            for move in neighbour_pos:
                target_x = x + move[0]
                target_y = y + move[1]
                # Check if neighbour is within the board.
                if in_list_bounds([width, height], [target_x, target_y]):
                    this_node.neighbours.append(map_grid[target_x][target_y])


def solution(map):
    """
    Calculates the shortest path in a maze when allowed to remove one wall.
    Arguments:
        map[y][x] - A 2D array representing a map of the maze.

    Returns:
        (int) Shortest path when able to remove one wall.
    """
    map_size = {
        "height": len(map),
        "width": len(map[0])
    }
    dest_x = dest_y = 0
    src_x = map_size["width"] - 1
    src_y = map_size["height"] - 1

    neighbour_pos = [
        [1, 0],  # Right
        [-1, 0],  # Left
        [0, 1],  # Down
        [0, -1],  # Up
    ]
    map_grid = generate_map_grid(map, map_size["width"], map_size["height"])
    fill_neighbours(map_grid, neighbour_pos)

    wall_heap = []
    start_node = map_grid[src_x][src_y]
    start_node.opened = True
    open_set = [start_node]
    target_node = map_grid[dest_x][dest_y]

    # Run through the full maze from the start, documenting the distances of each cell.
    while len(open_set):
        # As I'm documenting all nodes, I don't need to set up a heap, just check all of them eventually.
        current_node = open_set[0]

        open_set.remove(current_node)
        current_node.closed = True

        src_distance = current_node.src_distance + 1  # How far the neighbour node is from src.
        for neighbour in current_node.neighbours:
            if neighbour.closed:
                continue

            neighbour_open = neighbour.opened
            if not neighbour_open or neighbour.src_distance > src_distance:
                neighbour.set_distance(src_distance)
                if not neighbour_open:
                    neighbour.opened = True
                    if neighbour.wall:
                        wall_heap.append(neighbour)
                    else:
                        open_set.append(neighbour)

    if target_node.opened:
        best_speed = target_node.src_distance  # Currently, the fastest time to the exit, without changing any walls.
        lowest_cost = target_node.cell_cost
    else:
        # End was not reached.
        best_speed = 9999999
        lowest_cost = 9999999
    heapify(wall_heap)
    wall_heap_size = len(wall_heap)

    # Regenerate the map with the target wall removed, and check the new best speed.
    # This new iteration is done in standard A*.
    for i in range(wall_heap_size):
        wall = heappop(wall_heap)
        if wall.cell_cost >= lowest_cost:
            return best_speed

        map_modified = generate_map_grid(map, map_size["width"], map_size["height"])
        fill_neighbours(map_modified, neighbour_pos)
        wall_pos = wall.pos
        map_modified[wall_pos[0]][wall_pos[1]].wall = False
        target_node = map_modified[dest_x][dest_y]

        open_set = [map_modified[src_x][src_y]]

        while len(open_set):
            current_node = heappop(open_set)
            current_node.closed = True

            if current_node.pos == [0, 0]:
                # Check if the best speed on this is faster.
                speed = target_node.src_distance
                if speed < best_speed:
                    best_speed = speed
                    lowest_cost = target_node.cell_cost
                break

            src_distance = current_node.src_distance + 1
            for neighbour in current_node.neighbours:
                if neighbour.wall or neighbour.closed:
                    continue

                if not neighbour.opened or neighbour.src_distance > src_distance:
                    neighbour.set_distance(src_distance)
                    if not neighbour.opened:
                        neighbour.opened = True
                        heappush(open_set, neighbour)

    return best_speed


print solution([[0, 1, 1, 0],
          [0, 0, 0, 1],
          [1, 1, 0, 0],
          [1, 1, 1, 0]])

print solution([
    [0, 0],
    [1, 0],
    [1, 0],
    [1, 0],
    [0, 0],
    [0, 1],
    [1, 1],
    [0, 0],
    [0, 1],
    [0, 1],
    [0, 0]
])

print solution([
    [0,0,0,1,0,0],
    [1,1,1,1,0,0],
    [0,0,0,1,0,0],
    [0,0,0,1,0,0],
    [0,0,0,1,0,0],
    [0,0,0,1,0,0]
])

print solution([[0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1],
          [0, 1, 1, 1, 1, 1],
          [0, 0, 0, 0, 0, 0]])

print solution([[0]])


# chunky.
def test():
    print solution(
    [
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0],
    [0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0],
    [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1],
    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
    [0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
    [0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0],
    [1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0],
    [0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0],
    [0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0]
    ]
)


cProfile.run("test()", sort="cumtime")