import pygame
import random


class Tile:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface: pygame.Surface = surface

        self.size: int = 32

    def create_platform(self, width: int, height: int) -> None:

        x_offset: int = (self.surface.width - self.size * width) // 2
        y_offset: int = (self.surface.height - self.size * height) // 2

        for h in range(height):
            for w in range(width):
                rand_gray: int = random.randint(60, 90)
                grayscale: tuple[int, int, int] = (rand_gray, rand_gray, rand_gray)

                x_loc: int = w * self.size + x_offset
                y_loc: int = h * self.size + y_offset

                self.rect: pygame.Rect = pygame.Rect((x_loc, y_loc), (self.size, self.size))
                pygame.draw.rect(self.surface, grayscale, self.rect)
