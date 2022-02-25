import time
import copy
import math
from tools import tile_yx
from node import Node
from env import g_env

class Direction:
    def __init__(self, move, y, x):
        self.move = move
        self.y = y
        self.x = x

class Solver:
    def __init__(self):
        self.opened_nodes = []
        self.closed_nodes = [] #list of states already gone through
        return

    def check_closed_nodes(self, node_cmp):
        if (node_cmp in self.closed_nodes):
            return True
        return False

    def get_chain(self, node):
        tmp = node
        while (tmp != None):
            print(tmp)
            tmp = tmp.parent

    def add_node():
        return



    def get_possible_moves(self, node):
        moves = { Direction('u', -1, 0), Direction('d', 1, 0), Direction('l', 0, -1), Direction('r', 0, 1) }
        for move in moves:
            print(move)
        y, x = tile_yx(node.puzzle, 0)
        ret = []
        for move in moves:
            cmpy = y + move.y
            cmpx = x + move.x
            if (cmpx >= 0 and cmpx < g_env.puzzle_width and cmpy >= 0 and cmpy < g_env.puzzle_width):
                ret.append(move)
        return ret



    def try_curate_moves(self, parent, moves):
        nodes = []
        curated_nodes = []
        for move in moves:
            new_node = Node(copy.deepcopy(parent.puzzle), parent, move)
            for closed_node in self.closed_nodes:
                if (new_node.equals(closed_node) == True):
                    print("Existing node found in closed_nodes")
                    continue
            nodes.append(new_node)
        if (g_env.heuristics == False):
            curated_nodes = nodes;
        else:
            curated_moves = 0 #this is where heuristics should kick in
        return curated_nodes



    def solve(self, initial_puzzle):
        time_start = time.clock()

        firstNode = Node(copy.deepcopy(initial_puzzle), None, None)
        self.opened_nodes.append(firstNode)
        i = 0;
        while (len(self.opened_nodes) > 0):
            i += 1
            print(str(len(self.opened_nodes)) + " opened_nodes")
            print(str(len(self.closed_nodes)) + " closed_nodes")
            add_nodes = []
            for op in self.opened_nodes:
                op.print_puzzle()
                self.opened_nodes.remove(op)
                self.closed_nodes.append(op)
                moves = self.get_possible_moves(op)
                add_nodes = self.try_curate_moves(op, moves)
            for add_node in add_nodes:
                self.opened_nodes.append(add_node)
            if (i >= 4):
                break
        time_end = time.clock()
