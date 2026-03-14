import pygame
from game.floor import FloorManager, Floor, Room
from game.camera import Camera
from game.player import Player
from game.tile import BaseTile


class World:

    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant

        self.floor_manager: FloorManager = FloorManager(surface=self.surface, grid_constant=self.grid_constant)
        self.current_floor: Floor = self.floor_manager.floors[self.floor_manager.current_floor_index]
        self.player: Player = Player(surface=self.surface, size=self.grid_constant)

        self.camera_offset: tuple[float, float] = (0, 0)
        self.camera: Camera = Camera(surface=self.surface, grid_constant=self.grid_constant)

    def get_wall_tiles(self) -> list[BaseTile]:
        walls: list[BaseTile] = []
        for room in self.current_floor.path.values():
            walls.extend(room.wall_map)

        return walls

    def player_found_exit(self) -> bool:
        if self.player.get_rect().colliderect(self.current_floor.exit.get_rect()):
            return True

        return False

    def get_room_player_in(self) -> Room:
        for room in self.current_floor.path.values():
            if self.player.get_rect().colliderect(room.get_rect()):
                return room

        return self.current_floor.entrance

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

    def update_camera_offset(self, delta_time: float) -> None:
        room: Room = self.get_room_player_in()
        self.camera.x_focus = room.x_focus
        self.camera.y_focus = room.y_focus

        self.camera_offset = self.camera.get_offset(dx=room.x_pos, dy=room.y_pos, delta_time=delta_time)

    def update(self, delta_time: float, viewport: pygame.Rect, scale: int) -> None:
        new_floor: Floor = self.floor_manager.floors[self.floor_manager.current_floor_index]
        if new_floor is not self.current_floor:
            self.current_floor = new_floor

        self.update_camera_offset(delta_time=delta_time)
        self.update_collisions(delta_time=delta_time)
        self.floor_manager.update(camera_offset=self.camera_offset)
        self.player.update(camera_offset=self.camera_offset, viewport=viewport, scale=scale)

    def draw(self):
        self.floor_manager.draw()
        self.player.draw()
        self.draw_alerts()
