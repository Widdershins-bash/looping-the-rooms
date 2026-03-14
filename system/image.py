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
    def __int__(self):
        super().__init__()

        self.y_scalar: int = Main.GRID_CONSTANT

        self.play: pygame.Surface
        self.quit: pygame.Surface
        self.resume: pygame.Surface
        self.settings: pygame.Surface
        self.menu: pygame.Surface
        self.volume: pygame.Surface
        self.knob: pygame.Surface
