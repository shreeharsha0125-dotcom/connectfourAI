import numpy as np
from constants import *

class Board:
    def __init__(self):
        # Initialize an empty 6x7 board grid matrix using NumPy
        self.grid = np.zeros((ROWS, COLS), dtype=int)

    def drop_piece(self, row, col, piece):
        """Places a piece token inside the data grid matrix."""
        self.grid[row][col] = piece

    def is_valid_location(self, col):
        """Checks if a column has space for more pieces."""
        return self.grid[ROWS-1][col] == 0

    def get_next_open_row(self, col):
        """Finds the lowest open row in a specific column."""
        for r in range(ROWS):
            if self.grid[r][col] == 0:
                return r
        return None

    def get_valid_locations(self):
        """Returns a list of columns that are not full yet."""
        valid_cols = []
        for col in range(COLS):
            if self.is_valid_location(col):
                valid_cols.append(col)
        return valid_cols

    def check_win(self, piece):
        """Checks the entire matrix to determine if 'piece' has secured 4-in-a-row."""
        # Horizontal lines check
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r][c+i] == piece for i in range(4)):
                    return True

        # Vertical lines check
        for r in range(ROWS - 3):
            for c in range(COLS):
                if all(self.grid[r+i][c] == piece for i in range(4)):
                    return True

        # Positively sloped diagonals (Bottom-Left to Top-Right)
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.grid[r+i][c+i] == piece for i in range(4)):
                    return True

        # Negatively sloped diagonals (Top-Left to Bottom-Right)
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.grid[r-i][c+i] == piece for i in range(4)):
                    return True

        return False

    def is_draw(self):
        """Returns True if the board is completely full with no winner."""
        return len(self.get_valid_locations()) == 0
