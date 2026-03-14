import pygame
from game.floor import FloorManager
from game.camera import Camera
from game.player import Player
from game.tile import BaseTile


class World:

    def __init__(self, surface: pygame.Surface, grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant

        self.floor_manager: FloorManager = FloorManager(surface=self.surface, grid_constant=self.grid_constant)
        self.player: Player = Player(surface=self.surface, size=self.grid_constant)

        self.camera_offset: tuple[float, float] = (0, 0)
        self.camera: Camera = Camera(
            surface=self.surface,
            player_x=self.player.x_pos,
            player_y=self.player.y_pos,
            grid_constant=self.grid_constant,
        )

    def get_wall_tiles(self) -> list[BaseTile]:
        walls: list[BaseTile] = []
        for floor in self.floor_manager.floors:
            for room in floor.path.values():
                walls.extend(room.wall_map)

        return walls

    def player_found_exit(self) -> bool:
        for floor in self.floor_manager.floors:
            x_check: bool = (
                self.player.x_pos > floor.exit.start_x and self.player.x_pos < floor.exit.start_x + floor.exit.width
            )
            y_check: bool = (
                self.player.y_pos > floor.exit.start_y and self.player.y_pos < floor.exit.start_y + floor.exit.height
            )

            if x_check and y_check:
                return True

        return False

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

    def update(self, delta_time: float) -> None:
        self.camera_offset = self.camera.get_offset(
            player_x=self.player.x_pos, player_y=self.player.y_pos, delta_time=delta_time
        )
        self.update_collisions(delta_time=delta_time)
        self.floor_manager.update(camera_offset=self.camera_offset)
        self.player.update(camera_offset=self.camera_offset)

    def draw(self):
        self.floor_manager.draw()
        self.player.draw()
        self.draw_alerts()
