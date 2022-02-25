def tile_yx(tile_value, state, state_size):
    for line in state:
        for tile in line:
            if (tile == tile_value):
                return (state.index(line), line.index(tile))
    return None
