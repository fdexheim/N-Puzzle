def tile_yx(state, value):
    for line in state:
        for tile in line:
            if (tile == value):
                return (state.index(line), line.index(tile))
    return None

def tile_value_yx(state, y, x):
    return state[y][x]
