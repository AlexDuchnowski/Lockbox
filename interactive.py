import time

import pygame

import cube
import pieces
import rotation as rot

pygame.init()

CELL_SIZE = 20

SCREEN_WIDTH = 23 * CELL_SIZE
SCREEN_HEIGHT = 23 * CELL_SIZE

PLAYER_X = 11
PLAYER_Y = 11

delay = 0.08

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

c = cube.Cube()

maze_view = c.get_face()


def render():
    # TODO: Implement this method
    for i in range(3):
        for j in range(3):
            for k in range(7):
                for l in range(7):
                    pygame.draw.rect(
                        screen,
                        pieces.colors[
                            rot.rotate_n(pieces.cells[maze_view[i][j]], c.rotation)[k][
                                l
                            ]
                        ],
                        (
                            (j * 7 + l + 1) * CELL_SIZE,
                            (i * 7 + k + 1) * CELL_SIZE,
                            CELL_SIZE,
                            CELL_SIZE,
                        ),
                    )


run = True
while run:
    screen.fill((0, 0, 0))
    render()
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        ((PLAYER_X + 1) * CELL_SIZE, (PLAYER_Y + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE),
    )

    # Handle Key Presses
    # key = pygame.key.get_pressed()

    # if key[pygame.K_LEFT]:
    #     player.move_ip(-CELL_SIZE, 0)
    # elif key[pygame.K_RIGHT]:
    #     player.move_ip(CELL_SIZE, 0)
    # elif key[pygame.K_UP]:
    #     player.move_ip(0, -CELL_SIZE)
    # elif key[pygame.K_DOWN]:
    #     player.move_ip(0, CELL_SIZE)

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PLAYER_X -= 1
            elif event.key == pygame.K_RIGHT:
                PLAYER_X += 1
            elif event.key == pygame.K_UP:
                PLAYER_Y -= 1
            elif event.key == pygame.K_DOWN:
                PLAYER_Y += 1

    pygame.display.update()
    time.sleep(delay)

pygame.quit()
