from tools import tile_yx
from env import g_env


def col_confs(puz):
    ret = 0
    for i in range(0, g_env.puzzle_width):
        for a in range(0, g_env.puzzle_width - 1):
            tilea = puz[a][i]
            if (tilea == 0):
                continue
            ya, xa = tile_yx(g_env.desired_board, tilea)
            if (xa != i):
                continue
            for b in range(a + 1, g_env.puzzle_width):
                tileb = puz[b][i]
                if (tileb == 0):
                    continue
                yb, xb = tile_yx(g_env.desired_board, tileb)
                if (xb != i):
                    continue
                if yb < ya:
                    ret += 1
    return ret


def line_confs(puz):
    ret = 0
    for i in range(0, g_env.puzzle_width):
        for a in range(0, g_env.puzzle_width - 1):
            tilea = puz[i][a]
            if (tilea == 0):
                continue
            ya, xa = tile_yx(g_env.desired_board, tilea)
            if (ya != i):
                continue
            for b in range(a + 1, g_env.puzzle_width):
                tileb = puz[i][b]
                if (tileb == 0):
                    continue
                yb, xb = tile_yx(g_env.desired_board, tileb)
                if (yb != i):
                    continue
                if xb < xa:
                    ret += 1
    return ret


def linear_conflict(current_puzzle):
    ret = 0
    lc = line_confs(current_puzzle)
    cc = col_confs(current_puzzle)
    man = manhattan_distance(current_puzzle)

    ret = lc + cc
    ret *= 2
    ret += man
    return ret


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
    ret = 0
    if (g_env.use_heuristic_misplaced_tiles == True):
        ret += misplaced_tiles(puzzle)
    if (g_env.use_heuristic_manhattan_distance == True):
        ret += manhattan_distance(puzzle)
    if (g_env.use_heuristic_linear_conflict == True):
        ret += linear_conflict(puzzle)
    return ret
