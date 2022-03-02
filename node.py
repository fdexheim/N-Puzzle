from tools import tile_value_yx
from tools import tile_yx
from env import g_env
from heuristics import heuristic
import hashlib

class Node:
    def __init__(self, puzzle, parent=None, move=None):
        self.puzzle = puzzle
        self.parent = parent
        self.move = move
        self.uid = g_env.uid
        g_env.uid += 1
        if (move != None):
            y0, x0 = tile_yx(puzzle, 0)
            val = tile_value_yx(puzzle, y0 + move.y, x0 + move.x)
            puzzle[y0][x0] = val
            puzzle[y0 + move.y][x0 + move.x] = 0
        self.puzzle_hash = hashlib.md5(str(self.puzzle).encode('utf-8')).hexdigest()
        self.g = 0
        if (self.parent != None):
            self.g = parent.g + 1
        self.h = heuristic(self.puzzle)
        self.f = self.g + self.h


    def equals(self, compare):
        if self.puzzle_hash == compare.puzzle_hash:
            return True
        return False



    def is_solved(self):
        if self.puzzle_hash == g_env.desired_board_hash:
            return True
        return False


    def print_data(self, name):
        print("node {0}   uid = {1}   f = {2}   g = {3}   h = {4}   hash = {5}".format(name, self.uid, self.f, self.g, self.h, self.puzzle_hash))

    def print_puzzle(self):
        for i in range(0, len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                if (self.puzzle[i][j] < 10):
                    print(" " + str(self.puzzle[i][j]), end=' ')
                else:
                    print(str(self.puzzle[i][j]), end = " ")
            print("");
