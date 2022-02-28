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
            node_already_exists = False
            for closed_node in self.closed_nodes:
                if (new_node.equals(closed_node) == True):
                    existing_closed_nodes += 1
                    node_already_exists = True
                    break
            for opened_node in self.opened_nodes:
                if (new_node.equals(opened_node) == True):
                    existing_opened_nodes += 1
                    node_already_exists = True
                    break
            if node_already_exists == False:
                nodes.append(new_node)
        if (g_env.heuristics == False):
            curated_nodes = nodes;
        else:
            curated_moves = 0 #this is where heuristics should kick in
        return curated_nodes


    def get_inversion_count(self, puz):
        inversions = 0
        for i in range(0, len(puz)):
            for j in range(i + 1, len(puz)):
                if (puz[i] != 0 and puz[j] != 0 and puz[i] > puz[j]):
                    inversions += 1
        return inversions


    def check_solvability(self, initial_puzzle):
        one_d_board = []
        one_d_ref = []
        for i in range(0, g_env.puzzle_width):
            for j in range(0, g_env.puzzle_width):
                one_d_board.append(initial_puzzle[i][j])
                one_d_ref.append(g_env.desired_board[i][j])
        print(one_d_board)
        print(one_d_ref)
        inversion_board = self.get_inversion_count(one_d_board)
        inversion_ref = self.get_inversion_count(one_d_ref)
        print(inversion_board)
        print(inversion_ref)
        if (g_env.puzzle_width % 2 == 0):
            inversion_board += one_d_board.index(0)
            inversion_ref += one_d_ref.index(0)
        print(inversion_board)
        print(inversion_ref)
        if (inversion_board % 2 == inversion_ref % 2):
            return True
        return False


    def print_solution(self, node):
        nodes = []
        moves = ""
        ptr = node
        while (ptr.parent != None):
            nodes.append(ptr)
            moves += ptr.move.move
            ptr = ptr.parent
        print(len(nodes))
        for snode in nodes[::-1]:
            snode.print_puzzle()
            print("")
        print(moves[::-1])
        print("max_states    : " + str(g_env.max_states))
        print("opened_states : " + str(g_env.opened_states))


    def solve(self, initial_puzzle):
        solvable = self.check_solvability(initial_puzzle)
        if (solvable == False):
            print("Input puzzle has no solution")
            exit()
        time_start = time.clock()
        firstNode = Node(copy.deepcopy(initial_puzzle), None, None)
        self.opened_nodes.append(firstNode)
        i = 0;
        while (len(self.opened_nodes) > 0):
            i += 1
            print("============= ITER " + str(i) + " ==============")
            tot_states = len(self.opened_nodes) + len(self.closed_nodes)
            if tot_states > g_env.max_states:
                g_env.max_states = tot_states
            print(str(len(self.opened_nodes)) + " opened_nodes")
            for node in self.opened_nodes:
                print(node.uid, end=" ")
            print("")
            #for node in self.opened_nodes:
            #    node.print_puzzle()
            #    print("")
            print(str(len(self.closed_nodes)) + " closed_nodes")
            for node in self.closed_nodes:
                print(node.uid, end=" ")
            print("")
            #for node in self.closed_nodes:
            #    node.print_puzzle()
            #    print("")
            add_nodes = []
            iter_add_nodes = []
            process_nodes = []
            for op in self.opened_nodes:
                process_nodes.append(op)
            for op in process_nodes:
                print("processsing node " + str(op.uid))
                if (op.is_solved() == True):
                    print("SOLVED")
                    time_end = time.clock()
                    self.print_solution(op)
                    print("time to solve : " + str(time_end - time_start))
                    exit()
                self.opened_nodes.remove(op)
                self.closed_nodes.append(op)
                moves = self.get_possible_moves(op)
                add_nodes = self.try_curate_moves(op, moves)
                for add_node in add_nodes:
                    self.opened_nodes.append(add_node)
                    iter_add_nodes.append(add_node)
            print(str(len(iter_add_nodes)) + " iter_add_nodes ", end=" : ")
            for node in iter_add_nodes:
                print(node.uid, end=" ")
            print("");
            if (i >= 5):
                print("")
                break
            #print("\n")
