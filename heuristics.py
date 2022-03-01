from tools import tile_yx
from env import g_env


def manhattan_distance(current_puzzle):
    ret = 0
    for y in range(0, g_env.puzzle_width):
        for x in range(0, g_env.puzzle_width):
            y2, x2 = tile_yx(current_puzzle, g_env.desired_board[y][x])
            ret += abs(y - y2) + abs(x - x2)
    return ret


def misplaced_tiles(current_puzzle):
    ret = 0
    for y in range(0, g_env.puzzle_width):
        for x in range(0, g_env.puzzle_width):
            if (current_puzzle[y][x] != g_env.desired_board[y][x]):
                ret += 1
    return ret


def heuristic(puzzle):
    if (g_env.heuristic == "misplaced_tiles"):
        return misplaced_tiles(puzzle)
    elif (g_env.heuristic == "manhattan_distance"):
        return manhattan_distance(puzzle)
    else:
        return 0
