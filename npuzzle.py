import sys
import os
import array
import math
from tools import tile_yx
from env import g_env
from Solver import Solver

def get_initial_state_from_file(path):
    firstline = 0
    puzzle_size = 0
    parsed_puzzle_lines = 0
    linecout = 0
    totallines = 1;
    ret = []
    with open(path, "r") as f:
        for line in f:
            comment_remover = line.find('#')
            if (comment_remover != -1):
                line = line[:comment_remover]
            if (len(line) == 0):
                continue
            if (firstline == 0):
                try:
                    firstline = 1
                    puzzle_size = int(line)
                    if (puzzle_size < 2):
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
    if parsed_puzzle_lines < puzzle_size :
        print("Bad puzzle format, missing lines")
        return None, 0
    return ret, puzzle_size


def get_desired_board(size):
    ret = [-1] * size
    for i in range(0, size):
        ret[i] = [-1] * size
    start_x = -1
    start_y = 0;
    end_x = size - 1
    end_y = size - 1
    x = 0
    y = 0
    ymove = 0
    xmove = 1

    ran = int(math.pow(size, 2))
    for i in range(1, ran + 1):
        if (i == ran):
            ret[y][x] = 0
            return ret
        else:
            ret[y][x] = i

        if (x == end_x and y == start_y):
            xmove = 0
            ymove = 1
            start_x += 1
        elif (x == end_x and y == end_y):
            xmove = -1
            ymove = 0
            start_y += 1
        elif (x == start_x and y == end_y):
            xmove = 0
            ymove = -1
            end_x -= 1
        elif (x == start_x and y == start_y):
            xmove = 1
            ymove = 0
            end_y -= 1
        y += ymove;
        x += xmove;
    print("Unexpected return encountered in get_desired_board()")
    return ret


def check_initial_state(initial_state, size):
    ran = int(math.pow(size, 2))
    for i in range(0, ran):
        if (tile_yx(initial_state, i) == None):
            return False
    return True


def main(argc, argv):
    if (argc < 2):
        print("usage : python3 npuzzle.py [puzzle file] [heuristic]")
        print("heuristics : mahattan_distance | misplaced_tiles | linear_conflict")
        return
    g_env.argc = argc
    g_env.argv = argv
    initial_state, puzzle_size = get_initial_state_from_file(argv[1])
    if argc >= 3:
        g_env.heuristic = argv[2].lower()
    if (initial_state == None):
        print("Parsing Error")
        exit()
    if (check_initial_state(initial_state, puzzle_size) == False):
        print("Puzzle tile verification failed")
        exit()

    print("initial_board " + str(puzzle_size))
    for j in range(0, puzzle_size):
        print(initial_state[j])

    if (check_initial_state(initial_state, puzzle_size) == False):
        print("Bad initial_state")
        exit()
    g_env.puzzle_width = puzzle_size
    g_env.desired_board = get_desired_board(puzzle_size);
    print("desired_board : ")
    for j in range(0, puzzle_size):
        print(g_env.desired_board[j])
    print("puzzle_width : " + str(g_env.puzzle_width))

    solver = Solver()
    solver.solve(initial_state)

main(len(sys.argv), sys.argv)
