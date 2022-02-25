class Node:
    def __init__(self, puzzle, parent=None, action=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        self.g = 0
        if (self.parent != None):
            self.g = parent.g + 1

    @property
    def h(self):
        return 0

    @property
    def f(self):
        return self.h + self.g
