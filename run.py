import sys
import os
import array
import math
import hashlib
import re
from tools import tile_yx
from tools import tile_yx_snail
from env import g_env
from Solver import Solver

def get_initial_state_from_file(path):
    firstline = 0
    puzzle_size = 0
    parsed_puzzle_lines = 0
    linecout = 0
    totallines = 1;
    ret = []
    f = 0
    try:
        f = open(path, "r")
        for line in f:
            comment_remover = line.find('#')
            if (comment_remover != -1):
                line = line[:comment_remover]
            line = line.lstrip()
            line = re.sub("\s\s+" , " ", line)
            if (len(line) == 0):
                continue
            if (firstline == 0):
                try:
                    firstline = 1
                    puzzle_size = int(line)
                    if (puzzle_size < 3):
                        print("Bad puzzle_size : " + str(puzzle_size))
                        return None, 0
                except ValueError:
                    print("unacceptable value for size : " + line)
                    return None, 0
            else:
                tokens = line.split(" ")
                parsedline = [0] * puzzle_size
                i = 0
                for token in tokens:
                    try:
                        parsedline[i] = int(token)
                    except ValueError:
                        print("unacceptable value for tile : " + token)
                        return None, 0
                    i += 1
                    if (i >= puzzle_size):
                        break
                if (i + 1 <= puzzle_size):
                    err = "Line " + str(totallines) + " : " "Bad line "
                    print(err)
                    return None, 0
                parsed_puzzle_lines += 1
                ret.append(parsedline)
                if parsed_puzzle_lines == puzzle_size:
                    break;
            totallines += 1
    except FileNotFoundError:
        print("[Error] No file found")
        return None, 0
    if parsed_puzzle_lines < puzzle_size :
        print("[Error] Bad puzzle format, missing lines")
        return None, 0
    return ret, puzzle_size


def get_desired_board(size):
    ret = [-1] * size
    for i in range(0, size):
        ret[i] = [-1] * size

    ran = int(math.pow(size, 2))
    for i in range(0, ran - 1):
        y, x = tile_yx_snail(i, size)
        ret[y][x] = i + 1
    y, x = tile_yx_snail(ran - 1, size)
    ret[y][x] = 0
    return ret


def check_initial_state(initial_state, size):
    ran = int(math.pow(size, 2))
    for i in range(0, ran):
        if (tile_yx(initial_state, i) == None):
            return False
    return True


def parse_heuristic_arg(arg):
    if arg.find('d') != -1:
        g_env.use_heuristic_manhattan_distance = True
    if arg.find('m') != -1:
        g_env.use_heuristic_misplaced_tiles = True
    if arg.find('l') != -1:
        g_env.use_heuristic_linear_conflict = True


def main(argc, argv):
    if (argc < 2):
        print("usage : python3 npuzzle.py [puzzle file] [heuristic]")
        print("heuristics : mahattan_distance | misplaced_tiles | linear_conflict")
        return
    g_env.argc = argc
    g_env.argv = argv
    initial_state, puzzle_size = get_initial_state_from_file(argv[1])
    if (initial_state == None):
        print("Parsing Error")
        exit()
    if (check_initial_state(initial_state, puzzle_size) == False):
        print("Puzzle tile verification failed")
        exit()

    if argc < 3:
        print("[Warning] missing heuristic or wrong heuristic name")
        print("Aviable heuristics : \nflag | heuristic")
        for heuristic in g_env.heuristics:
            print(heuristic)
        print("Continue ? yes / no (input heuristic flag if intend to proceed with one instead)")
        a = input()
        if (a.lower() == "no" or a.lower() == "n"):
            return
        g_env.heuristic_arg = a.lower()
    else:
        g_env.heuristic_arg = argv[2]
    parse_heuristic_arg(g_env.heuristic_arg)


    print("initial_board (size : " + str(puzzle_size) + ") : ")
    for j in range(0, puzzle_size):
        print(initial_state[j])

    if (check_initial_state(initial_state, puzzle_size) == False):
        print("Bad initial_state")
        exit()
    g_env.puzzle_width = puzzle_size
    g_env.desired_board = get_desired_board(puzzle_size);
    g_env.desired_board_hash = hashlib.md5(str(g_env.desired_board).encode('utf-8')).hexdigest()
    print("desired_board : ")
    for j in range(0, puzzle_size):
        print(g_env.desired_board[j])
    print("")

    solver = Solver()
    solver.solve(initial_state)
