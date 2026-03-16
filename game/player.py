import pygame
from system.constants import Player as p, ColorPalette as cp
from system.image import PlayerSprite
from enum import Enum, auto
from system.audio import SFX
import random


class Player:
    def __init__(self, surface: pygame.Surface, size: int, start_pos: tuple[float, float], sfx: SFX) -> None:
        self.surface: pygame.Surface = surface
        self.width: int = 48
        self.height: int = 34
        self.sfx: SFX = sfx

        self.sprite: PlayerSprite = PlayerSprite()

        self.rect_margin: int = self.width // 6
        self.width -= self.rect_margin * 2
        self.x_pos: float = start_pos[0]
        self.y_pos: float = start_pos[1]

        self.initial_speed: int = self.width * 7
        self.speed: float = self.initial_speed

        self.mouse_pos: tuple[int, int] = (0, 0)
        self.last_direction: Direction = Direction.DOWN
        self.direction: Direction | None = None

        self.animation_speed: float = self.speed / 15
        self.frame: float = 0

        self.sound_speed: float = self.animation_speed / (len(self.sprite.walk_down) / 2)
        self.sound_ping: float = 0

        self.move_dict: dict[Direction, list[pygame.Surface]] = {
            Direction.UP: self.sprite.walk_up,
            Direction.DOWN: self.sprite.walk_down,
            Direction.LEFT: self.sprite.walk_left,
            Direction.RIGHT: self.sprite.walk_right,
        }

        self.idle_dict: dict[Direction, pygame.Surface] = {
            Direction.UP: self.sprite.idle_up,
            Direction.DOWN: self.sprite.idle_down,
            Direction.LEFT: self.sprite.idle_left,
            Direction.RIGHT: self.sprite.idle_right,
        }

    def scale_mouse(self, viewport: pygame.Rect, scale: int) -> tuple[int, int]:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        scale_x: int = (mouse_x - viewport.x) // scale
        scale_y: int = (mouse_y - viewport.y) // scale

        return scale_x, scale_y

    def get_movement(self, delta_time: float) -> tuple[float, float]:
        dx: float = 0.0
        dy: float = 0.0
        keys: pygame.typing.SequenceLike = pygame.key.get_pressed()
        self.direction = None

        if keys[pygame.K_UP]:
            dy -= self.speed * delta_time
            self.direction = Direction.UP

        if keys[pygame.K_DOWN]:
            dy += self.speed * delta_time
            self.direction = Direction.DOWN

        if keys[pygame.K_RIGHT]:
            dx += self.speed * delta_time
            self.direction = Direction.RIGHT

        if keys[pygame.K_LEFT]:
            dx -= self.speed * delta_time
            self.direction = Direction.LEFT

        # strictly for debugging
        # if pygame.mouse.get_just_pressed()[0]:
        #     self.x_pos, self.y_pos = self.mouse_pos

        return dx, dy

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def update_frames(self, delta_time: float):
        self.frame += self.animation_speed * delta_time
        if self.frame > len(self.sprite.walk_down):
            self.frame = 0

    def update_sound_queue(self, delta_time: float):
        if self.direction:
            self.sound_ping += self.sound_speed * delta_time

    def update(self, delta_time: float, camera_offset: tuple[float, float], viewport: pygame.Rect, scale: int) -> None:
        self.x_pos += camera_offset[0]
        self.y_pos += camera_offset[1]

        self.mouse_pos = self.scale_mouse(viewport=viewport, scale=scale)
        if self.direction != None:
            self.last_direction = self.direction
            self.update_frames(delta_time=delta_time)
            self.update_sound_queue(delta_time=delta_time)

    def draw(self) -> None:

        if self.direction != None:
            frame: pygame.Surface = self.move_dict[self.direction][int(self.frame)]
            self.surface.blit(frame, self.get_rect())
            if self.sound_ping > 1:
                random.choice(self.sfx.walking_sfx).play()
                self.sound_ping = 0

        else:
            idle: pygame.Surface = self.idle_dict[self.last_direction]
            self.surface.blit(idle, self.get_rect())

        # pygame.draw.rect(self.surface, cp.YELLOW, self.get_rect(), border_radius=p.RADIUS)


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
