from string import ascii_lowercase
import typing
import itertools
import time
import random

import numpy as np


# Some common type aliases
Grid = np.ndarray[float]
Time = int
Position = [int, int]
KnightState = tuple[Time, Position]

search_count = 0
roadblock_count = 0
leniency_factor = 20


def get_opposite_position(grid: Grid, position: Position) -> Position:
    height, width = grid.shape
    row, col = position
    opp_row = height - row - 1
    opp_col = width - col - 1
    return opp_row, opp_col


def update_grid(grid: Grid, position: Position) -> Grid:
    # Get indices of cells with same altitude
    row, col = position
    altitude = grid[row, col]
    indices = np.transpose((grid == altitude).nonzero())

    # This discards diametrically opposite cell since it shouldn't count
    opposite_position = get_opposite_position(grid, position)
    opposite_match = np.all(indices == opposite_position, axis=1)
    opposite_was_same_alt = np.count_nonzero(opposite_match) > 0
    indices = indices[~opposite_match]
    n = len(indices)

    # Rise all cells with same altitude
    rate = 1 / n
    rows, cols = indices.transpose()
    updated_grid = grid.copy()
    updated_grid[rows, cols] -= rate

    # Sink diametrically opposite cell if it wasn't same altitude
    if not opposite_was_same_alt:
        opp_row, opp_col = opposite_position
        updated_grid[opp_row, opp_col] += rate

    return updated_grid

def search_for_action(action: KnightState, path: list[KnightState]) -> bool:
    """Return True if given action is already in path, False otherwise.
    
    Note we know that our path is sorted in ascending time order, so we only need
    to search backwards until the time time drops below that of the given action.
    """
    search_time = action[0]
    for prev_state in reversed(path):
        if prev_state == action:
            return True
        
        prev_time = prev_state[0]
        if prev_time < search_time:
            return False

    # Don't think this should ever reach here, but if it does answer is definitely False!
    return False

def get_valid_actions(grid: Grid, path: list[KnightState]) -> list[KnightState]:
    """Return list of valid (t, P) states following from the current knight state."""
    time, (row, col) = path[-1]
    altitude = grid[row, col]
    height, width = grid.shape

    valid_actions = []
    valid_combos = [(0, 1, 2), (0, 1, -2), (0, -1, 2), (0, -1, -2)]
    any_valid_sleeps = False
    for combo in valid_combos:
        for perm in itertools.permutations(combo):
            row_diff, col_diff, alt_diff = perm
            new_row = row + row_diff
            new_col = col + col_diff
            new_alt = altitude + alt_diff
            if new_row < 0 or new_row >= height or new_col < 0 or new_col >= width:
                continue
            if grid[new_row, new_col] == new_alt:
                # Double-check that this state is not already in our path, 
                # otherwise get infinte loop!
                new_action = (time, (new_row, new_col))
                if not search_for_action(action=new_action, path=path):
                    valid_actions.append((time, (new_row, new_col)))
                else:
                    # print(f"Action {new_action} was already in path!")
                    pass
            elif grid[new_row, new_col] < new_alt:
                # If target position has same altitude as current position, then 
                # sleeping will *not* allow a valid jump in the future.
                # The exception to this is if the target position also happens
                # to be the diametrically opposite position, in which case the
                # current position can sink below the target and *maybe* allow
                # a valid jump in the future
                is_opposite = (new_row, new_col) == get_opposite_position(grid, (row, col))
                matching_altitude = grid[new_row, new_col] == altitude
                if not matching_altitude or is_opposite:
                    # print(f"Valid sleep from ({new_row}, {new_col}); {new_alt}")
                    any_valid_sleeps = True
                
    # Only include sleep as a valid action if *no* valid jumps are available
    if len(valid_actions) == 0 and any_valid_sleeps:
        valid_actions.append((time+1, (row, col)))

    return valid_actions


def check_if_reachable(grid: Grid, target_pos: Position) -> bool:
    """Return True if target position seems reachable now or in the future."""
    row, col = target_pos
    altitude = grid[row, col]
    height, width = grid.shape
    
    valid_combos = [(0, 1, 2), (0, 1, -2), (0, -1, 2), (0, -1, -2)]
    for combo in valid_combos:
        for perm in itertools.permutations(combo):
            row_diff, col_diff, alt_diff = perm
            new_row = row + row_diff
            new_col = col + col_diff
            if new_row < 0 or new_row >= height or new_col < 0 or new_col >= width:
                continue
            
            new_alt = altitude + alt_diff
            actual_diff = altitude - grid[new_row, new_col]
            if actual_diff < leniency_factor * alt_diff:
                return True
            
    return False


def search(grid: Grid, path: list[KnightState], target_time: int, target_pos: Position) -> bool:
    global search_count, roadblock_count
    search_count += 1
    if search_count % 1000 == 0:
        print(f"Searched {search_count} paths. Found {roadblock_count} roadblocks")
    if search_count % 1e5 == 0:
        print(grid)
        print(f"Path length = {len(path)}")
        print(path)

    t, position = path[-1]
    if position == target_pos and t >= target_time:
        print("!!!!!!!!!!!!!!!!!!!! YOU WON !!!!!!!!!!!!!!!!!!!!")
        print(path)
        return True
    
    if not check_if_reachable(grid=grid, target_pos=target_pos):
        print("Can't seem to reach target position!")
        print(path)
        print(grid)
        roadblock_count += 1
        return False

    valid_actions = get_valid_actions(grid=grid, path=path)
    if len(valid_actions) == 0:
        # print("Reached roadblock!")
        roadblock_count += 1
        return False
    
    for action in valid_actions:
        action_time = action[0]
        # print(f"{action_time=}")
        if action_time > t:
            new_grid = update_grid(grid=grid, position=position)
            search_result = search(grid=new_grid, path=path + [action], target_time=target_time, target_pos=target_pos)
        else:
            search_result = search(grid=grid, path=path + [action], target_time=target_time, target_pos=target_pos)

        if search_result is True:
            return True

    return False



def main():
    grid = np.array([
        [11, 10, 11, 14],
        [8, 6, 9, 9],
        [10, 4, 3, 1],
        [5, 6, 5, 0]
    ], dtype=np.float64)
    # Target is top-right corner
    target_pos = (0, grid.shape[1] - 1)
    target_time = 10
    path = [(0, (3, 0))]

    search(grid=grid, path=path, target_time=target_time, target_pos=target_pos)


if __name__ == "__main__":
    main()