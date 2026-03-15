import pygame
from system.constants import Font, ColorPalette as cp, Menu


class Stats:
    def __init__(self, surface: pygame.Surface, init_floor_size: tuple[int, int]) -> None:
        self.surface: pygame.Surface = surface

        self.font: pygame.Font = Font.STATS
        self.font_color: pygame.typing.ColorLike = cp.BLACK

        self.score: int = 0
        self.high_score: int = 0
        self.floor_size: tuple[int, int] = init_floor_size
        self.timer: float = 0.0

        self.margin: int = 5
        self.surfaces: list[pygame.Surface] = []

    def get_score_surface(self) -> pygame.Surface:
        text: str = f"Floors Traversed: {self.score}"
        return self.font.render(text, True, self.font_color)

    def get_highscore_surface(self) -> pygame.Surface:
        text: str = f"Lowest Floor: {self.high_score}"
        return self.font.render(text, True, self.font_color)

    def get_floor_size_surface(self) -> pygame.Surface:
        text: str = f"Dungeon Size: {self.floor_size[0]} x {self.floor_size[1]}"
        return self.font.render(text, True, self.font_color)

    def get_timer_surface(self) -> pygame.Surface:
        text: str = f"Timer: {self.timer}"
        return self.font.render(text, True, self.font_color)

    def get_box_size(self) -> tuple[int, int]:
        largest_width: int = self.surfaces[0].width
        for surface in self.surfaces:
            if surface.width > largest_width:
                largest_width = surface.width

        stat_box_width: int = largest_width + self.margin * 2
        stat_box_height: int = self.surfaces[0].height * len(self.surfaces) + self.margin * 2

        return stat_box_width, stat_box_height

    def update(self):
        self.surfaces = [
            self.get_score_surface(),
            self.get_floor_size_surface(),
            self.get_timer_surface(),
        ]

    def display_stat_box(self):
        size_point: tuple[int, int] = self.get_box_size()
        stat_box: pygame.Surface = pygame.Surface(size_point)
        stat_box.fill(cp.GRAY)

        for i, stat in enumerate(self.surfaces):
            stat_box.blit(stat, (self.margin, i * self.surfaces[0].height + self.margin))

        self.surface.blit(stat_box, (Menu.MENU_MARGIN, Menu.MENU_MARGIN))
