import pygame

pygame.init()

from system.screen import Screen
from system.constants import Main, GameState as gs
from game.world import World


def get_delta_time(clock: pygame.Clock, fps: int):
    delta_time: float = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    return delta_time


screen: Screen = Screen()
world: World = World(surface=screen.logical, grid_constant=Main.GRID_CONSTANT)

if __name__ == "__main__":

    game_state: gs = gs.PLAY

    while screen.running:

        screen.clear()

        delta_time: float = get_delta_time(clock=screen.clock, fps=screen.fps)

        for event in pygame.event.get():
            if screen.running:
                screen.handle_events(event=event, game_state=game_state)

        world.update(delta_time=delta_time)
        world.draw()

        screen.scale_flip()

    pygame.quit()
