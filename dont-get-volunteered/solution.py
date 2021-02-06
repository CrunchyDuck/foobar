class ChessBoardNode():
    def __init__(self):
        self.h_cost = 0
        self.g_cost = 0
        self.f_cost = 0
        self.open = False
        self.neighbours = []

    def update(self, h, g):
        self.g_cost = g
        self.h_cost = h
        self.f_cost = g + h


def solution(src, dest):
    open = []
    closed = []
    board_size = 8
    board = [[ChessBoardNode() for x in range(board_size)] for y in range(board_size)]
    # As this is specifically for the knight, neighbours are calculated on its moveset.


solution(0, 1)