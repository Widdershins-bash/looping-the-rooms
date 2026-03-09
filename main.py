import pygame
from game.tile import Tile


pygame.init()


def get_delta_time(clock: pygame.Clock, fps: int):
    delta_time: float = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    return delta_time


screen: pygame.Surface = pygame.display.set_mode((600, 600))

clock: pygame.Clock = pygame.Clock()
FPS: int = 60

tile: Tile = Tile(surface=screen)

color_seq: float = 0
running: bool = True
while running:

    delta_time: float = get_delta_time(clock=clock, fps=FPS)

    red: int = int(color_seq) % 255
    green: int = (int(color_seq) + 85) % 255
    blue: int = (int(color_seq) + 170) % 255
    screen.fill((red, green, blue))

    tile.create_platform(width=10, height=10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    color_seq += 50 * delta_time
    pygame.display.flip()

pygame.quit()
