import pygame
from enum import Enum, auto


class Main:
    GRID_CONSTANT: int = 32  # tile size in px


class Screen:
    LOGICAL_WIDTH: int = 640
    LOGICAL_HEIGHT: int = 360
    FPS: int = 120


class Menu:
    MENU_MARGIN: int = 6


class Button:
    SCALED_SLIDER_LENGTH: int = 38
    SCALED_SLIDER_START_X: int = 28


class Camera:
    EASING_MULTIPLIER: int = 4
    TOLERANCE: float = 0.4


class Player:
    SPEED: int = Main.GRID_CONSTANT * 15
    RADIUS: int = 0  # Main.GRID_CONSTANT // 2


class Floor:
    ROOM_UNIT_SIZE: int = 10


class Image:
    IMAGE_PATH: str = "assets/images/"


class Audio:
    AUDIO_PATH: str = "assets/audio/"


class ColorPalette:
    BLACK: pygame.typing.ColorLike = "#000000"
    GRAY: pygame.typing.ColorLike = "#666666"
    WHITE: pygame.typing.ColorLike = "#ffffff"

    LIGHT_GREEN: pygame.typing.ColorLike = "#59ff00"
    MAGENTA: pygame.typing.ColorLike = "#a600ff"
    DARK_GREEN: pygame.typing.ColorLike = "#00731f"
    YELLOW: pygame.typing.ColorLike = "#eaff00"


class GameState(Enum):
    MAIN_MENU = auto()
    PLAY = auto()
    QUIT = auto()
    SETTINGS = auto()
    PAUSE = auto()


class Font:
    BASE: pygame.Font = pygame.Font("freesansbold.ttf")
    ACCENTUATED: pygame.Font = pygame.Font("freesansbold.ttf", 40)
