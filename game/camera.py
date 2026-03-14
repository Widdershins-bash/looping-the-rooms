import pygame
from system.constants import Camera as cm


class Camera:
    def __init__(self, surface: pygame.Surface, player_x: float, player_y: float, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.initial_x: float = player_x
        self.initial_y: float = player_y
        self.grid_constant: int = grid_constant

        self.x_offset: float = 0
        self.y_offset: float = 0

    def get_offset(self, player_x: float, player_y: float, delta_time: float) -> tuple[float, float]:
        easing_speed: float = delta_time * cm.EASING_MULTIPLIER

        self.x_offset = (self.initial_x - player_x) * easing_speed
        self.y_offset = (self.initial_y - player_y) * easing_speed

        offset: tuple[float, float] = self.x_offset, self.y_offset

        return offset
