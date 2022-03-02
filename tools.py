class Direction:
    def __init__(self, move, y, x):
        self.move = move
        self.y = y
        self.x = x

def tile_yx(state, value):
    for line in state:
        for tile in line:
            if (tile == value):
                return (state.index(line), line.index(tile))
    return None

def tile_value_yx(state, y, x):
    return state[y][x]


def get_possible_moves(puzzle, puzzle_width, prev_move):
    moves = { Direction('u', -1, 0), Direction('d', 1, 0), Direction('l', 0, -1), Direction('r', 0, 1) }
    y, x = tile_yx(puzzle, 0)
    ret = []
    for move in moves:
        cmpy = y + move.y
        cmpx = x + move.x
        # exclude cases where previous move was the opposite
        if (prev_move != None):
            if prev_move.move == 'd' and move.move == 'u':
                continue
            if prev_move.move == 'u' and move.move == 'd':
                continue
            if prev_move.move == 'l' and move.move == 'r':
                continue
            if prev_move.move == 'r' and move.move == 'l':
                continue
        if (cmpx >= 0 and cmpx < puzzle_width and cmpy >= 0 and cmpy < puzzle_width):
            ret.append(move)
    return ret
