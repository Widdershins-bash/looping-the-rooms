import pygame
from system.constants import Audio as ad


class SFX:
    def __init__(self) -> None:
        self.path: str = ad.AUDIO_PATH
        self.audio_state: AudioState = AudioState(volume=50)

        self.jump_sfx: pygame.mixer.Sound = pygame.mixer.Sound(self.path + "jump.ogg")
        self.swoosh_sfx: pygame.mixer.Sound = pygame.mixer.Sound(self.path + "jump.ogg")
        self.click_sfx: pygame.mixer.Sound = pygame.mixer.Sound(self.path + "jump.ogg")
        self.hover_sfx: pygame.mixer.Sound = pygame.mixer.Sound(self.path + "jump.ogg")

    def update_volume(self) -> None:
        converted_volume: float = self.audio_state.volume / 100

        self.jump_sfx.set_volume(converted_volume)


class AudioState:
    def __init__(self, volume: int = 50) -> None:
        self.volume: int = max(0, min(100, volume))

    def set_volume(self, value: int) -> None:
        self.volume: int = max(0, min(100, value))
