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
    maze: List[List[str]],
    CELL_SIZE: int,
    BORDER: int,
    x: Optional[int] = None,
    y: Optional[int] = None,
):
    if x is not None and y is not None:
        pygame.draw.rect(
            screen,
            vary_color(stickers.colors[maze[y][x]]),
            ((x + BORDER) * CELL_SIZE, (y + BORDER) * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )
    else:
        for i in range(21):
            for j in range(21):
                pygame.draw.rect(
                    screen,
                    vary_color(stickers.colors[maze[i][j]]),
                    (
                        (j + BORDER) * CELL_SIZE,
                        (i + BORDER) * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                    ),
                )


def draw_player(
    screen: pygame.Surface, PLAYER_X: int, PLAYER_Y: int, CELL_SIZE: int, BORDER: int
):
    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (
            (PLAYER_X + BORDER) * CELL_SIZE,
            (PLAYER_Y + BORDER) * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        ),
    )
    pygame.draw.rect(
        screen,
        (255, 20, 147),
        (
            (PLAYER_X + BORDER) * CELL_SIZE + (CELL_SIZE // 4),
            (PLAYER_Y + BORDER) * CELL_SIZE + (CELL_SIZE // 4),
            CELL_SIZE // 2,
            CELL_SIZE // 2,
        ),
    )


pygame.init()
pygame.font.init()


async def main():
    # def main():
    CELL_SIZE = 32

    BORDER = 0

    SCREEN_WIDTH = (21 + 2 * BORDER) * CELL_SIZE
    SCREEN_HEIGHT = (21 + 2 * BORDER) * CELL_SIZE

    PLAYER_X = 10 + BORDER
    PLAYER_Y = 10 + BORDER

    KEY_AQUIRED = False

    delay = 0.08

    my_font = pygame.font.SysFont("Arial", 30)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Set up cube
    c = cube.Cube()

    setup = [1, 1, 1, 0, 0, 2, 2, 2, 3, 3, 3]
    for side in setup:
        c.rotate_adjacent_face(side)

    # Set up maze
    maze = form_maze(c)
    screen.fill((200, 200, 200))
    render(screen, maze, CELL_SIZE, BORDER)

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
                        render(screen, maze, CELL_SIZE, BORDER)
                        PLAYER_X = 20
                    elif maze[PLAYER_Y][PLAYER_X - 1] != stickers.WALL:
                        render(screen, maze, CELL_SIZE, BORDER, PLAYER_X, PLAYER_Y)
                        PLAYER_X -= 1
                elif event.key == pygame.K_RIGHT:
                    if PLAYER_X == 20:
                        c.change_face(1)
                        maze = form_maze(c)
                        render(screen, maze, CELL_SIZE, BORDER)
                        PLAYER_X = 0
                    elif maze[PLAYER_Y][PLAYER_X + 1] != stickers.WALL:
                        render(screen, maze, CELL_SIZE, BORDER, PLAYER_X, PLAYER_Y)
                        PLAYER_X += 1
                elif event.key == pygame.K_UP:
                    if PLAYER_Y == 0:
                        c.change_face(0)
                        maze = form_maze(c)
                        render(screen, maze, CELL_SIZE, BORDER)
                        PLAYER_Y = 20
                    elif maze[PLAYER_Y - 1][PLAYER_X] != stickers.WALL:
                        render(screen, maze, CELL_SIZE, BORDER, PLAYER_X, PLAYER_Y)
                        PLAYER_Y -= 1
                elif event.key == pygame.K_DOWN:
                    if PLAYER_Y == 20:
                        c.change_face(2)
                        maze = form_maze(c)
                        render(screen, maze, CELL_SIZE, BORDER)
                        PLAYER_Y = 0
                    elif maze[PLAYER_Y + 1][PLAYER_X] != stickers.WALL:
                        render(screen, maze, CELL_SIZE, BORDER, PLAYER_X, PLAYER_Y)
                        PLAYER_Y += 1
                elif event.key == pygame.K_SPACE:
                    if maze[PLAYER_Y][PLAYER_X] in "0123":
                        c.rotate_adjacent_face(int(maze[PLAYER_Y][PLAYER_X]))
                        maze = form_maze(c)
                        render(screen, maze, CELL_SIZE, BORDER)
                    elif maze[PLAYER_Y][PLAYER_X] == "K":
                        KEY_AQUIRED = True
                        for i, row in enumerate(stickers.key_room_alt):
                            stickers.stickers["Y4"][i] = row
                        maze = form_maze(c)
                        render(screen, maze, CELL_SIZE, BORDER)
                    elif maze[PLAYER_Y][PLAYER_X] == "L" and KEY_AQUIRED:
                        run = False

        draw_player(screen, PLAYER_X, PLAYER_Y, CELL_SIZE, BORDER)

        pygame.display.update()
        # time.sleep(delay)
        await asyncio.sleep(0)

    screen.fill((200, 200, 200))
    you_win = my_font.render("You win!", False, (0, 0, 0))
    answer_is = my_font.render("The answer is:", False, (0, 0, 0))
    answer = my_font.render("[ANSWER]", False, (183, 18, 52))
    bye_now = my_font.render("Bye now...", False, (0, 0, 0))

    screen.blit(you_win, (CELL_SIZE * 9 + BORDER, CELL_SIZE * 9 + BORDER))
    screen.blit(answer_is, (CELL_SIZE * 5 + BORDER, CELL_SIZE * 10 + BORDER))
    screen.blit(answer, (CELL_SIZE * 12 + BORDER, CELL_SIZE * 10 + BORDER))
    pygame.display.update()

    await asyncio.sleep(15)

    screen.blit(bye_now, (CELL_SIZE * 9 + BORDER, CELL_SIZE * 11 + BORDER))
    pygame.display.update()

    await asyncio.sleep(2)

    screen.fill((0, 0, 0))
    screen.blit(answer, (CELL_SIZE * 12 + BORDER, CELL_SIZE * 10 + BORDER))
    pygame.display.update()

    pygame.quit()


asyncio.run(main())


# if __name__ == "__main__":
# main()
