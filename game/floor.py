import pygame
import random
from enum import Enum, auto
from system.constants import Main, Floor as fl, ColorPalette as cp, Font
from game.tile import TileConfiguration, BaseTile
import math


class FloorManager:
    def __init__(self, surface: pygame.Surface, grid_constant: int):
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant

        self.first_floor_config: FloorConfiguration = FloorConfiguration(
            surface=self.surface, grid_constant=self.grid_constant, rows=5, columns=5
        )
        self.first_floor: Floor = Floor(
            surface=self.surface,
            grid_constant=self.grid_constant,
            path=self.first_floor_config.generate_path(),
            entrance=self.first_floor_config.entrance,
            exit=self.first_floor_config.exit,
        )

        self.floors: list[Floor] = [self.first_floor]
        self.floor_margin: int = self.grid_constant

    def update(self, camera_offset: tuple[float, float]):
        for floor in self.floors:
            floor.update(camera_offset=camera_offset)

    def display_room_found(self):
        message: str = "You Found The Exit!"
        display: pygame.Surface = Font.ACCENTUATED.render(text=message, antialias=True, color=cp.MAGENTA)
        self.surface.blit(display, ((self.surface.width - display.width) // 2, self.grid_constant * 4))

    def draw(self):
        for floor in self.floors:
            floor.draw()


class FloorConfiguration:
    def __init__(self, surface: pygame.Surface, grid_constant: int, rows: int = 4, columns: int = 4) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant
        self.rows: int = rows
        self.cols: int = columns

        self.entrance: tuple[int, int] = self.get_random_entrance()
        self.exit: tuple[int, int] = self.get_random_exit()

        self.movement_dict: dict[Direction, tuple[int, int]] = {
            Direction.SOUTH: (1, 0),
            Direction.NORTH: (-1, 0),
            Direction.WEST: (0, -1),
            Direction.EAST: (0, 1),
        }

        self.door_connections_dict: dict[Direction, Direction] = {
            Direction.SOUTH: Direction.NORTH,
            Direction.NORTH: Direction.SOUTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
        }

    def get_random_entrance(self) -> tuple[int, int]:
        entrance_row: int = 0
        entrance_col: int = 0

        return entrance_row, entrance_col

    def get_random_exit(self) -> tuple[int, int]:
        exit_row: int = self.rows - 1
        exit_col: int = self.cols - 1  # temp placeholders

        return exit_row, exit_col

    def check_direction(
        self, row: int, col: int, direction: Direction, room_dict: dict[tuple[int, int], Room]
    ) -> Direction | None:
        move: tuple[int, int] = self.movement_dict[direction]
        next_row = row + move[0]
        next_col = col + move[1]

        if (next_row, next_col) not in room_dict:
            return direction

    def get_next_direction(
        self, current_row: int, current_col: int, room_dict: dict[tuple[int, int], Room]
    ) -> Direction | None:
        valid: list[Direction] = []
        row: int = current_row
        col: int = current_col

        if row - 1 >= 0 and self.check_direction(row=row, col=col, direction=Direction.NORTH, room_dict=room_dict):
            valid.append(Direction.NORTH)

        if row + 1 < self.rows and self.check_direction(
            row=row, col=col, direction=Direction.SOUTH, room_dict=room_dict
        ):
            valid.append(Direction.SOUTH)

        if col - 1 >= 0 and self.check_direction(row=row, col=col, direction=Direction.WEST, room_dict=room_dict):
            valid.append(Direction.WEST)

        if col + 1 < self.cols and self.check_direction(
            row=row, col=col, direction=Direction.EAST, room_dict=room_dict
        ):
            valid.append(Direction.EAST)

        if valid:
            random_dir: Direction = random.choice(valid)
            return random_dir

    # TODO in the future, make generate_path retrace it's steps if it has no empty rooms to go to next.
    # Maybe convert to BSP generation later (if you have more time than you bargained for)
    def generate_path(self) -> dict[tuple[int, int], Room]:
        room_dict: dict[tuple[int, int], Room] = {}
        (ent_row, ent_col), (ex_row, ex_col) = self.entrance, self.exit

        entrance_room: Room = Room(
            surface=self.surface,
            grid_constant=self.grid_constant,
            row=ent_row,
            col=ent_col,
            room_type=RoomType.ENTRANCE,
        )
        exit_room: Room = Room(
            surface=self.surface, grid_constant=self.grid_constant, row=ex_row, col=ex_col, room_type=RoomType.EXIT
        )

        room_dict[entrance_room.get_loc()] = entrance_room

        current_row: int = ent_row
        current_col: int = ent_col

        movement_tracker: list[tuple[int, int]] = [(current_row, current_col)]
        movement_pointer: int = 0
        calculating: bool = True
        while calculating:
            next_dir: Direction | None = self.get_next_direction(
                current_row=current_row, current_col=current_col, room_dict=room_dict
            )
            if not next_dir:
                movement_pointer -= 1
                current_row, current_col = movement_tracker[movement_pointer]
                continue

            move_dir: tuple[int, int] = self.movement_dict[next_dir]

            next_row: int = current_row + move_dir[0]
            next_col: int = current_col + move_dir[1]

            current_room: Room = room_dict[(current_row, current_col)]
            current_room.add_door(door=next_dir)

            if (next_row, next_col) not in room_dict:
                if (next_row, next_col) == (ex_row, ex_col):
                    exit_room.add_door(door=self.door_connections_dict[next_dir])

                    calculating = False
                    continue

                new_room: Room = Room(
                    surface=self.surface,
                    grid_constant=self.grid_constant,
                    row=next_row,
                    col=next_col,
                    room_type=RoomType.NORMAL,
                )
                new_room.add_door(door=self.door_connections_dict[next_dir])

                room_dict[(next_row, next_col)] = new_room

            else:
                next_room: Room = room_dict[(next_row, next_col)]
                next_room.add_door(door=self.door_connections_dict[next_dir])

            # move pointer
            current_row = next_row
            current_col = next_col
            movement_tracker.append((current_row, current_col))
            movement_pointer += 1

        room_dict[exit_room.get_loc()] = exit_room
        return room_dict


class Floor:
    def __init__(
        self,
        surface: pygame.Surface,
        grid_constant: int,
        path: dict[tuple[int, int], Room],
        entrance: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant
        self.path: dict[tuple[int, int], Room] = path

        self.entrance: Room = self.path[entrance]
        self.exit: Room = self.path[exit]

    def update(self, camera_offset: tuple[float, float]):
        for room in self.path.values():
            room.start_x += camera_offset[0]  # I am only doing this in case I need to access room positions later
            room.start_y += camera_offset[1]
            room.update(camera_offset=camera_offset)

    def draw(self):
        for room in self.path.values():
            room.draw()


class RoomType(Enum):
    ENTRANCE = auto()
    NORMAL = auto()
    ENEMY = auto()
    PUZZLE = auto()
    EXIT = auto()


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


class Room:
    def __init__(
        self, surface: pygame.Surface, grid_constant: int, row: int, col: int, room_type: RoomType = RoomType.NORMAL
    ) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant
        self.row: int = row
        self.col: int = col
        self.room_type: RoomType = room_type

        self.tile_config: TileConfiguration = TileConfiguration(surface=self.surface, grid_constant=self.grid_constant)

        self.enabled: bool = True
        self.doors: set[Direction] = set()

        self.width: int = self.grid_constant * fl.ROOM_UNIT_SIZE
        self.height: int = self.grid_constant * fl.ROOM_UNIT_SIZE
        self.spacing: int = self.grid_constant * 2
        self.start_x: float = self.col * (self.spacing + self.width) + (self.surface.width - self.width) // 2
        self.start_y: float = self.row * (self.spacing + self.height) + (self.surface.height - self.height) // 2

        self.door_pos_dict: dict[Direction, tuple[int, int]] = {
            Direction.SOUTH: (self.start_x + ((self.width - self.grid_constant * 2) // 2), self.start_y + self.height),
            Direction.NORTH: (
                self.start_x + ((self.width - self.grid_constant * 2) // 2),
                self.start_y - self.grid_constant,
            ),
            Direction.WEST: (
                self.start_x - self.grid_constant,
                self.start_y + ((self.height - self.grid_constant * 2) // 2),
            ),
            Direction.EAST: (self.start_x + self.width, self.start_y + ((self.height - self.grid_constant * 2) // 2)),
        }

        self.tile_map: list[BaseTile] = self.set_floor()
        self.wall_map: list[BaseTile] = []
        self.door_map: list[BaseTile] = []

        self.tile_mesh: list[BaseTile] = self.tile_map + self.wall_map + self.door_map

    def refresh_tile_mesh(self):
        self.tile_mesh = self.tile_map + self.wall_map + self.door_map

    def add_door(self, door: Direction):
        self.doors.add(door)
        self.door_map = self.set_doors()
        self.wall_map = self.set_walls()
        self.refresh_tile_mesh()

    def get_loc(self) -> tuple[int, int]:
        return self.row, self.col

    def set_floor(self) -> list[BaseTile]:
        tiles: list[BaseTile] = []
        for row in range(fl.ROOM_UNIT_SIZE):
            for col in range(fl.ROOM_UNIT_SIZE):
                x: float = col * self.grid_constant + self.start_x
                y: float = row * self.grid_constant + self.start_y
                tiles.append(self.tile_config.create_tile(x=int(x), y=int(y), color=cp.DARK_GREEN))

        return tiles

    def set_doors(self) -> list[BaseTile]:
        doors: list[BaseTile] = []
        for door in self.doors:
            pos: tuple[int, int] = self.door_pos_dict[door]
            converted_x: float = pos[0]
            converted_y: float = pos[1]
            if door == Direction.EAST or door == Direction.WEST:
                doors.append(
                    self.tile_config.create_door(
                        w=self.grid_constant,
                        h=self.grid_constant * 2,
                        x=int(converted_x),
                        y=int(converted_y),
                        color=cp.GRAY,
                    )
                )

            else:
                doors.append(
                    self.tile_config.create_door(
                        w=self.grid_constant * 2,
                        h=self.grid_constant,
                        x=int(converted_x),
                        y=int(converted_y),
                        color=cp.GRAY,
                    )
                )

        return doors

    def get_door_bounds(self, door: BaseTile) -> pygame.Rect:
        margin: int = self.grid_constant // 3
        tl_pos: pygame.typing.Point = door.x_pos - margin, door.y_pos - margin
        wh_pos: pygame.typing.Point = self.grid_constant + margin * 2, self.grid_constant + margin * 2

        return pygame.Rect(tl_pos, wh_pos)

    def in_door_bounds(self, door: BaseTile, x: float, y: float) -> bool:
        bounding_rect: pygame.Rect = self.get_door_bounds(door=door)
        if x > bounding_rect.left and x < bounding_rect.right and y > bounding_rect.top and y < bounding_rect.bottom:
            return True

        else:
            return False

    def set_walls(self) -> list[BaseTile]:
        wall_tiles: list[BaseTile] = []
        base_x: float = self.start_x
        base_y: float = self.start_y - (self.grid_constant)

        for i in range(fl.ROOM_UNIT_SIZE):
            x: float = base_x + self.grid_constant * i
            y: float = base_y
            for door in self.door_map:
                if self.in_door_bounds(door=door, x=x, y=y):
                    break
            else:
                wall_tiles.append(self.tile_config.create_collide(x=int(x), y=int(y), color=cp.LIGHT_GREEN))

            for door in self.door_map:
                if self.in_door_bounds(door=door, x=x, y=y + self.height + self.grid_constant):
                    break

            else:
                wall_tiles.append(
                    self.tile_config.create_collide(
                        x=int(x), y=int(y + self.height + self.grid_constant), color=cp.LIGHT_GREEN
                    )
                )

        base_x: float = self.start_x - self.grid_constant
        base_y: float = self.start_y
        for j in range(fl.ROOM_UNIT_SIZE):
            x: float = base_x
            y: float = base_y + self.grid_constant * j
            for door in self.door_map:
                if self.in_door_bounds(door=door, x=x, y=y):
                    break

            else:
                wall_tiles.append(self.tile_config.create_collide(x=int(x), y=int(y), color=cp.LIGHT_GREEN))

            for door in self.door_map:
                if self.in_door_bounds(door=door, x=x + self.width + self.grid_constant, y=y):
                    break

            else:
                wall_tiles.append(
                    self.tile_config.create_collide(
                        x=int(x + self.width + self.grid_constant), y=int(y), color=cp.LIGHT_GREEN
                    )
                )

        return wall_tiles

    def update(self, camera_offset: tuple[float, float]):
        for tile in self.tile_mesh:
            tile.x_pos += camera_offset[0]
            tile.y_pos += camera_offset[1]

    def draw(self):
        for tile in self.tile_mesh:
            tile.draw()
