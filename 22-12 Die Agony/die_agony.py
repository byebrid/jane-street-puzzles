from typing import List
from collections import deque


class InvalidMove(Exception):
    """
    If a particular move cannot be made according to the rules of the game.
    """
    pass

class FaceAlreadySet(Exception):
    """
    If you try to set the same face more than once without clearing it in 
    between.
    """
    pass

class FaceAlreadyCleared(Exception):
    """
    If you try to clear a face that is already cleared.
    """
    pass


class FaceNotSet(Exception):
    """
    If you try to get the value of a face that hasn't been set yet.
    """
    pass


class NoMovesToUndo(Exception):
    """
    If you try to undo a move when there are no moves left to undo.
    """
    pass

class Dice:
    def __init__(self, grid):
        # Order:        Front      Back        Right       Left      Up      Down
        self.faces = list(range(6))
        self.map = {
            i: None for i in range(6)
        }
        self.moves = deque(maxlen=512)
        self.row = 0
        self.col = 0
        self.grid = grid

    def reset(self):
        self.__init__(grid=self.grid)

    def rearrange_faces(self, new_order: List[int]):
        """
        Rearranges the current list of faces according to the new order given by
        a list of indices.

        :param new_order: List of indices.
        """
        faces = [self.faces[i] for i in new_order]
        self.faces = faces

    def roll_forward(self, undoing: bool=False):
        if self.row + 1 >= self.grid_height:
            raise InvalidMove("Can't move forwards out of bounds")
        
        new_order = [5, 4, 2, 3, 0, 1]
        self.rearrange_faces(new_order)
        if not undoing:
            self.moves.append("forward")

        self.row += 1

    def roll_backward(self, undoing: bool=False):
        if self.row - 1 < 0:
            raise InvalidMove("Can't move backwards out of bounds")

        new_order = [4, 5, 2, 3, 1, 0]
        self.rearrange_faces(new_order)
        if not undoing:
            self.moves.append("backward")

        self.row -= 1

    def roll_left(self, undoing: bool=False):
        if self.col - 1 < 0:
            raise InvalidMove("Can't move left out of bounds")

        new_order = [0, 1, 5, 4, 2, 3]
        self.rearrange_faces(new_order)
        if not undoing:
            self.moves.append("left")

        self.col -= 1

    def roll_right(self, undoing: bool=False):
        if self.col + 1 >= self.grid_width:
            raise InvalidMove("Can't move left out of bounds")

        new_order = [0, 1, 4, 5, 3, 2]
        self.rearrange_faces(new_order)
        if not undoing:
            self.moves.append("right")

        self.col += 1

    def face_is_set(self, i: int) -> bool:
        return self.map[i] != None

    def get_face_value(self, i: int):
        if not self.face_is_set(i):
            raise FaceNotSet(f"Face#{i} has not been set!")
        
        return self.map[i]

    def get_top_face(self):
        face_num = self.faces[4]
        return self.get_face_value(face_num)

    def set_top_face(self, val):
        face_num = self.faces[4]
        self.set_face(face_num, val)

    def set_face(self, i: int, val):
        if self.face_is_set(i):
            raise FaceAlreadySet(f"Face#{i} is already set to {self.get_face_value(i)} (tried setting to {val})")

        self.map[i] = val

    def clear_face(self, i: int):
        if self.map[i] is None:
            raise FaceAlreadyCleared(f"Face#{i} is already cleared!")
        
        self.map[i] = None

    def undo_move(self):
        try:
            last_move = self.moves.pop()
        except IndexError:
            raise NoMovesToUndo()

        if last_move == "forward":
            self.roll_backward(undoing=True)
        elif last_move == "backward":
            self.roll_forward(undoing=True)
        elif last_move == "left":
            self.roll_right(undoing=True)
        elif last_move == "right":
            self.roll_left(undoing=True)

    def try_move(self, move):
        if move == "forward":
            move = self.roll_forward
        elif move == "backward":
            move = self.roll_backward
        elif move == "left":
            move = self.roll_left
        elif move == "right":
            move = self.roll_right

        # Get current tile's value
        a = self.grid[self.row][self.col]

        # Try moving to next tile, allow exception to occur if appropriate
        move()
        # If move was fine, get new tile's value
        b = self.grid[self.row][self.col]
        # Then check what face we would need on top afterwards to make this work
        req_face = self.get_required_dice_face(a=a, b=b, n=self.n - 1)
        # See if we can have that face on top now
        try:
            top_face = self.get_top_face()
            if top_face == req_face:
                print(f"Top face is already required face, {top_face}")
            else:
                print(f"Top face is wrong for this move. Currently {top_face} but need {req_face}")
        except FaceNotSet:
            print(f"Could set face to {req_face} to make this work!")

    @property
    def n(self) -> int:
        return len(self.moves) + 1

    @property
    def grid_height(self) -> int:
        return len(self.grid)

    @property
    def grid_width(self) -> int:
        return len(self.grid[0])

    @staticmethod
    def get_required_dice_face(a: int, b: int, n: int) -> int:
        """
        Return the dice face required in order to get from a to b on the n-th move.

        :param a: Tile to move *from*
        :param b: Tile to move *to*
        :param n: This turn's number
        :return: required dice face for this move
        """
        face = (b - a) / n
        if face % 1 != 0:
            raise InvalidMove(f"Move from {a} to {b} on turn#{n} is impossible. No dice face could allow this.")

        return int(face)




# Note grid is "upside-down" to make sure we start from position (0, 0)
# That means "forwards" actually moves down in this grid, and vice versa for "backwards"
# Left and right remain the same though
grid = [
    [0, 77, 32, 403, 337, 452],
    [5, 23, -4, 592, 445, 620],
    [-7, 2, 357, 452, 317, 395],
    [186, 42, 195, 704, 452, 228],
    [81, 123, 240, 443, 353, 508],
    [57, 33, 132, 268, 492, 732]
]
width = len(grid[0])
height = len(grid)
print(f"Grid is {height} rows x {width} cols")

d = Dice(grid=grid)
# faces = ["Front", "Back", "Right", "Left", "Top", "Down"]
# for i, face in enumerate(faces):
#     d.set_face(i, face)



