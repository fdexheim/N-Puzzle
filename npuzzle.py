import sys
import os
import array
from tools import tile_yx
import math


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
'''
def get_desired_board(size):
    size = 4
    ret = [-1] * size
    for i in range(0, size):
        ret[i] = [-1] * size
    print(ret)
    start_x = 0
    start_y = 0;
    end_x = size - 1
    end_y = size - 1
    x = 0
    y = 0
    ymove = 0
    xmove = 1

    ran = int(math.pow(size, 2))
    for i in range(1, ran + 1):
        print("ret[{0}][{1}] = {2}    Xranges{3}-{4} Yranges{5}-{6}".format(y, x, i, start_x, end_x, start_y, end_y))

        if (i == ran):
            ret[y][x] = 0
            for j in range(0, size):
                print(ret[j])
            return
        else:
            ret[y][x] = i

        if (x == end_x and y == start_y):
            print("First Corner")
            xmove = 0
            ymove = 1
        elif (x == end_x and y == end_y):
            print("Second Corner")
            xmove = -1
            ymove = 0
            start_y += 1
        elif (x == start_x and y == end_y):
            print("Third Corner")
            xmove = 0
            ymove = -1
            end_x -= 1
        elif (x == start_x and y - 1 == start_y):
            print("Fourth Corner")
            xmove = 1
            ymove = 0
            end_y -= 1
            start_x += 1
        y += ymove;
        x += xmove;
    print("Wrong return")
    print(ret)
    return 0
'''

def check_initial_state(initial_state, size):
    ran = int(math.pow(size, 2))
    for i in range(0, ran):
        if (tile_yx(i, initial_state, size) == None):
            return False
    return True

def main(argc, argv):
    if (argc < 2):
        print("Bad arg")
        return

    initial_state, puzzle_size = get_initial_state_from_file(argv[1])
    if (initial_state == None):
        print("Parsing Error")
        exit()
    if (check_initial_state(initial_state, puzzle_size) == False):
        print("Puzzle tile verification failed")
        exit()

    print("puzzle_size ('" + str(type(puzzle_size)) + "') = " + str(puzzle_size))
    print(str(type(initial_state)))
    print(initial_state)

    if (check_initial_state == False):
        print("Bad initial_state")
        exit()
    desired_state = get_desired_state(puzzle_size);


main(len(sys.argv), sys.argv)
