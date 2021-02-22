class RoomNode:
    def __init__(self, map):
        self.to_nodes = []  # list of lists where [#][0] is the node and [#][1] is the size of this hall.
        self.in_room = 0  # Bunnies currently in this cell.
        self.room_capacity = 0  # How many bunnies this room can store. Defined by how many can flow out per tick. Allows dead ends/loops to fill up.
        self.destination = False  # If this cell is an escape pod.
        self.last_updated = 0  # Which tick this node was last updated on.
        self.last_flow = 0  # How many bunnies entered this cell last flood tick
        self.map = map  # The map this node belongs to.

    @property
    def room_left(self):
        return self.room_capacity - self.in_room

    def make_corridor(self, other, size):
        """
        Create a corridor between two rooms. Corridors are one-way.

        Arguments:
            other - The node to make an edge to.
            size - How many bunnies can fit through this
        """
        self.to_nodes += [other, size]

    def flow(self):
        """Push as many bunnies out of connected corridors as possible."""
        for to_room in self.to_nodes:
            target_room = to_room[0]
            corridor = to_room[1]

            bunnies_to_go = min(min(self.in_room, corridor), target_room.room_left)
            self.in_room -= bunnies_to_go
            target_room.in_room += bunnies_to_go


class RoomMap:
    def __init__(self, entrances, exits, path):
        self.room_map = []
        self.entrance_rooms = []
        self.exit_rooms = []
        self.open_nodes = []
        self.generate_map(entrances, exits, path)

        self.ticks = 0  # How many ticks of simulation have passed.

    def generate_map(self, entrances, exits, path):
        # Create the list of empty rooms
        self.room_map = [RoomNode(self) for _ in range(len(path))]

        # Mark exit and entrance nodes.
        self.exit_rooms = [self.room_map[num] for num in exits]
        self.entrance_rooms = [self.room_map[num] for num in entrances]

        # Create corridors
        for i, room_corridors in enumerate(path):
            start_room = self.room_map[i]
            for j, corridor_size in enumerate(room_corridors):
                if corridor_size > 0:
                    end_room = self.room_map[j]
                    start_room.make_corridor(end_room, corridor_size)
                    start_room.room_capacity += corridor_size

    def update(self):
        """
        Runs a tick of simulation on the map.
        """


def solution(entrances, exits, path):
    # Create data structure
    room_map = RoomMap(entrances, exits, path)

    # Flood structure.
    pass


n = RoomNode(None)
n.room_capacity = 5
n.in_room = 3
print n.room_left
exit()

solution([0, 1], [4, 5],
         [[0, 0, 4, 6, 0, 0],
          [0, 0, 5, 2, 0, 0],
          [0, 0, 0, 0, 4, 4],
          [0, 0, 0, 0, 6, 6],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0]])
solution([0], [3],
         [[0, 7, 0, 0],
          [0, 0, 6, 0],
          [0, 0, 0, 8],
          [9, 0, 0, 0]])