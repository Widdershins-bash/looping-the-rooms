import pygame

pygame.init()

from system.screen import Screen
from system.menu import MenuManager
from system.audio import SFX
from system.constants import Main, GameState as gs
from game.world import World


def get_delta_time(clock: pygame.Clock, fps: int):
    delta_time: float = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    return delta_time


game_state: gs = gs.MAIN_MENU

screen: Screen = Screen()
sfx: SFX = SFX()
world: World = World(surface=screen.logical, grid_constant=Main.GRID_CONSTANT)
menu: MenuManager = MenuManager(surface=screen.alpha, init_state=game_state, sfx=sfx)

if __name__ == "__main__":

    game_state: gs = gs.PLAY

    while screen.running:

        screen.clear()

        delta_time: float = get_delta_time(clock=screen.clock, fps=screen.fps)
        if menu.game_state != game_state:
            if game_state == gs.MAIN_MENU and menu.game_state == gs.PLAY:
                world.__init__(surface=world.surface, grid_constant=world.grid_constant)

            game_state = menu.game_state

        for event in pygame.event.get():
            if screen.running:
                screen.handle_events(event=event, game_state=game_state)

        menu.update(viewport=screen.viewport, scale=screen.scalar)
        menu.draw()

        if game_state == gs.PLAY:
            world.update(delta_time=delta_time)
        world.draw()

        screen.scale_flip()

    pygame.quit()
