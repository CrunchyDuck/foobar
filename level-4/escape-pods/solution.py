class RoomNode:
    """
    Represents a room and all of the corridors connected to it.
    Attributes:
        map - The map this node belongs to.
        self.pathed - If this room has had a path drawn to it from an exit.

        to_nodes - Nodes this object flows into. [#][0] = node, [#][1] = corridor size
        from_nodes - Nodes that flow into this object. Same structure as to_nodes

        in_room - Bunnies currently stored in this room.
        room_capacity - How many bunnies this room can store.
        room_left - How many more bunnies can fit in this room. (property)

        this_flow_in - How many bunnies entered this cell last tick.
        this_flow_in_tick - Which tick this_flow_in was calculated.

        start_room - If this room is a start room.
        end_room - If this room is an end room.

    Methods:
        make_corridor(other, size)
            Creates a corridor from this room to another.
        flow_out()
            Makes this room push as much out to connected rooms as it can.
        flow_in()
            Sucks in as many bunnies from connected rooms as it can.
        update_tick()
            Resets this_flow_in and updates this_flow_in_tick.
    """
    def __init__(self, room_map):
        self.map = room_map
        self.pathed = False

        self.to_nodes = []
        self.from_nodes = []

        self.in_room = 0
        self.room_capacity = 0  # Defined by how many bunnies can flow out per tick. Allows dead ends/loops to fill up.

        self.start_room = False
        self.end_room = False

        self.this_flow_in = 0
        self.this_flow_in_tick = 0

    @property
    def room_left(self):
        return self.room_capacity - self.in_room

    def make_corridor(self, other, size):
        """
        Create a corridor from this room to another. Corridors are one-way.

        Arguments:
            other - The node to make an edge to.
            size - How many bunnies can fit through this
        """
        self.to_nodes.append([other, size])
        other.from_nodes.append([self, size])

    def flow_out(self):
        """
        Push as many bunnies out of connected corridors as possible.
        This is only used by start nodes, which contain infinite bunnies.
        This is done so that loops or inefficient paths will eventually be blocked.
        """
        for to_room in self.to_nodes:
            target_room = to_room[0]
            corridor = to_room[1]
            target_room.update_tick()

            bunnies_to_go = max(min(self.in_room, corridor), 0)
            self.in_room -= bunnies_to_go
            target_room.in_room += bunnies_to_go
            target_room.this_flow_in += bunnies_to_go

    def flow_in(self):
        """
        Pulls bunnies in from adjacent rooms.
        Rooms cannot pull from start or end rooms, as these are handled manually.
        """
        self.update_tick()
        for from_room in self.from_nodes:
            target_room = from_room[0]
            corridor = from_room[1]
            # Start rooms flow out at the start of each frame, thus they don't need to be taken from again.
            if target_room.start_room or target_room.end_room:
                continue

            bunnies_to_go = min(target_room.in_room, corridor)
            if not self.end_room:
                bunnies_to_go = min(bunnies_to_go, self.room_left)
            bunnies_to_go = max(bunnies_to_go, 0)

            target_room.in_room -= bunnies_to_go
            self.in_room += bunnies_to_go
            self.this_flow_in += bunnies_to_go

    def update_tick(self):
        """
        Reset counters and updates the current tick if applicable.
        """
        if self.this_flow_in_tick != self.map.tick:
            self.this_flow_in = 0  # How many bunnies entered this room this tick.
            self.this_flow_in_tick = self.map.tick


class RoomMap:
    """
    Represents a collection of RoomNodes.
    Attributes:
        room_map
    """
    def __init__(self, entrances, exits, path):
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
        room_map = [RoomNode(self) for _ in range(len(path))]

        # Mark exit and entrance nodes.
        for num in exits:
            room = room_map[num]
            self.exit_rooms.append(room)
            room.pathed = True  # These are manually added and don't need to be algorithmically found.
            room.end_room = True
        for num in entrances:
            room = room_map[num]
            self.entrance_rooms.append(room)
            room.start_room = True

        # Create corridors
        for i, room_corridors in enumerate(path):
            start_room = room_map[i]
            for j, corridor_size in enumerate(room_corridors):
                if corridor_size > 0:
                    end_room = room_map[j]
                    start_room.make_corridor(end_room, corridor_size)
                    start_room.room_capacity += corridor_size

    def generate_path(self):
        """
        Creates a path, traced from the exit node to the start node.
        """
        path = []
        open_nodes = list(self.exit_rooms)  # Copy the existing list.

        for node in open_nodes:
            if node.start_room:  # The start nodes do not need to be mapped, as they never pull inward.
                continue
            path.append(node)
            for connected_node in node.from_nodes:
                connected_node = connected_node[0]
                if not connected_node.pathed:
                    open_nodes.append(connected_node)
                    connected_node.pathed = True

        return path

    def update(self):
        """
        Runs a tick of simulation on the map.
        If there is no change in the flow of water, equilibrium=True.

        When simulating, we perform a breadth first search from the exit node until all input nodes are "flowed"
        This ensures that nodes that do not connect to the exit are ignored.
        """
        self.tick += 1
        this_flow_amount = 0  # How many bunnies moved on the map this tick.

        for room in self.entrance_rooms:
            # Flow from the entrances outwards before everything else.
            # This ensures loops/dead-ends will fill up and reach equilibrium.
            room.in_room = room.room_capacity * 2  # Fill entrance rooms such that they will never run out of bunnies.
            room.flow_out()

        # Make each mapped node flow.
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
print solution([0], [2],  # answer: 1
          [[0, 5, 0],
           [5, 0, 1],
           [0, 0, 0]])
print solution([0, 1], [5],  # answer: 7
           [[0, 0, 10, 0, 0, 0],
            [0, 0, 0, 5, 0, 0],
            [0, 0, 0, 0, 0, 2],
            [0, 0, 5, 0, 5, 0],
            [0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 0]])
print solution([0], [3],  # answer: 1
            [[0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 1, 0, 3],
             [0, 0, 2, 0]])