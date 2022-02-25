class Puzzle:
    def __init__(self, size, board):
        self.width = size
        self.board = board

    def is_solved(self, ref):
        ntiles = self.width * self.width;
        if str(self.board) == str(ref.board):
            return True
        return False
