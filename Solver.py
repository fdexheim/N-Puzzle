import time
import copy
import math
from tools import tile_yx, get_possible_moves, Direction
from node import Node
from env import g_env
from solvability import check_solvability


class Solver:
    def __init__(self):
        self.opened_nodes = []
        self.closed_nodes = { } #dictionary of states already gone through
        time_start = 0
        time_end = 0
        return


    def get_chain(self, node):
        tmp = node
        while (tmp != None):
            print(tmp)
            tmp = tmp.parent


    def print_solution(self, node):
        self.time_end = time.perf_counter()
        nodes = []
        moves = ""
        ptr = node
        while (ptr.parent != None):
            nodes.append(ptr)
            moves += ptr.move.move
            ptr = ptr.parent
        for snode in nodes[::-1]:
            snode.print_puzzle()
            print("")
        print("Moves required    : " + str(len(nodes)))
        print("Moves (tile 0)    : " + moves[::-1])
        print("max_opened_states : " + str(g_env.max_opened_states))
        print("Total states      : " + str(g_env.uid))
        print("Time to solve     : " + str(self.time_end - self.time_start))
        exit()


    def find_existing_closed_node(self, node_cmp):
        if (node_cmp.puzzle_hash in self.closed_nodes):
            return self.closed_nodes[node_cmp.puzzle_hash]
        return None


    def add_closed_node(self, node):
        existing_node = self.find_existing_closed_node(node)
        if (existing_node != None and node.f < existing_node.f):
            self.closed_nodes[node.puzzle_hash] = node
        elif (existing_node == None):
            self.closed_nodes[node.puzzle_hash] = node
        return


    def replace_node(self, nodes, node_to_replace, new_node):
        for i, n in enumerate(nodes):
            if n == node_to_replace:
                nodes[i] = new_node
        return


    def create_child_nodes(self, parent, moves):
        nodes = []
        for move in moves:
            new_node = Node(copy.deepcopy(parent.puzzle), parent, move)
            node_already_exists = False
            existing_closed_node = self.find_existing_closed_node(new_node)
            if (existing_closed_node != None):
                node_already_exists = True
                if (new_node.f < existing_closed_node.f):
                    self.closed_nodes[existing_closed_node.puzzle_hash] = new_node
                break
            for opened_node in self.opened_nodes:
                if (new_node.equals(opened_node) == True):
                    node_already_exists = True
                    if (new_node.f < opened_node.f):
                        self.replace_node(self.opened_nodes, opened_node, new_node)
                    break
            if node_already_exists == False:
                nodes.append(new_node)
        return nodes


    def astar(self, initial_puzzle):
        self.opened_nodes.append(Node(copy.deepcopy(initial_puzzle), None, None))
        while (len(self.opened_nodes) > 0):
            op_size = len(self.opened_nodes)
            cl_size = len(self.closed_nodes)
            if (op_size > g_env.max_opened_states):
                g_env.max_opened_states = op_size
            self.opened_nodes.sort(key=lambda x: x.f)
            node = self.opened_nodes.pop(0)
            #node.print_data("first")
            self.add_closed_node(node)
            if node.is_solved() == True:
                return node
            moves = get_possible_moves(node.puzzle, g_env.puzzle_width, node.move)
            add_nodes = self.create_child_nodes(node, moves)
            for add_node in add_nodes:
                self.opened_nodes.append(add_node)
        return None



    def solve(self, initial_puzzle):
        solvable = check_solvability(initial_puzzle, g_env.desired_board, g_env.puzzle_width)
        if (solvable == False):
            print("Input puzzle has no solution")
            exit()

        if (g_env.puzzle_width > 5):
            print("You're getting hungry, expect it to take some time (even with heuristics)")

        self.time_start = time.perf_counter()
        op = self.astar(initial_puzzle)

        if (op != None):
            self.print_solution(op)
        else:
            print("Bad : search returned none (somehow)")
