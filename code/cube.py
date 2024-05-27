from typing import List

import rotation as rot


class Cube:
    def __init__(self):
        """
        Initializes a Rubik's Cube in a solved state, with the white face facing the user (green face below, red face right, etc.).
        """
        self.face: int = 0
        self.rotation: int = 0
        self.state: List[List[str, int]] = [
            [[[f"{F}{i*3+j}", 0] for j in range(3)] for i in range(3)]
            for F in ["W", "O", "G", "R", "B", "Y"]
        ]
        self.neighbors = [
            [[4, 2], [3, 3], [2, 0], [1, 1]],  # Neighbors of W
            [[0, 3], [2, 0], [5, 1], [4, 0]],  # Neighbors of O
            [[0, 0], [3, 0], [5, 0], [1, 0]],  # Neighbors of G
            [[0, 1], [4, 0], [5, 3], [2, 0]],  # Neighbors of R
            [[0, 2], [1, 0], [5, 2], [3, 0]],  # Neighbors of B
            [[2, 0], [3, 1], [4, 2], [1, 3]],  # Neighbors of Y
        ]

    def get_face(self):
        """Returns the current state of the current face of the cube."""
        return rot.rotate_n(self.state[self.face], self.rotation)

    def __repr__(self):
        """Prints the current state of the current face of the cube for debugging purposes."""
        return "\n".join([str(row) for row in self.get_face()])

    def change_face(self, direction):
        """Changes the current face of the cube to the face in the specified direction."""
        update = self.neighbors[self.face][(direction - self.rotation) % 4]
        self.face, self.rotation = update[0], update[1] + self.rotation % 4

    def rotate_face_clockwise(self, face: int):
        """Rotates the specified face of the cube clockwise by 90 degrees."""
        # Update the arrangement of stickers on the face
        new_face = rot.rotate_n(self.state[face], 1)
        self.state[face] = new_face

        # Update the rotation of the stickers on the face
        for row in self.state[face]:
            for sticker in row:
                sticker[1] = (sticker[1] + 1) % 4

        # Update the arrangement of stickers on the neighboring faces
        neighbors = self.neighbors[face]

        face_rotations, borders, sticker_rotations = [], [], []
        for i, (neighbor, rotation) in enumerate(neighbors):
            face_rotations.append(((i if i % 2 == 1 else 2 - i) + rotation) % 4)
            self.state[neighbor] = rot.rotate_n(
                self.state[neighbor], face_rotations[-1]
            )
            borders.append([x for x in self.state[neighbor][0]])
            sticker_rotations.append(
                self.neighbors[neighbor][(i + 1 - rotation) % 4][1]
            )

        for i in range(4):
            neighbor = neighbors[i][0]
            for j in range(3):
                # Update the rotation of the stickers on the neighboring faces using sticker_rotations
                replacement = [
                    borders[(i - 1) % 4][j][0],
                    (borders[(i - 1) % 4][j][1] - sticker_rotations[(i - 1) % 4]) % 4,
                ]
                self.state[neighbor][0][j] = replacement
            self.state[neighbor] = rot.rotate_n(
                self.state[neighbor], (4 - face_rotations[i]) % 4
            )

    def rotate_adjacent_face(self, direction: int):
        """Rotates clockwise the face adjacent to the current face in the specified direction."""
        self.rotate_face_clockwise(self.neighbors[self.face][direction][0])


if __name__ == "__main__":
    # Initialize a solved Rubik's Cube
    c = Cube()
    print(c)

    # Rotate the right face of the cube clockwise 4 times (returning to solved),
    # printing the state of the cube at each point in the process
    for _ in range(4):
        c.rotate_face_clockwise(3)
        print()
        print(c)
