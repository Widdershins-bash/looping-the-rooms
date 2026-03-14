import pygame
from system.constants import Player as p, ColorPalette as cp


class Player:
    def __init__(self, surface: pygame.Surface, size: int) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = size

        self.rect_margin: int = self.size // 6
        self.size -= self.rect_margin * 2
        self.x_pos: float = self.surface.width // 2 + self.rect_margin
        self.y_pos: float = self.surface.height // 2 + self.rect_margin

        self.mouse_pos: tuple[int, int] = (0, 0)

    def scale_mouse(self, viewport: pygame.Rect, scale: int) -> tuple[int, int]:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        scale_x: int = (mouse_x - viewport.x) // scale
        scale_y: int = (mouse_y - viewport.y) // scale

        return scale_x, scale_y

    def get_movement(self, delta_time: float) -> tuple[float, float]:
        dx: float = 0.0
        dy: float = 0.0
        keys: pygame.typing.SequenceLike = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            dy -= p.SPEED * delta_time

        if keys[pygame.K_DOWN]:
            dy += p.SPEED * delta_time

        if keys[pygame.K_RIGHT]:
            dx += p.SPEED * delta_time

        if keys[pygame.K_LEFT]:
            dx -= p.SPEED * delta_time

        # strictly for debugging
        if pygame.mouse.get_just_pressed()[0]:
            self.x_pos, self.y_pos = self.mouse_pos

        return dx, dy

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)

    def update(self, camera_offset: tuple[float, float], viewport: pygame.Rect, scale: int) -> None:
        self.x_pos += camera_offset[0]
        self.y_pos += camera_offset[1]

        self.mouse_pos = self.scale_mouse(viewport=viewport, scale=scale)

    def draw(self) -> None:
        pygame.draw.rect(self.surface, cp.YELLOW, self.get_rect(), border_radius=p.RADIUS)
