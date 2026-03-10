import pygame

pygame.init()

from game.room.tile import Tile
from system.screen import Screen
from system.constants import Main, GameState as gs
from game.room.floor_generator import FloorManager


def get_delta_time(clock: pygame.Clock, fps: int):
    delta_time: float = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    return delta_time


screen: Screen = Screen(grid_constant=Main.GRID_CONSTANT)
tile: Tile = Tile(surface=screen.logical)
floor_manager: FloorManager = FloorManager()

if __name__ == "__main__":

    floor_manager.print_plan()

    game_state: gs = gs.PLAY

    while screen.running:

        delta_time: float = get_delta_time(clock=screen.clock, fps=screen.fps)

        for event in pygame.event.get():
            if screen.running:
                screen.handle_events(event=event, game_state=game_state)

        tile.create_platform(width=10, height=10)

        screen.scale_flip()

    pygame.quit()
