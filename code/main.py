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


def draw_lock(screen: pygame.Surface, CELL_SIZE: int, rotation: int):
    tile = pygame.Surface((CELL_SIZE, CELL_SIZE))
    lock = pygame.image.load("sprites/Lock_2.png")
    tile.blit(lock, (0, 0))
    tile = pygame.transform.rotate(tile, 90 * rotation)
    screen.blit(tile, (10 * CELL_SIZE, 10 * CELL_SIZE))


def draw_key(screen: pygame.Surface, CELL_SIZE: int, rotation: int):
    tile = pygame.Surface((CELL_SIZE, CELL_SIZE))
    lock = pygame.image.load("sprites/Key.png")
    tile.blit(lock, (0, 0))
    tile = pygame.transform.rotate(tile, 90 * rotation)
    screen.blit(tile, (10 * CELL_SIZE, 10 * CELL_SIZE))


def draw_cell(
    screen: pygame.Surface,
    maze: List[List[str]],
    c: cube.Cube,
    CELL_SIZE: int,
    x: int,
    y: int,
    colorblind: bool,
):
    if maze[y][x] == "L":
        draw_lock(screen, CELL_SIZE, c.rotation)
    elif maze[y][x] == "K":
        draw_key(screen, CELL_SIZE, c.rotation)
    elif not colorblind:
        pygame.draw.rect(
            screen,
            vary_color(stickers.colors[maze[y][x]]),
            (
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            ),
        )
    else:
        tile = pygame.Surface((CELL_SIZE, CELL_SIZE))
        tile.fill(vary_color(stickers.colors[maze[y][x]]))
        char = (
            maze[y][x]
            if maze[y][x] not in "0123DP"
            else (
                "#"
                if maze[y][x] == "D"
                else ("" if maze[y][x] == "P" else "BRGO"[int(maze[y][x])])
            )
        )
        text = my_font.render(char, False, (0, 0, 0))
        tile.blit(
            text,
            (
                CELL_SIZE // 2 - text.get_width() // 2,
                CELL_SIZE // 2 - text.get_height() // 2,
            ),
        )
        screen.blit(tile, (x * CELL_SIZE, y * CELL_SIZE))


def render_maze(
    screen: pygame.Surface,
    maze: List[List[str]],
    c: cube.Cube,
    CELL_SIZE: int,
    colorblind: bool,
    x: Optional[int] = None,
    y: Optional[int] = None,
):
    if x is not None and y is not None:
        draw_cell(screen, maze, c, CELL_SIZE, x, y, colorblind)
    else:
        for i in range(21):
            for j in range(21):
                draw_cell(screen, maze, c, CELL_SIZE, j, i, colorblind)


def draw_player(
    screen: pygame.Surface,
    PLAYER_X: int,
    PLAYER_Y: int,
    CELL_SIZE: int,
    interactable: bool,
):
    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (
            PLAYER_X * CELL_SIZE,
            PLAYER_Y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        ),
    )
    pygame.draw.rect(
        screen,
        (135, 206, 235),
        (
            PLAYER_X * CELL_SIZE + (CELL_SIZE // 4),
            PLAYER_Y * CELL_SIZE + (CELL_SIZE // 4),
            CELL_SIZE // 2,
            CELL_SIZE // 2,
        ),
    )
    if interactable:
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                PLAYER_X * CELL_SIZE + 3 * (CELL_SIZE // 8),
                PLAYER_Y * CELL_SIZE + 3 * (CELL_SIZE // 8),
                CELL_SIZE // 4,
                CELL_SIZE // 4,
            ),
        )


def move(
    direction: int,
    screen: pygame.Surface,
    maze: List[List[str]],
    c: cube.Cube,
    CELL_SIZE: int,
    PLAYER_X: int,
    PLAYER_Y: int,
    colorblind: bool,
) -> Tuple[List[List[str]], int, int]:
    coords = [PLAYER_X, PLAYER_Y]
    if coords[[1, 0, 1, 0][direction]] == [0, 20, 20, 0][direction]:
        c.change_face(direction)
        maze = form_maze(c)
        render_maze(screen, maze, c, CELL_SIZE, colorblind)
        coords[[1, 0, 1, 0][direction]] = [20, 0, 0, 20][direction]
    elif (
        maze[PLAYER_Y + [-1, 0, 1, 0][direction]][PLAYER_X + [0, 1, 0, -1][direction]]
        not in stickers.WALLS
    ):
        render_maze(screen, maze, c, CELL_SIZE, colorblind, PLAYER_X, PLAYER_Y)
        coords[[1, 0, 1, 0][direction]] += [-1, 1, 1, -1][direction]
    return maze, *coords


pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont("arial", 30, bold=True)


async def main():
    CELL_SIZE = 32

    SCREEN_WIDTH = 21 * CELL_SIZE
    SCREEN_HEIGHT = 21 * CELL_SIZE

    PLAYER_X = 10
    PLAYER_Y = 10

    KEY_AQUIRED = False
    intro = True
    win = False
    run = True
    colorblind = False

    delay, increment = 0.25, 0.1

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    clock.tick(30)

    welcome_to = my_font.render("Welcome to...", False, (0, 0, 0))
    lockbox = pygame.transform.scale_by(my_font.render("LOCKBOX", False, (0, 0, 0)), 3)
    colorblind_settings = my_font.render(
        "Colorblind Mode (C to toggle):", False, (0, 0, 0)
    )
    active = my_font.render("ACTIVE", False, (0, 0, 0))
    inactive = my_font.render("INACTIVE", False, (0, 0, 0))
    movement = my_font.render("Arrow keys or WASD to move", False, (0, 0, 0))
    interaction = my_font.render("Spacebar to interact", False, (0, 0, 0))
    press_space = my_font.render("Press space to play", False, (0, 0, 0))

    # Set up cube
    c = cube.Cube()

    # setup = [3, 3, 3, 0, 3, 1, 1, 1] # L' B L R'
    setup = [1, 1, 1, 0, 0, 2, 2, 2, 3, 3, 3]  # R' B2 F' L'

    for side in setup:
        c.rotate_adjacent_face(side)

    # Set up maze
    maze = form_maze(c)

    MOVE_LOG = [None, None, None, None]

    while run:
        if intro:
            screen.fill((200, 200, 200))
            screen.blit(welcome_to, (CELL_SIZE * 2, CELL_SIZE * 2))
            screen.blit(lockbox, (CELL_SIZE * 4, CELL_SIZE * 4))
            screen.blit(colorblind_settings, (CELL_SIZE * 2, CELL_SIZE * 10))
            if colorblind:
                screen.blit(active, (CELL_SIZE * 16, CELL_SIZE * 10))
            else:
                screen.blit(inactive, (CELL_SIZE * 16, CELL_SIZE * 10))
            screen.blit(movement, (CELL_SIZE * 2, CELL_SIZE * 14))
            screen.blit(interaction, (CELL_SIZE * 2, CELL_SIZE * 15))
            screen.blit(press_space, (CELL_SIZE * 6, CELL_SIZE * 18))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        intro = False
                        render_maze(screen, maze, c, CELL_SIZE, colorblind)
                    if event.key == pygame.K_c:
                        colorblind = not colorblind
        else:
            # Handle Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    for i, keys in enumerate(
                        [
                            (pygame.K_UP, pygame.K_w),
                            (pygame.K_RIGHT, pygame.K_d),
                            (pygame.K_DOWN, pygame.K_s),
                            (pygame.K_LEFT, pygame.K_a),
                        ]
                    ):
                        if event.key in keys:
                            MOVE_LOG[i] = time.time()
                            maze, PLAYER_X, PLAYER_Y = move(
                                i,
                                screen,
                                maze,
                                c,
                                CELL_SIZE,
                                PLAYER_X,
                                PLAYER_Y,
                                colorblind,
                            )
                    if event.key == pygame.K_SPACE:
                        if maze[PLAYER_Y][PLAYER_X] in "0123":
                            c.rotate_adjacent_face(int(maze[PLAYER_Y][PLAYER_X]))
                            maze = form_maze(c)
                            render_maze(screen, maze, c, CELL_SIZE, colorblind)
                        elif maze[PLAYER_Y][PLAYER_X] == "K":
                            KEY_AQUIRED = True
                            for i, row in enumerate(stickers.key_room_alt):
                                stickers.stickers["Y4"][i] = row
                            maze = form_maze(c)
                            render_maze(screen, maze, c, CELL_SIZE, colorblind)
                        elif maze[PLAYER_Y][PLAYER_X] == "L" and KEY_AQUIRED:
                            run = False
                            win = True
                elif event.type == pygame.KEYUP:
                    for i, keys in enumerate(
                        [
                            (pygame.K_UP, pygame.K_w),
                            (pygame.K_RIGHT, pygame.K_d),
                            (pygame.K_DOWN, pygame.K_s),
                            (pygame.K_LEFT, pygame.K_a),
                        ]
                    ):
                        if event.key in keys:
                            MOVE_LOG[i] = None
            for i in range(4):
                if MOVE_LOG[i] is not None and time.time() - MOVE_LOG[i] > delay:
                    maze, PLAYER_X, PLAYER_Y = move(
                        i,
                        screen,
                        maze,
                        c,
                        CELL_SIZE,
                        PLAYER_X,
                        PLAYER_Y,
                        colorblind,
                    )
                    MOVE_LOG[i] = time.time() - delay + increment

            draw_player(
                screen,
                PLAYER_X,
                PLAYER_Y,
                CELL_SIZE,
                maze[PLAYER_Y][PLAYER_X] in "0123KL",
            )

        pygame.display.update()
        # time.sleep(delay)
        await asyncio.sleep(0)

    if win:
        screen.fill((200, 200, 200))
        you_win = pygame.transform.scale_by(
            my_font.render("You win!", False, (0, 0, 0)), 2
        )
        answer_is = my_font.render("The answer is:", False, (0, 0, 0))
        answer = my_font.render(
            "FIZZING", False, (183, 18, 52) if not colorblind else (0, 0, 0)
        )
        bye_now = my_font.render("Thank you for playing. Bye now...", False, (0, 0, 0))

        screen.blit(you_win, (CELL_SIZE * 7, CELL_SIZE * 7))
        screen.blit(answer_is, (CELL_SIZE * 5, CELL_SIZE * 10))
        screen.blit(answer, (CELL_SIZE * 12, CELL_SIZE * 10))
        pygame.display.update()

        await asyncio.sleep(2)

        screen.blit(bye_now, (CELL_SIZE * 3, CELL_SIZE * 13))
        pygame.display.update()

        await asyncio.sleep(2)

        screen.fill((0, 0, 0) if not colorblind else (255, 255, 255))
        screen.blit(answer, (CELL_SIZE * 12, CELL_SIZE * 10))
        pygame.display.update()

    pygame.quit()


asyncio.run(main())


# if __name__ == "__main__":
# main()
