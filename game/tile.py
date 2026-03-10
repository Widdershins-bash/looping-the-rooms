import pygame
import random


class TileConfiguration:
    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = grid_constant

    def create_tile(self, x: int, y: int) -> pygame.Rect:
        new_tile: pygame.Rect = pygame.Rect(x, y, self.size, self.size)
        return new_tile
