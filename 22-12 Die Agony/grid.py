from __future__ import annotations
from typing import List
import numpy as np
 

FRONT = 0
BACK = 1
RIGHT = 2
LEFT = 3
UP = 4
DOWN = 5 

grid = np.array([
    [57, 33, 132, 268, 492, 732],
    [81, 123, 240, 443, 353, 508],
    [186, 42, 195, 704, 452, 228],
    [-7, 2, 357, 452, 317, 395],
    [5, 23, -4, 592, 445, 620],
    [0, 77, 32, 403, 337, 452],
])
height, width = grid.shape


def get_top_face(dice):
    return dice[UP]

def set_top_face(dice, val):
    dice[UP] = val

def roll_dice(dice, dir: str):
    if dir == "f":
        order = [DOWN, UP, RIGHT, LEFT, FRONT, BACK]
    elif dir == "b":
        order = [UP, DOWN, RIGHT, LEFT, BACK, FRONT]
    elif dir == "l":
        order = [FRONT, BACK, DOWN, UP, RIGHT, LEFT]
    elif dir == "r":
        order = [FRONT, BACK, UP, DOWN, LEFT, RIGHT]
    
    return [dice[i] for i in order]

def get_top_face_after_move(dice, dir: str):
    dice_after_move = roll_dice(dice, dir)
    top_face_after_move = get_top_face(dice_after_move)
    return top_face_after_move

def get_required_dice_face(a: int, b: int, n: int) -> int:
    """
    Return the dice face required in order to get from a to b on the n-th move.

    :param a: Tile to move *from*
    :param b: Tile to move *to*
    :param n: This turn's number
    :return: required dice face for this move
    """
    face = (b - a) / n
    
    # Everything was integers in the end, but I guess it didn't have to be so!
    # if face % 1 != 0: 
    #     return None
        # raise InvalidMove(f"Move from {a} to {b} on turn#{n} is impossible. No dice face could allow this.")

    return face



class Tile:
    def __init__(self, val: int):
        self.val = val
        self.row = None
        self.col = None

        self.forward = None
        self.backward = None
        self.right = None
        self.left = None

        self.end = False

    def can_move_to(self, other: Tile, path, dice):
        if other is None:
            return False, None
        
        # This was actually not the right way of doing it. Nothing wrong with
        # going back over path so long as dice is not in exact same state as it
        # was the last time it was here!
        # if other in path:
        #     print(f"{self.val} -> {other.val}; Already in path!")
        #     return False, None

        n = len(path)
        req_face = get_required_dice_face(self.val, other.val, n)
        # Means no dice face could give us this (assuming integers only?)
        if req_face is None:
            return False, None

        # Figure out direction of this other tile
        if other == self.forward:
            direction = "f"
        elif other == self.backward:
            direction = "b"
        elif other == self.left:
            direction = "l"
        elif other == self.right:
            direction = "r"
        else:
            # Shouldn't get here, this means other is not even adjacent to this Tile!
            raise ValueError("Should only attempt moving to orthogonally adjacent tiles!")

        new_dice = roll_dice(dice, direction)
        top_face_after_move = get_top_face(new_dice)
        if top_face_after_move is None:
            set_top_face(new_dice, req_face)
        if get_top_face(new_dice) == req_face:
            return True, new_dice

        # Otherwise dice had wrong face for this move
        return False, None


    def __str__(self) -> str:
        f = str(self.forward.val if self.forward else None)
        b = str(self.backward.val if self.backward else None)
        r = str(self.right.val if self.right else None)
        l = str(self.left.val if self.left else None)
        v = str(self.val if self.val else None)

        s = (
            f"{f:^22}\n"
            f"{'+-------+':^22}\n"
            f"{l:^6}|{v:^7}|{r:^6}\n"
            f"{'+-------+':^22}\n"
            f"{b:^22}"
        )

        return s
    
    def __repr__(self) -> str:
        return f"Tile({self.val:3d})"

# Initialise *graph* of Tiles from grid array
tiles = np.vectorize(Tile)(grid)
for row_num, row in enumerate(tiles):
    for col_num, tile in enumerate(row):
        # Just for easier printing once we've got result
        tile.row = row_num
        tile.col = col_num

        # Ensure tiles only connect where appropriate
        if row_num - 1 >= 0:
            tile.forward = tiles[row_num - 1, col_num]
        if row_num + 1 < height:
            tile.backward = tiles[row_num + 1, col_num]
        if col_num - 1 >= 0:
            tile.left = tiles[row_num, col_num - 1]
        if col_num + 1 < width:
            tile.right = tiles[row_num, col_num + 1]

# Mark exit tile as the end (i.e. the 732 in top-right corner)
(tiles[0, width-1]).end = True

def search(path: List[Tile], dice: List, answer):
    tile = path[-1]
    if tile.end:
        print("##################################################################")
        answer["path"] = path
        answer["dice"] = dice
        return True

    # Cycle through all options from this tile and die, but in a depth-first way
    for other in (tile.forward, tile.right, tile.backward, tile.left):
        can, new_dice = tile.can_move_to(other, path, dice)
        
        if can:
            new_path = path + [other]
            success = search(new_path, new_dice, answer)
            if success:
                return True

    return False

if __name__ == "__main__":
    path = [tiles[5, 0]]
    dice = [None for _ in range(6)]
    answer = {"path": None, "dice": None}
    search(path, dice, answer)
    print(answer["path"])
    print(answer["dice"])

    total = 0
    num = 0
    for tile in tiles.flatten():
        if tile not in answer["path"]:
            total += tile.val
            num += 1

    print(f"Path was {len(answer['path']) - 1} moves long")
    print(f"Sum of {num} tiles *not* in path = {total}")
    print(" -> ".join([f"{t.val:>5}@({t.row}, {t.col})" for t in answer["path"]]))


# dice[FRONT] = 1
# dice[BACK] = 6
# dice[UP] = 2
# dice[DOWN] = 5
# dice[LEFT] = 4
# dice[RIGHT] = 3
# print(dice)

# dice = roll_dice(dice, "l")
# dice = roll_dice(dice, "r")

# dice = roll_dice(dice, "f")
# dice = roll_dice(dice, "b")

# dice = roll_dice(dice, "r")
# dice = roll_dice(dice, "f")
# dice = roll_dice(dice, "l")
# dice = roll_dice(dice, "b")

# dice = roll_dice(dice, "f")
# dice = roll_dice(dice, "r")
# dice = roll_dice(dice, "b")
# dice = roll_dice(dice, "l")
# print(dice)
