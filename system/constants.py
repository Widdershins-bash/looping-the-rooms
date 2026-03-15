import pygame
from enum import Enum, auto


class Main:
    BASE_CONSTANT: int = 32  # never used in the game, rather, just used for setting the grid standard
    BASE_DIVISOR: int = 2
    GRID_CONSTANT: int = max(6, BASE_CONSTANT // BASE_DIVISOR)  # tile size in px
    BUTTON_CONSTANT: int = BASE_CONSTANT


class Screen:
    LOGICAL_WIDTH: int = 640
    LOGICAL_HEIGHT: int = 360
    FPS: int = 120


class Menu:
    MENU_MARGIN: int = 6


class Button:
    SLIDER_LENGTH: int = 88
    SLIDER_START_X: int = 20


class Camera:
    EASING_MULTIPLIER: int = 6
    TOLERANCE: float = 0.6


class Player:
    SPEED: int = Main.GRID_CONSTANT * 8
    RADIUS: int = 0  # Main.GRID_CONSTANT // 2


class Floor:
    ROOM_UNIT_SIZE: int = 10
    FLOOR_ROOM_SIZE: int = 4


class Image:
    IMAGE_PATH: str = "assets/images/"
    TILE_SCALAR: float = Main.GRID_CONSTANT / Main.BASE_CONSTANT


class Audio:
    AUDIO_PATH: str = "assets/audio/"


class ColorPalette:
    BLACK: pygame.typing.ColorLike = "#000000"
    GRAY: pygame.typing.ColorLike = "#666666"
    ALPHA_GRAY: pygame.typing.ColorLike = (122, 122, 122, 100)
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
    NEXT = auto()
    LEVEL_SELECT = auto()
    PAUSE = auto()


class Font:
    BASE: pygame.Font = pygame.Font("freesansbold.ttf")
    ACCENTUATED: pygame.Font = pygame.Font("freesansbold.ttf", 40)
