from typing import List

import rotation as rot


class Cube:
    def __init__(self):
        self.face = 0
        self.rotation = 0
        self.state = [
            [[f"{F}{i*3+j}" for j in range(3)] for i in range(3)]
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

    def __repr__(self):
        return "\n".join(
            [
                " ".join(row)
                for row in rot.rotate_n(self.state[self.face], self.rotation)
            ]
        )

    def change_face(self, direction):
        update = self.neighbors[self.face][(direction - self.rotation) % 4]
        self.face, self.rotation = update[0], update[1] + self.rotation % 4

    def rotate_face(self, face: int, rotation: int):
        # TODO: Implement this method
        pass

    def get_face(self):
        return rot.rotate_n(self.state[self.face], self.rotation)


if __name__ == "__main__":
    c = Cube()
    print(c)
    for _ in range(4):
        print()
        c.change_face(3)
        print(c)
