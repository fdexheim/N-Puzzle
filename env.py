class g_env:
    argc = 0
    argv = 0
    uid = 1
    puzzle_width = 0
    desired_board = None
    time_start = 0
    time_end = 0
    max_opened_states = 0
    heuristics = { "manhattan_distance", "misplaced_tiles" }
    heuristic = ""
