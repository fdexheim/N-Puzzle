from tools import tile_yx_snail, tile_yx


def get_inversion_count(puz):
    inversions = 0
    for i in range(0, len(puz)):
        for j in range(i + 1, len(puz)):
            if (puz[i] != 0 and puz[j] != 0 and puz[i] > puz[j]):
                inversions += 1
    return inversions


def check_solvability(initial_puzzle, desired_board, puzzle_width):
#    return True
    one_d_board = []
    one_d_ref = []
    for i in range(0, puzzle_width * puzzle_width):
        y, x = tile_yx_snail(i, puzzle_width)
        one_d_board.append(initial_puzzle[y][x])
        one_d_ref.append(i + 1)
    one_d_ref[(puzzle_width * puzzle_width) - 1] = 0
    inversions = get_inversion_count(one_d_board)
    inversions_ref = get_inversion_count(one_d_ref)
    y2, x2 = tile_yx(initial_puzzle, 0)
    if (puzzle_width % 2 == 0):
        inversions += one_d_board.index(0)
        inversions_ref += one_d_ref.index(0)
    if (inversions % 2 == inversions_ref % 2):
        return True
    return False
