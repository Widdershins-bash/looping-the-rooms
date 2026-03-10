import pygame
from game.floor import FloorManager


class World:

    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant

        self.floor_manager: FloorManager = FloorManager(surface=self.surface, grid_constant=self.grid_constant)

    def update(self):
        self.floor_manager.update()

    def draw(self):
        self.floor_manager.draw()
