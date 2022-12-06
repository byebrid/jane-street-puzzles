import unittest
from die_agony import grid, Dice, InvalidMove, FaceAlreadySet, FaceAlreadyCleared, FaceNotSet, NoMovesToUndo


class TestDieAgony(unittest.TestCase):
    def test_get_dice_face(self):
        self.assertEqual(Dice.get_required_dice_face(0, 5, 1), 5)
        self.assertEqual(Dice.get_required_dice_face(5, -7, 2), -6)
        self.assertEqual(Dice.get_required_dice_face(508, 732, 14), 16)

        with self.assertRaises(InvalidMove):
            Dice.get_required_dice_face(0, 5, 2)
        with self.assertRaises(InvalidMove):
            Dice.get_required_dice_face(0, 5, 4)

        self.assertEqual(Dice.get_required_dice_face(0, 5, 5), 1)

    def test_roll_dice(self):
        # Roll forwards
        d = Dice(grid=grid)
        d.roll_forward()
        self.assertEqual(d.faces, [5, 4, 2, 3, 0, 1])

        # Roll backwards
        d = Dice(grid=grid)
        d.roll_backward()
        self.assertEqual(d.faces, [4, 5, 2, 3, 1, 0])

        # Roll left
        d = Dice(grid=grid)
        d.roll_left()
        self.assertEqual(d.faces, [0, 1, 5, 4, 2, 3])

        # Roll right
        d = Dice(grid=grid)
        d.roll_right()
        self.assertEqual(d.faces, [0, 1, 4, 5, 3, 2])

        # Roll forwards, then backwards, and also left then right
        d = Dice(grid=grid)
        d.roll_forward()
        d.roll_backward()
        self.assertEqual(d.faces, [0, 1, 2, 3, 4, 5])
        d.roll_left()
        d.roll_right()
        self.assertEqual(d.faces, [0, 1, 2, 3, 4, 5])

        # Verify that rolling two directions in different order gives different result
        d = Dice(grid=grid)
        d.roll_forward()
        d.roll_right()
        faces1 = d.faces
        d = Dice(grid=grid)
        d.roll_right()
        d.roll_forward()
        faces2 = d.faces
        self.assertNotEqual(faces1, faces2)

    def test_faces(self):
        d = Dice(grid=grid)
        # Verify all faces are unset by default
        for i in range(6):
            with self.subTest(i=i):
                self.assertFalse(d.face_is_set(i))

        # Change a face
        d.set_face(4, "Up")
        self.assertEqual(d.get_face_value(4), "Up")
        self.assertTrue(d.face_is_set(4))
        # Try changing same face without clearing
        with self.assertRaises(FaceAlreadySet):
            d.set_face(4, "Down")
        # Now clear first, then change that same face
        d.clear_face(4)
        self.assertFalse(d.face_is_set(4))
        d.set_face(4, "Down")
        self.assertEqual(d.get_face_value(4), "Down")
        self.assertTrue(d.face_is_set(4))

        # Finally, set all faces, then reset and check all faces unset
        d = Dice(grid=grid)
        for i in range(6):
            d.set_face(i, f"Face{i}")
            self.assertEqual(d.get_face_value(i), f"Face{i}")
            self.assertTrue(d.face_is_set(i))
        d.reset()
        for i in range(6):
            self.assertFalse(d.face_is_set(i))
        
    def test_clear_face(self):
        d = Dice(grid=grid)
        # Set every face
        for i in range(6):
            d.set_face(i, i)
            self.assertTrue(d.face_is_set(i))

        # Clear every face manually
        for i in range(6):
            d.clear_face(i)
            self.assertFalse(d.face_is_set(i))

        # Try clearing face that is already clear
        with self.assertRaises(FaceAlreadyCleared):
            d.clear_face(0)

    def test_get_cleared_face(self):
        d = Dice(grid=grid)
        for i in range(6):
            with self.subTest(i=i), self.assertRaises(FaceNotSet):
                d.get_face_value(i)


    def test_undo_move(self):
        d = Dice(grid=grid)
        # Just give sensible names for faces
        faces = ["Front", "Back", "Right", "Left", "Top", "Down"]
        for i, face in enumerate(faces):
            d.set_face(i, face)

        # Roll forward, then try undoing
        d.roll_forward()
        d.undo_move()
        for i, face in enumerate(faces):
            self.assertEqual(d.get_face_value(i), face)
        # Try undoing again, expect error
        with self.assertRaises(NoMovesToUndo):
            d.undo_move()

        # Try doing multiple moves, then undoing all of them
        d.roll_forward()
        d.roll_forward()
        d.roll_left()
        d.roll_backward()
        d.roll_right()
        while True:
            try:
                d.undo_move()
            except NoMovesToUndo:
                break
        # Make sure we're back to original faces
        for i, face in enumerate(faces):
            self.assertEqual(d.get_face_value(i), face)





if __name__ == "__main__":
    unittest.main()

