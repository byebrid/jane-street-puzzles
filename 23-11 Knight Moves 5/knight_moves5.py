from string import ascii_lowercase
import itertools
import time
import random

import numpy as np


class Board:
    def __init__(self, grid: np.ndarray[float]) -> None:
        self.grid = np.array(grid, dtype=np.float64)

    def update(self, row: int, col: int):
        # Get indices of cells with same altitude
        altitude = self.grid[row, col]
        indices = np.transpose((self.grid == altitude).nonzero())

        # This discards diametrically opposite cell since it shouldn't count
        opp_row, opp_col = self.opposite_rowcol(row, col)
        opposite_match = np.all(indices == (opp_row, opp_col), axis=1)
        opposite_was_same_alt = np.count_nonzero(opposite_match) > 0
        indices = indices[~opposite_match]
        n = len(indices)

        # Rise all cells with same altitude
        rate = 1 / n
        rows, cols = indices.transpose()
        self.grid[rows, cols] -= rate

        # Sink diametrically opposite cell if it wasn't same altitude
        if not opposite_was_same_alt:
            self.grid[opp_row, opp_col] += rate

    def valid_jumps(self, row: int, col: int) -> list[tuple[int, int]]:
        """Return list of (row, col) corresponding to valid jumps."""
        altitude = self.grid[row, col]
        height, width = self.grid.shape

        valid_jumps = []
        valid_combos = [(0, 1, 2), (0, 1, -2), (0, -1, 2), (0, -1, -2)]
        for combo in valid_combos:
            for perm in itertools.permutations(combo):
                row_diff, col_diff, alt_diff = perm
                new_row = row + row_diff
                new_col = col + col_diff
                new_alt = altitude + alt_diff
                if new_row < 0 or new_row >= height or new_col < 0 or new_col >= width:
                    continue
                if self.grid[new_row, new_col] == new_alt:
                    valid_jumps.append((new_row, new_col))

        return valid_jumps

    def opposite_rowcol(self, row: int, col: int) -> tuple[int, int]:
        height, width = self.grid.shape
        opp_row = height - row - 1
        opp_col = width - col - 1
        return opp_row, opp_col
    
    def xy_to_a1(self, row: int, col: int) -> str:
        """Convert zero-indexed (row, col) to one-indexed alphanumeric like 'b5'"""
        height, width = self.grid.shape
        row_name = height - row
        letter = ascii_lowercase[col]
        return f"{letter}{row_name}"

    def __str__(self) -> str:
        return str(self.grid)
    
    def __repr__(self) -> str:
        return str(self)


def main():
    while True:
        board = Board(np.array([
            [11, 10, 11, 14],
            [8, 6, 9, 9],
            [10, 4, 3, 1],
            [7, 6, 5, 0]
            ]))
        
        row, col = 3, 0
        t = 0
        iters = 0
        max_iters = 400
        rest_chance = 0.5
        
        while True:
            print(f"{t}, {board.xy_to_a1(row, col)}")
            print(board)
            valid_jumps = board.valid_jumps(row=row, col=col)
            if len(valid_jumps) == 0:
                print("Got stuck!")
                break
            if random.random() < rest_chance:
                board.update(row=row, col=col)
                t += 1
            else:
                row, col = random.choice(valid_jumps)
                print(valid_jumps)
            
            iters += 1
            if iters >= max_iters:
                print("Stopping early...")
                break

            if row == 0 and col == 3:
                print("Hit end?")
                if t > 180:
                    print("WE WON!!!!!!!!!!!!!!!!")
                    return

if __name__ == "__main__":
    main()