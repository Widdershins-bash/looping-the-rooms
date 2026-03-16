import pygame
from system.constants import Font, ColorPalette as cp, Menu, Main
import math


class Stats:
    def __init__(self, surface: pygame.Surface, init_floor_size: tuple[int, int]) -> None:
        self.surface: pygame.Surface = surface

        self.font: pygame.Font = Font.STATS
        self.font_color: pygame.typing.ColorLike = cp.BLACK

        self.floor: int = 1
        self.highest_floor: int = self.floor
        self.speed: int = 0
        self.floor_size: tuple[int, int] = init_floor_size

        self.timer_on: bool = False
        self.initial_time: int = 1
        self.timer: float = self.initial_time

        self.margin: int = 5
        self.surfaces: list[pygame.Surface] = []

        self.compass: Compass = Compass(surface=self.surface, margin=self.margin)

    def get_score_surface(self) -> pygame.Surface:
        text: str = f"Floor: {self.floor}"
        return self.font.render(text, True, self.font_color)

    def get_speed_surface(self) -> pygame.Surface:
        text: str = f"Speed: +%{self.speed}"
        return self.font.render(text, True, self.font_color)

    def get_floor_size_surface(self) -> pygame.Surface:
        text: str = f"Dungeon Size: {self.floor_size[0]} x {self.floor_size[1]}"
        return self.font.render(text, True, self.font_color)

    def get_timer_surface(self) -> pygame.Surface:
        text: str = f"Timer: {self.timer:.1f}"
        return self.font.render(text, True, self.font_color)

    def get_highest_floor_surface(self) -> pygame.Surface:
        text: str = f"Session Best: {self.highest_floor}"
        return self.font.render(text, True, self.font_color)

    def get_box_size(self) -> tuple[int, int]:
        largest_width: int = self.surfaces[0].width
        for surface in self.surfaces:
            if surface.width > largest_width:
                largest_width = surface.width

        stat_box_width: int = largest_width + self.margin * 2
        stat_box_height: int = self.surfaces[0].height * len(self.surfaces) + self.margin * 2

        return stat_box_width, stat_box_height

    def start_timer(self):
        self.timer = self.initial_time
        self.timer_on = True

    def update_timer(self, delta_time: float):
        if self.timer <= 0:
            self.timer = 0

        elif self.timer_on:
            self.timer -= delta_time

    def update(self, delta_time: float, player_pos: tuple[float, float], exit_pos: tuple[float, float]):
        self.update_timer(delta_time=delta_time)
        self.surfaces = [
            self.get_score_surface(),
            self.get_highest_floor_surface(),
            self.get_speed_surface(),
            self.get_floor_size_surface(),
            self.get_timer_surface(),
        ]
        self.compass.update(delta_time=delta_time, player_pos=player_pos, exit_pos=exit_pos)

    def display_stat_gui(self):
        size_point: tuple[int, int] = self.get_box_size()
        stat_box: pygame.Surface = pygame.Surface(size_point)
        stat_box.fill(cp.GRAY)

        for i, stat in enumerate(self.surfaces):
            stat_box.blit(stat, (self.margin, i * self.surfaces[0].height + self.margin))

        self.surface.blit(stat_box, (Menu.MENU_MARGIN, Menu.MENU_MARGIN))

        self.compass.draw()


class Compass:
    def __init__(self, surface: pygame.Surface, margin: int) -> None:
        self.surface: pygame.Surface = surface
        self.margin: int = margin

        self.font: pygame.Font = Font.STATS
        self.font_small: pygame.Font = Font.STATS_SMALL

        self.width: int = Main.BASE_CONSTANT * 2
        self.height: int = Main.BASE_CONSTANT * 3
        self.container: pygame.Surface = self.get_container()

        self.circle_width: float = Main.BASE_CONSTANT * 1.5
        self.circle_height: float = Main.BASE_CONSTANT * 1.5
        self.circle_x: float = Main.BASE_CONSTANT // 4
        self.circle_y: float = self.container.height - Main.BASE_CONSTANT // 4 - self.circle_height
        self.circle: pygame.Rect = pygame.Rect(self.circle_x, self.circle_y, self.circle_width, self.circle_height)

        self.needle_width: float = 5
        self.needle_height: float = (self.circle_height - self.margin * 2) // 2

        self.needle_x: float = self.circle_x + self.circle_width / 2
        self.needle_y: float = self.circle_y + self.circle_height / 2
        self.needle: pygame.Surface = self.get_needle()
        self.rotated_needle: pygame.Surface = self.needle.copy()
        self.needle_rect: pygame.Rect = self.rotated_needle.get_rect(center=(self.needle_x, self.needle_y))

        self.degrees: float = 0

    def get_needle(self) -> pygame.Surface:
        needle_con: pygame.Surface = pygame.Surface((self.needle_width, self.needle_height * 2))
        needle_con.fill(cp.RED)
        needle: pygame.Rect = pygame.Rect(0, 0, self.needle_width, self.needle_height)
        pygame.draw.rect(needle_con, cp.WHITE, needle)

        return needle_con

    def get_container(self) -> pygame.Surface:
        box: pygame.Surface = pygame.Surface((self.width, self.height))
        box.fill(cp.GRAY)
        text: pygame.Surface = self.font.render("Exit", True, cp.BLACK)
        dir_text: pygame.Surface = self.font_small.render("N", True, cp.BLACK)
        box.blit(text, ((box.width - text.width) // 2, self.margin))
        box.blit(dir_text, ((box.width - dir_text.width) // 2, Main.BASE_CONSTANT - dir_text.height / 2))

        return box

    def update(self, delta_time: float, player_pos: tuple[float, float], exit_pos: tuple[float, float]):
        dx: float = exit_pos[0] - player_pos[0]
        dy: float = exit_pos[1] - player_pos[1]

        self.degrees = math.degrees(math.atan2(dy, dx))
        self.rotated_needle: pygame.Surface = pygame.transform.rotate(self.needle, -self.degrees + 90)
        self.needle_rect = self.rotated_needle.get_rect(center=(self.needle_x, self.needle_y))

    def draw(self):
        pygame.draw.rect(self.container, cp.WHITE, self.circle, border_radius=int(self.circle_width // 2))
        self.container.blit(self.rotated_needle, self.needle_rect)
        self.surface.blit(self.container, (self.margin, self.surface.height - self.container.height - self.margin))
