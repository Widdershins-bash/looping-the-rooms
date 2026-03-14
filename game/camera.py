import pygame
from system.constants import Camera as cm


class Camera:
    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant

        self.x_focus: float
        self.y_focus: float

    def get_offset(self, dx: float, dy: float, delta_time: float) -> tuple[float, float]:
        easing_speed: float = delta_time * cm.EASING_MULTIPLIER

        x_offset: float = (self.x_focus - dx) * easing_speed
        y_offset: float = (self.y_focus - dy) * easing_speed

        if abs(x_offset) < cm.TOLERANCE:
            x_offset = 0

        if abs(y_offset) < cm.TOLERANCE:
            y_offset = 0

        return x_offset, y_offset
