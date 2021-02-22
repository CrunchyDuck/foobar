class RoomNode:
    def __init__(self, map, node_num):
        self.node_num = node_num  # Debugging purposes

        self.to_nodes = []  # list of lists where [#][0] is the node and [#][1] is the size of this hall.
        self.from_nodes = []  # List of nodes that flow into this node.
        self.in_room = 0  # Bunnies currently in this cell.
        self.room_capacity = 0  # How many bunnies this room can store. Defined by how many can flow out per tick. Allows dead ends/loops to fill up.
        self.start_room = False  # If this room is a start node.
        self.last_in = 0
        self.last_out = 0
        self.last_flow = 0  # How many bunnies entered this cell last flood tick
        self.map = map  # The map this node belongs to.
        self.pathed = False  # If a path has been mapped to here.

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
        self.to_nodes.append([other, size])
        other.from_nodes.append([self, size])

    def flow_out(self):
        """Push as many bunnies out of connected corridors as possible."""
        for to_room in self.to_nodes:
            target_room = to_room[0]
            corridor = to_room[1]

            bunnies_to_go = max(min(min(self.in_room, corridor), target_room.room_left), 0)
            self.in_room -= bunnies_to_go
            target_room.in_room += bunnies_to_go

            # Add uncalculated rooms to open list.
            if target_room.last_out != self.map.tick:
                self.map.open_rooms.append(target_room)
                target_room.last_out = self.map.tick

    def flow_in(self):
        """
        Pulls bunnies in from adjacent rooms.
        """
        for from_room in self.from_nodes:
            target_room = from_room[0]
            corridor = from_room[1]

            bunnies_to_go = min(target_room.in_room, corridor)  # Flow the amount this corridor can support, or all in this room.
            target_room.in_room -= bunnies_to_go
            self.in_room += bunnies_to_go

    def __repr__(self):
        return "Node %s with %s" % (self.node_num, self.in_room)


class RoomMap:
    def __init__(self, entrances, exits, path):
        self.room_map = []
        self.entrance_rooms = []
        self.exit_rooms = []
        self.generate_map(entrances, exits, path)
        self.path = self.generate_path()  # The rooms to flow from, in order.

        self.tick = 0  # How many ticks of simulation have passed.

    def generate_map(self, entrances, exits, path):
        # Create the list of empty rooms
        self.room_map = [RoomNode(self, i) for i in range(len(path))]

        # Mark exit and entrance nodes.
        for num in exits:
            room = self.room_map[num]
            self.exit_rooms.append(room)
            room.pathed = True  # These are manually added and don't need to be algorithmically found.
        for num in entrances:
            room = self.room_map[num]
            self.entrance_rooms.append(room)
            room.start_room = True

        # Create corridors
        for i, room_corridors in enumerate(path):
            start_room = self.room_map[i]
            for j, corridor_size in enumerate(room_corridors):
                if corridor_size > 0:
                    end_room = self.room_map[j]
                    start_room.make_corridor(end_room, corridor_size)
                    start_room.room_capacity += corridor_size

    def generate_path(self):
        """
        Creates a path, traced from the exit node to the start node.
        """
        path = []
        open_nodes = self.exit_rooms

        for node in open_nodes:
            path.append(node)
            if node.start_room:  # Don't map nodes that push to start rooms.
                continue
            for connected_node in node.from_nodes:
                connected_node = connected_node[0]
                if not connected_node.pathed:
                    open_nodes.append(connected_node)
                    connected_node.pathed = True

        return path

    def update(self):
        """
        Runs a tick of simulation on the map.

        When simulating, we perform a breadth first search from the exit node until all input nodes are "flowed"
        This ensures that nodes that do not connect to the exit are ignored.
        """
        for room in self.entrance_rooms:  # Fill entrance rooms such that they will never run out of bunnies.
            room.in_room = room.room_capacity * 2

        for node in self.path:
            self.tick += 1
            node.flow_in()



def solution(entrances, exits, path):
    # Create data structure
    room_map = RoomMap(entrances, exits, path)

    # Flood structure.
    while True:
        room_map.update()


# solution([0], [3],
#          [[0, 1, 0, 0],
#           [0, 0, 1, 1],
#           [1, 0, 0, 0],
#           [0, 0, 50, 0]])

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