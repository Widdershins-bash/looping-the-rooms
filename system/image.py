import pygame
from system.constants import Image as im, Main


class Image:
    def __init__(self) -> None:
        self.path: str = im.IMAGE_PATH

    def gen_image(self, path: str, scalar: float | None = None) -> pygame.Surface:
        image: pygame.Surface = pygame.image.load(path)
        if scalar:
            image = pygame.transform.scale_by(image, scalar)

        return image


class ButtonSprite(Image):
    def __init__(self) -> None:
        super().__init__()

        self.y_scalar: int = Main.BUTTON_CONSTANT
        self.x_scalar: int = Main.BUTTON_CONSTANT
        self.sheet: pygame.Surface = self.gen_image(self.path + "tileset.png")

        self.play: pygame.Surface = self.sheet.subsurface(0, 0, self.x_scalar, self.y_scalar)
        self.quit: pygame.Surface = self.sheet.subsurface(0, 0, self.x_scalar, self.y_scalar)
        self.resume: pygame.Surface = self.sheet.subsurface(0, 0, self.x_scalar, self.y_scalar)
        self.settings: pygame.Surface = self.sheet.subsurface(0, 0, self.y_scalar, self.y_scalar)
        self.restart: pygame.Surface = self.sheet.subsurface(0, 0, self.y_scalar, self.y_scalar)
        self.next_level: pygame.Surface = self.sheet.subsurface(0, 0, self.y_scalar, self.y_scalar)
        self.menu: pygame.Surface = self.sheet.subsurface(0, 0, self.x_scalar, self.y_scalar)
        self.volume: pygame.Surface = self.sheet.subsurface(0, 0, self.x_scalar, self.y_scalar)
        self.knob: pygame.Surface = self.sheet.subsurface(0, 0, 18, 18)


class PlayerSprite(Image):
    def __init__(self) -> None:
        super().__init__()

        self.y_scalar: int = 21
        self.x_scalar: int = 23
        self.sheet: pygame.Surface = self.gen_image(self.path + "playerWalkAnimation.png")

        self.idle_down: pygame.Surface = pygame.transform.scale_by(self.gen_image(self.path + "idle.png"), 1.5)
        self.idle_right: pygame.Surface = pygame.transform.rotate(self.idle_down, 90)
        self.idle_up: pygame.Surface = pygame.transform.rotate(self.idle_down, 180)
        self.idle_left: pygame.Surface = pygame.transform.rotate(self.idle_down, 270)

        self.walk_down: list[pygame.Surface] = [
            pygame.transform.scale_by(self.sheet.subsurface(self.x_scalar * i, 0, self.x_scalar, self.y_scalar), 1.5)
            for i in range(7)
        ]
        self.walk_right: list[pygame.Surface] = [pygame.transform.rotate(image, 90) for image in self.walk_down]
        self.walk_up: list[pygame.Surface] = [pygame.transform.rotate(image, 180) for image in self.walk_down]
        self.walk_left: list[pygame.Surface] = [pygame.transform.rotate(image, 270) for image in self.walk_down]


class ThemeManager:
    def __init__(self) -> None:

        self.theme_one: Theme = TileThemeOne()
        self.theme_two: Theme = TileThemeTwo()

        self.theme_list: list[Theme] = [self.theme_one]  # add more later


class Theme(Image):
    def __init__(self) -> None:
        super().__init__()

        self.y_scalar: float = Main.GRID_CONSTANT
        self.x_scalar: float = Main.GRID_CONSTANT
        self.theme_path: str
        self.sheet: pygame.Surface

        self.floor: pygame.Surface
        self.north_wall: pygame.Surface
        self.east_wall: pygame.Surface
        self.south_wall: pygame.Surface
        self.west_wall: pygame.Surface

        self.tl_corner: pygame.Surface
        self.tr_corner: pygame.Surface
        self.bl_corner: pygame.Surface
        self.br_corner: pygame.Surface

        # still have to figure out code
        self.item: pygame.Surface

        self.north_door: pygame.Surface
        self.south_door: pygame.Surface
        self.west_door: pygame.Surface
        self.east_door: pygame.Surface


class TileThemeOne(Theme):
    def __init__(self) -> None:
        super().__init__()

        self.theme_path = "MapTiles.png"
        self.sheet = self.gen_image(self.path + self.theme_path, scalar=im.TILE_SCALAR)

        self.floor = self.sheet.subsurface(self.x_scalar * 2, self.y_scalar * 3, self.x_scalar, self.y_scalar)

        self.wall_image: pygame.Surface = self.sheet.subsurface(
            self.x_scalar * 2, self.y_scalar, self.x_scalar, self.y_scalar
        )
        self.north_wall = pygame.transform.rotate(self.wall_image, 270)
        self.east_wall = pygame.transform.rotate(self.wall_image, 180)
        self.south_wall = pygame.transform.rotate(self.wall_image, 90)
        self.west_wall = pygame.transform.rotate(self.wall_image, 0)

        self.corner_image: pygame.Surface = self.sheet.subsurface(
            self.x_scalar * 2, self.y_scalar * 2, self.x_scalar, self.y_scalar
        )
        self.tl_corner = pygame.transform.rotate(self.corner_image, 0)
        self.tr_corner = pygame.transform.rotate(self.corner_image, 270)
        self.bl_corner = pygame.transform.rotate(self.corner_image, 90)
        self.br_corner = pygame.transform.rotate(self.corner_image, 180)

        self.north_door = self.sheet.subsurface(0, self.y_scalar, self.x_scalar * 2, self.y_scalar)
        self.south_door = self.sheet.subsurface(0, 0, self.x_scalar * 2, self.y_scalar)
        self.west_door = self.sheet.subsurface(self.x_scalar, self.y_scalar * 2, self.x_scalar, self.y_scalar * 2)
        self.east_door = self.sheet.subsurface(0, self.y_scalar * 2, self.x_scalar, self.y_scalar * 2)


class TileThemeTwo(Theme):
    def __init__(self) -> None:
        super().__init__()
