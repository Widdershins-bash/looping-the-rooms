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
        self.x_scalar: int = Main.BUTTON_CONSTANT * 4
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

        self.theme_path = "tileset.png"
        self.sheet = self.gen_image(self.path + self.theme_path, scalar=im.TILE_SCALAR)

        self.floor = self.sheet.subsurface(
            self.x_scalar, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar
        )
        self.north_wall = self.sheet.subsurface(0, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar)
        self.east_wall = self.sheet.subsurface(0, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar)
        self.south_wall = self.sheet.subsurface(0, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar)
        self.west_wall = self.sheet.subsurface(0, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar)

        self.tl_corner = self.sheet.subsurface(0, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar)
        self.tr_corner = self.sheet.subsurface(0, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar)
        self.bl_corner = self.sheet.subsurface(0, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar)
        self.br_corner = self.sheet.subsurface(0, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar)

        self.north_door = self.sheet.subsurface(
            self.x_scalar, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar
        )
        self.south_door = self.sheet.subsurface(
            self.x_scalar, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar
        )
        self.west_door = self.sheet.subsurface(
            self.x_scalar, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar
        )
        self.east_door = self.sheet.subsurface(
            self.x_scalar, self.sheet.height - self.y_scalar * 2, self.x_scalar, self.y_scalar
        )


class TileThemeTwo(Theme):
    def __init__(self) -> None:
        super().__init__()
