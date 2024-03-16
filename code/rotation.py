from typing import Any, List


def rotate(grid: List[List[Any]]) -> List[List[Any]]:
    """Rotate a 2D grid 90 degrees clockwise."""
    return [
        [grid[j][i] for j in range(len(grid) - 1, -1, -1)] for i in range(len(grid[0]))
    ]


def rotate_n(grid: List[List[Any]], n: int) -> List[List[Any]]:
    """Rotate a 2D grid clockwise n times."""
    output = grid
    for _ in range(n):
        output = rotate(output)
    return output


if __name__ == "__main__":
    g1 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    for row in rotate(g1):
        print(row)

    print()

    g2 = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
    for row in rotate_n(g2, 2):
        print(row)
