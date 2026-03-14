import pygame


class TileConfiguration:
    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.size: int = grid_constant

    def create_tile(self, x: int, y: int, color: pygame.typing.ColorLike) -> Tile:
        tile: Tile = Tile(surface=self.surface, size=self.size, x=x, y=y, color=color)
        return tile

    def create_door(self, w: int, h: int, x: int, y: int, color: pygame.typing.ColorLike) -> Door:
        door: Door = Door(surface=self.surface, w=w, h=h, x=x, y=y, color=color)
        return door

    def create_collide(self, x: int, y: int, color: pygame.typing.ColorLike) -> CollideTile:
        collide_tile: CollideTile = CollideTile(surface=self.surface, size=self.size, x=x, y=y, color=color)
        return collide_tile


class BaseTile:
    def __init__(self, surface: pygame.Surface, x: int, y: int, color: pygame.typing.ColorLike) -> None:
        self.surface: pygame.Surface = surface
        self.x_pos: float = x
        self.y_pos: float = y
        self.color: pygame.typing.ColorLike = color

        self.width: int = 0
        self.height: int = 0

    def get_rect(self):
        return pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def on_screen(self):
        check_x: bool = self.x_pos > -self.width and self.x_pos < self.surface.width
        check_y: bool = self.y_pos > -self.height and self.y_pos < self.surface.height

        return True if check_x and check_y else False

    def draw(self):
        if self.on_screen:
            pygame.draw.rect(self.surface, self.color, self.get_rect())


class Tile(BaseTile):
    def __init__(self, surface: pygame.Surface, size: int, x: int, y: int, color: pygame.typing.ColorLike) -> None:
        super().__init__(surface, x, y, color)
        self.width, self.height = size, size


class Door(BaseTile):
    def __init__(self, surface: pygame.Surface, w: int, h: int, x: int, y: int, color: pygame.typing.ColorLike) -> None:
        super().__init__(surface, x, y, color)
        self.width, self.height = w, h


class CollideTile(BaseTile):
    def __init__(self, surface: pygame.Surface, size: int, x: int, y: int, color: pygame.typing.ColorLike) -> None:
        super().__init__(surface, x, y, color)
        self.width, self.height = size, size
