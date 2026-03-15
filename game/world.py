import pygame
from system.constants import Floor as fl, GameState as gs
from system.stats import Stats
from system.audio import SFX
from game.floor import FloorManager, Room
from game.camera import Camera
from game.player import Player
from game.tile import BaseTile


class World:

    def __init__(self, surface: pygame.Surface, grid_constant: int, init_state: gs, sfx: SFX) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant
        self.game_state: gs = init_state
        self.sfx: SFX = sfx

        self.floor_manager: FloorManager = FloorManager(surface=self.surface, grid_constant=self.grid_constant)
        self.player: Player = Player(surface=self.surface, size=self.grid_constant)
        self.camera_offset: tuple[float, float] = (0, 0)
        self.camera: Camera = Camera(surface=self.surface, grid_constant=self.grid_constant)
        self.stat_tracker: Stats = Stats(
            surface=self.surface, init_floor_size=(self.floor_manager.floor_size[0], self.floor_manager.floor_size[1])
        )

        self.event_ping: bool = True
        self.finish_timer_event: int = pygame.event.custom_type()

    def start_world(self, init_state: gs):
        self.game_state = init_state
        self.floor_manager: FloorManager = FloorManager(surface=self.surface, grid_constant=self.grid_constant)
        self.player: Player = Player(surface=self.surface, size=self.grid_constant)
        self.camera_offset: tuple[float, float] = (0, 0)
        self.camera: Camera = Camera(surface=self.surface, grid_constant=self.grid_constant)

        self.stat_tracker.initial_time = len(self.floor_manager.floor.path.values()) * 2
        self.stat_tracker.timer = self.stat_tracker.initial_time
        self.stat_tracker.timer_on = False

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

    def check_grab_upgrade(self):
        if (
            self.player.get_rect().colliderect(self.floor_manager.floor.upgrade.get_rect())
            and self.floor_manager.floor.is_upgrade
        ):
            self.floor_manager.floor.upgrade_room.tile_mesh.remove(self.floor_manager.floor.upgrade)
            self.stat_tracker.speed += 20
            self.player.speed = self.player.initial_speed * (100 + self.stat_tracker.speed) / 100
            self.sfx.upgrade_sfx.play()
            self.floor_manager.floor.is_upgrade = False

    def update_collisions(self, delta_time: float) -> None:
        dx, dy = self.player.get_movement(delta_time=delta_time)
        self.move_player_and_collide(dx=dx, dy=dy)
        self.check_grab_upgrade()

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

    def update_stats(self):
        self.stat_tracker.initial_time = len(self.floor_manager.floor.path.values()) * 2
        self.stat_tracker.timer = self.stat_tracker.initial_time
        self.stat_tracker.timer_on = False
        self.stat_tracker.floor += 1
        if self.stat_tracker.floor > self.stat_tracker.highest_floor:
            self.stat_tracker.highest_floor = self.stat_tracker.floor

        self.stat_tracker.floor_size = (self.floor_manager.floor_size[0], self.floor_manager.floor_size[1])

    def update_stats_timer(self):
        room_in: Room = self.get_room_player_in()

        if room_in == self.floor_manager.floor.exit:
            self.stat_tracker.timer_on = False

        elif room_in != self.floor_manager.floor.entrance and not self.stat_tracker.timer_on:
            self.stat_tracker.start_timer()

        if self.stat_tracker.timer == 0:
            self.game_state = gs.LOSE
            self.stat_tracker.timer = (
                self.stat_tracker.initial_time
            )  # temporary reset so that it doesn't loop the loosing state

    def update(self, delta_time: float, viewport: pygame.Rect, scale: int) -> None:
        if self.game_state == gs.NEXT:
            self.floor_manager.floor = self.floor_manager.spawn_floor()
            self.update_stats()
            self.game_state = gs.PLAY

        if self.game_state == gs.PLAY:
            self.update_camera_offset(delta_time=delta_time)
            self.update_collisions(delta_time=delta_time)
            self.floor_manager.update(camera_offset=self.camera_offset)
            self.player.update(camera_offset=self.camera_offset, viewport=viewport, scale=scale)
            self.stat_tracker.update(delta_time=delta_time)
            self.update_stats_timer()

    def draw(self):
        self.floor_manager.draw()
        self.player.draw()

        if self.game_state == gs.PLAY:
            self.draw_alerts()
            self.stat_tracker.display_stat_box()
