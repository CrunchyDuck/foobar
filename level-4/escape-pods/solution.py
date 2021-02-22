class RoomNode:
    def __init__(self, map, node_num):
        self.node_num = node_num  # Debugging purposes

        self.to_nodes = []  # list of lists where [#][0] is the node and [#][1] is the size of this hall.
        self.from_nodes = []  # List of nodes that flow into this node.
        self.in_room = 0  # Bunnies currently in this cell.
        self.room_capacity = 0  # How many bunnies this room can store. Defined by how many can flow out per tick. Allows dead ends/loops to fill up.
        self.start_room = False  # If this room is a start node.
        self.this_flow_in = 0  # How many bunnies entered this cell last flood tick
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
        self.this_flow_in = 0  # How many bunnies entered this room this tick.
        for from_room in self.from_nodes:
            target_room = from_room[0]
            corridor = from_room[1]

            bunnies_to_go = min(target_room.in_room, corridor)  # Flow the amount this corridor can support, or all in this room.
            target_room.in_room -= bunnies_to_go
            self.in_room += bunnies_to_go
            self.this_flow_in += bunnies_to_go

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
        self.exit_flow_amount = 0  # How many bunnies entered the exit last tick.
        self.last_flow_amount = 0  # How many bunnies moved on the map last tick.
        self.equilibrium = False  # If the system has reached its end state.

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
        open_nodes = list(self.exit_rooms)  # Copy the existing list.

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
        self.tick += 1

        # Fill entrance rooms such that they will never run out of bunnies.
        for room in self.entrance_rooms:
            room.in_room = room.room_capacity * 2

        # Make each node flow.
        this_flow_amount = 0  # How many bunnies moved on the map this tick.
        for node in self.path:
            node.flow_in()
            this_flow_amount += node.this_flow_in

        # Check flow amount on exit nodes.
        self.exit_flow_amount = 0
        for exit_room in self.exit_rooms:
            self.exit_flow_amount += exit_room.this_flow_in

        # Evaluate if the system is in equilibrium.
        if this_flow_amount == self.last_flow_amount:
            self.equilibrium = True
        else:
            self.equilibrium = False
            self.last_flow_amount = this_flow_amount


def solution(entrances, exits, path):
    # Create data structure
    room_map = RoomMap(entrances, exits, path)

    # Flood structure.
    while not room_map.equilibrium:
        room_map.update()

    return room_map.exit_flow_amount


print solution([0], [3],  # answer: 1
         [[0, 1, 0, 0],
          [0, 0, 1, 1],
          [1, 0, 0, 0],
          [0, 0, 50, 0]])

print solution([0, 1], [4, 5],  # answer: 16
         [[0, 0, 4, 6, 0, 0],
          [0, 0, 5, 2, 0, 0],
          [0, 0, 0, 0, 4, 4],
          [0, 0, 0, 0, 6, 6],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0]])
print solution([0], [3],  # answer: 6
         [[0, 7, 0, 0],
          [0, 0, 6, 0],
          [0, 0, 0, 8],
          [9, 0, 0, 0]])