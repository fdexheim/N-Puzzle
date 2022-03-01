def get_inversion_count(puz):
    inversions = 0
    for i in range(0, len(puz)):
        for j in range(i + 1, len(puz)):
            if (puz[i] != 0 and puz[j] != 0 and puz[i] > puz[j]):
                inversions += 1
    return inversions


def check_solvability(initial_puzzle, desired_board, puzzle_width):
    one_d_board = []
    one_d_ref = []
    for i in range(0, puzzle_width):
        for j in range(0, puzzle_width):
            one_d_board.append(initial_puzzle[i][j])
            one_d_ref.append(desired_board[i][j])
    inversion_board = get_inversion_count(one_d_board)
    inversion_ref = get_inversion_count(one_d_ref)
    if (puzzle_width % 2 == 0):
        inversion_board += one_d_board.index(0)
        inversion_ref += one_d_ref.index(0)
    if (inversion_board % 2 == inversion_ref % 2):
        return True
    return False
