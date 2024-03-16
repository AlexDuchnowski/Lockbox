import asyncio
import time
from random import randint
from typing import List, Optional, Tuple

import cube
import pygame
import rotation as rot
import stickers


def vary_color(color: Tuple[int]) -> List[int]:
    if color == (25, 25, 25):
        return color
    shift = randint(-10, 10)
    x = [c + shift for c in color]
    return [abs(c) if c < 0 else (255 if c > 255 else c) for c in x]


def form_maze(c: cube.Cube) -> List[List[str]]:
    cube_face = c.get_face()
    return [
        [
            rot.rotate_n(
                stickers.stickers[cube_face[row // 7][col // 7][0]],
                (c.rotation + cube_face[row // 7][col // 7][1]) % 4,
            )[row % 7][col % 7]
            for col in range(21)
        ]
        for row in range(21)
    ]


def render(
    screen: pygame.Surface,
    CELL_SIZE: int,
    maze: List[List[str]],
    x: Optional[int] = None,
    y: Optional[int] = None,
):
    if x is not None and y is not None:
        pygame.draw.rect(
            screen,
            vary_color(stickers.colors[maze[y][x]]),
            ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )
    else:
        for i in range(21):
            for j in range(21):
                pygame.draw.rect(
                    screen,
                    vary_color(stickers.colors[maze[i][j]]),
                    ((j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )


def draw_player(screen: pygame.Surface, PLAYER_X: int, PLAYER_Y: int, CELL_SIZE: int):
    pygame.draw.rect(
        screen,
        (60, 60, 60),
        ((PLAYER_X + 1) * CELL_SIZE, (PLAYER_Y + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE),
    )
    pygame.draw.rect(
        screen,
        (255, 20, 147),
        (
            (PLAYER_X + 1) * CELL_SIZE + (CELL_SIZE // 4),
            (PLAYER_Y + 1) * CELL_SIZE + (CELL_SIZE // 4),
            CELL_SIZE // 2,
            CELL_SIZE // 2,
        ),
    )


pygame.init()


async def main():
    # def main():
    CELL_SIZE = 24

    SCREEN_WIDTH = 23 * CELL_SIZE
    SCREEN_HEIGHT = 23 * CELL_SIZE

    PLAYER_X = 10
    PLAYER_Y = 10

    delay = 0.08

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    print("Game Starting")

    c = cube.Cube()
    # await micropip.install("pygame")
    maze = form_maze(c)
    screen.fill((0, 0, 0))
    render(screen, CELL_SIZE, maze)

    print("Game Starting")
    run = True
    while run:
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if PLAYER_X == 0:
                        c.change_face(3)
                        maze = form_maze(c)
                        render(screen, CELL_SIZE, maze)
                        PLAYER_X = 20
                    elif maze[PLAYER_Y][PLAYER_X - 1] != "X":
                        render(screen, CELL_SIZE, maze, PLAYER_X, PLAYER_Y)
                        PLAYER_X -= 1
                elif event.key == pygame.K_RIGHT:
                    if PLAYER_X == 20:
                        c.change_face(1)
                        maze = form_maze(c)
                        render(screen, CELL_SIZE, maze)
                        PLAYER_X = 0
                    elif maze[PLAYER_Y][PLAYER_X + 1] != "X":
                        render(screen, CELL_SIZE, maze, PLAYER_X, PLAYER_Y)
                        PLAYER_X += 1
                elif event.key == pygame.K_UP:
                    if PLAYER_Y == 0:
                        c.change_face(0)
                        maze = form_maze(c)
                        render(screen, CELL_SIZE, maze)
                        PLAYER_Y = 20
                    elif maze[PLAYER_Y - 1][PLAYER_X] != "X":
                        render(screen, CELL_SIZE, maze, PLAYER_X, PLAYER_Y)
                        PLAYER_Y -= 1
                elif event.key == pygame.K_DOWN:
                    if PLAYER_Y == 20:
                        c.change_face(2)
                        maze = form_maze(c)
                        render(screen, CELL_SIZE, maze)
                        PLAYER_Y = 0
                    elif maze[PLAYER_Y + 1][PLAYER_X] != "X":
                        render(screen, CELL_SIZE, maze, PLAYER_X, PLAYER_Y)
                        PLAYER_Y += 1
                elif event.key == pygame.K_u:
                    c.rotate_face_clockwise(0)
                    maze = form_maze(c)
                    render(screen, CELL_SIZE, maze)
                elif event.key == pygame.K_l:
                    c.rotate_face_clockwise(1)
                    maze = form_maze(c)
                    render(screen, CELL_SIZE, maze)
                elif event.key == pygame.K_f:
                    c.rotate_face_clockwise(2)
                    maze = form_maze(c)
                    render(screen, CELL_SIZE, maze)
                elif event.key == pygame.K_r:
                    c.rotate_face_clockwise(3)
                    maze = form_maze(c)
                    render(screen, CELL_SIZE, maze)
                elif event.key == pygame.K_b:
                    c.rotate_face_clockwise(4)
                    maze = form_maze(c)
                    render(screen, CELL_SIZE, maze)
                elif event.key == pygame.K_d:
                    c.rotate_face_clockwise(5)
                    maze = form_maze(c)
                    render(screen, CELL_SIZE, maze)

        draw_player(screen, PLAYER_X, PLAYER_Y, CELL_SIZE)

        pygame.display.update()
        time.sleep(delay)
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())


# if __name__ == "__main__":
# main()
