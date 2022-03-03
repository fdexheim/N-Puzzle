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


def tile_yx_snail(flat_pos, puzzle_size):
    start_x = -1
    start_y = 0;
    end_x = puzzle_size - 1
    end_y = puzzle_size - 1
    x = 0
    y = 0
    ymove = 0
    xmove = 1

    ran = puzzle_size * puzzle_size
    for i in range(0, ran + 1):
        if (i == flat_pos):
            return y, x
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
    return 0, 0


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
