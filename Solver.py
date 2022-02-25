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
        y, x = tile_yx(node.puzzle, 0)
        ret = []
        for move in moves:
            cmpy = y + move.y
            cmpx = x + move.x
            # exclude cases where previous move was the opposite
            if (node.move != None):
                if node.move.move == 'd' and move.move == 'u':
                    continue
                if node.move.move == 'u' and move.move == 'd':
                    continue
                if node.move.move == 'l' and move.move == 'r':
                    continue
                if node.move.move == 'r' and move.move == 'l':
                    continue
            if (cmpx >= 0 and cmpx < g_env.puzzle_width and cmpy >= 0 and cmpy < g_env.puzzle_width):
                ret.append(move)
        return ret



    def try_curate_moves(self, parent, moves):
        nodes = []
        curated_nodes = []
        existing_closed_nodes = 0
        existing_opened_nodes = 0
        for move in moves:
            new_node = Node(copy.deepcopy(parent.puzzle), parent, move)
            for closed_node in self.closed_nodes:
                if (new_node.equals(closed_node) == True):
                    existing_closed_nodes += 1
                    continue
            for opened_node in self.opened_nodes:
                if (new_node.equals(opened_node) == True):
                    existing_opened_nodes += 1
                    continue
            nodes.append(new_node)
        #print(str(existing_nodes) + " Existing node found in closed_nodes")
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
            print("============= ITER " + str(i) + " ==============")
            print(str(len(self.opened_nodes)) + " opened_nodes")
            for node in self.opened_nodes:
                node.print_puzzle()
                print("")
            print(str(len(self.closed_nodes)) + " closed_nodes")
            for node in self.closed_nodes:
                node.print_puzzle()
                print("")
            add_nodes = []
            for op in self.opened_nodes:
                if (op.is_solved() == True):
                    print("SOLVED")
                    time_end = time.clock()
                    print("time to solve : " + str(time_end - time_start))
                    exit()
                self.opened_nodes.remove(op)
                self.closed_nodes.append(op)
                moves = self.get_possible_moves(op)
                add_nodes = self.try_curate_moves(op, moves)
                print(str(len(add_nodes)) + " add_nodes")
            for add_node in add_nodes:
                self.opened_nodes.append(add_node)
                print("");
            if (i >= 5):
                break
            #print("\n")
