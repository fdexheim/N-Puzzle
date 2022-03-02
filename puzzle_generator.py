import sys
from node import Node
from tools import get_possible_moves, Direction, tile_yx
from run import get_desired_board
import random
from random import randrange

def generate_puzzle(size_str, depth_str):
    size = 0
    depth = 0
    random.seed(None)
    try:
        size = int(size_str)
    except ValueError:
        print("unacceptable value for size : " + size_str)
        return
    try:
        depth = int(depth_str)
    except ValueError:
        print("unacceptable value for depth : " + depth_str)
        return
    if (size < 2):
        print("Size is too low")
        return
    if (depth < 1):
        print("Depth is too low")
        return

    desired_board = get_desired_board(size)
    move = None
    print(size)
    for i in range(0, depth):
        y0, x0 = tile_yx(desired_board, 0)
        if (i == 0):
            moves = get_possible_moves(desired_board, size, None)
        else:
            moves = get_possible_moves(desired_board, size, move)
        index = randrange(0, len(moves))
        move = moves[index]
        desired_board[y0][x0] = desired_board[y0 + move.y][x0 + move.x]
        desired_board[y0 + move.y][x0 + move.x] = 0
    for i in range(0, size):
        for j in range(0, size):
            print(desired_board[i][j], end=" ")
        print("")
    return


def usage():
    print("python puzzle_generator.py [size] [depth]")


if (len(sys.argv) < 2):
    print("missing input size")
    usage()
elif (len(sys.argv) < 3):
    print("missing input depth")
    usage()
else:
    generate_puzzle(sys.argv[1], sys.argv[2])
