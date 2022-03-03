class g_env:
    argc = 0
    argv = 0
    uid = 1
    puzzle_width = 0
    desired_board = None
    desired_board_hash = ""
    time_start = 0
    time_end = 0
    max_opened_states = 0
    heuristics = { "   d | manhattan_distance", "   m | misplaced_tiles", "   l | linear_conflict" }
    heuristic_arg = ""
    use_heuristic_manhattan_distance = False
    use_heuristic_misplaced_tiles = False
    use_heuristic_linear_conflict = False
