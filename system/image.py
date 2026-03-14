import pygame
from system.constants import Image as im, Main


# NOTE: this will be updated in the future with more classes and definitions to accomadate.


class Image:
    def __init__(self) -> None:
        self.path: str = im.IMAGE_PATH

    def gen_image(self, path: str, scalar: float | None = None) -> pygame.Surface:
        image: pygame.Surface = pygame.image.load(path)
        if scalar:
            pygame.transform.scale_by(image, scalar)

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
        self.menu: pygame.Surface = self.sheet.subsurface(0, 0, self.x_scalar, self.y_scalar)
        self.volume: pygame.Surface = self.sheet.subsurface(0, 0, self.x_scalar, self.y_scalar)
        self.knob: pygame.Surface = self.sheet.subsurface(0, 0, 18, 18)


class TileSprite(Image):
    def __init__(self) -> None:
        super().__init__()

        self.y_scalar: int = Main.BUTTON_CONSTANT
        self.x_scalar: int = Main.BUTTON_CONSTANT
        self.sheet: pygame.Surface = self.gen_image(self.path + "tileset.png")

        self.floor: pygame.Surface = self.sheet.subsurface(
            self.x_scalar, self.y_scalar * 4, self.x_scalar, self.y_scalar
        )
        self.north_wall: pygame.Surface = self.sheet.subsurface(0, self.y_scalar * 4, self.x_scalar, self.y_scalar)
        self.east_wall: pygame.Surface = self.sheet.subsurface(0, self.y_scalar * 4, self.x_scalar, self.y_scalar)
        self.south_wall: pygame.Surface = self.sheet.subsurface(0, self.y_scalar * 4, self.x_scalar, self.y_scalar)
        self.west_wall: pygame.Surface = self.sheet.subsurface(0, self.y_scalar * 4, self.x_scalar, self.y_scalar)
