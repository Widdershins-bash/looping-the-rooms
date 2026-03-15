import pygame
from system.constants import Floor as fl, GameState as gs
from game.floor import FloorManager, Room
from game.camera import Camera
from game.player import Player
from game.tile import BaseTile


class World:

    def __init__(self, surface: pygame.Surface, grid_constant: int, init_state: gs) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant
        self.game_state: gs = init_state

        self.floor_manager: FloorManager = FloorManager(surface=self.surface, grid_constant=self.grid_constant)
        self.player: Player = Player(surface=self.surface, size=self.grid_constant)

        self.camera_offset: tuple[float, float] = (0, 0)
        self.camera: Camera = Camera(surface=self.surface, grid_constant=self.grid_constant)

        self.event_ping: bool = True
        self.finish_timer_event: int = pygame.event.custom_type()

    def get_wall_tiles(self) -> list[BaseTile]:
        walls: list[BaseTile] = []
        for room in self.floor_manager.floor.path.values():
            walls.extend(room.wall_map)

        return walls

    def player_found_exit(self) -> bool:
        if self.player.get_rect().colliderect(self.floor_manager.floor.exit.get_rect()):
            return True

        return False

    def get_room_player_in(self) -> Room:
        for room in self.floor_manager.floor.path.values():
            if self.player.get_rect().colliderect(room.get_rect()):
                return room

        return self.floor_manager.floor.entrance

    def move_player_and_collide(self, dx: float, dy: float) -> None:
        wall_tiles: list[BaseTile] = self.get_wall_tiles()

        # Splitting up the x check and y check creates much smoother physics.
        self.player.x_pos += dx
        for wall_tile in wall_tiles:
            if self.player.get_rect().colliderect(wall_tile.get_rect()):
                self.player.x_pos -= dx

        self.player.y_pos += dy
        for wall_tile in wall_tiles:
            if self.player.get_rect().colliderect(wall_tile.get_rect()):
                self.player.y_pos -= dy

    def update_collisions(self, delta_time: float) -> None:
        dx, dy = self.player.get_movement(delta_time=delta_time)
        self.move_player_and_collide(dx=dx, dy=dy)

    def draw_alerts(self) -> None:
        if self.player_found_exit():
            self.floor_manager.display_room_found()
            if self.event_ping:
                pygame.time.set_timer(self.finish_timer_event, 2000, loops=1)
                self.event_ping = False

    def handle_events(self, event: pygame.Event):
        if event.type == self.finish_timer_event:
            self.event_ping = True
            self.game_state = gs.LEVEL_SELECT

    def update_camera_offset(self, delta_time: float) -> None:
        room: Room = self.get_room_player_in()
        self.camera.x_focus = room.x_focus
        self.camera.y_focus = room.y_focus

        self.camera_offset = self.camera.get_offset(dx=room.x_pos, dy=room.y_pos, delta_time=delta_time)

    def update(self, delta_time: float, viewport: pygame.Rect, scale: int) -> None:
        if self.game_state == gs.NEXT:
            self.floor_manager.floor = self.floor_manager.spawn_floor()
            self.game_state = gs.PLAY

        if self.game_state == gs.PLAY:
            self.update_camera_offset(delta_time=delta_time)
            self.update_collisions(delta_time=delta_time)
            self.floor_manager.update(camera_offset=self.camera_offset)
            self.player.update(camera_offset=self.camera_offset, viewport=viewport, scale=scale)

    def draw(self):
        self.floor_manager.draw()
        self.player.draw()

        if self.game_state == gs.PLAY:
            self.draw_alerts()
