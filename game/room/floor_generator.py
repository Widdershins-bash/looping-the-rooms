import pygame
import random
from enum import Enum, auto
from system.constants import Main


class FloorManager:
    def __init__(self):

        self.floor_gen: FloorGenerator = FloorGenerator()
        self.floor_plan: dict[tuple[int, int], Room] = self.floor_gen.generate_path()

    def print_plan(self):
        print(self.floor_plan)
        print("\n\n" + str(len(self.floor_plan)))


class FloorGenerator:
    def __init__(self, rows: int = 4, columns: int = 4) -> None:
        self.rows: int = rows
        self.cols: int = columns

        self.movement_dict: dict[Direction, tuple[int, int]] = {
            Direction.SOUTH: (-1, 0),
            Direction.NORTH: (1, 0),
            Direction.WEST: (0, -1),
            Direction.EAST: (0, 1),
        }

        self.door_connections_dict: dict[Direction, Direction] = {
            Direction.SOUTH: Direction.NORTH,
            Direction.NORTH: Direction.SOUTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
        }

    def select_entrance_exit(self) -> tuple[int, int, int, int]:
        entrance_row: int = 0
        entrance_col: int = 0
        exit_row: int = self.rows - 1
        exit_col: int = self.cols - 1  # temp placeholders

        return entrance_row, entrance_col, exit_row, exit_col

    def get_valid_directions(self, current_row: int, current_col: int) -> list[Direction]:
        valid: list[Direction] = []
        row: int = current_row
        col: int = current_col

        if row - 1 >= 0:
            valid.append(Direction.SOUTH)

        if row + 1 < self.rows:
            valid.append(Direction.NORTH)

        if col - 1 >= 0:
            valid.append(Direction.WEST)

        if col + 1 < self.cols:
            valid.append(Direction.EAST)

        return valid

    # TODO in the future, make generate_path retrace it's steps if it has no empty rooms to go to next.
    def generate_path(self) -> dict[tuple[int, int], Room]:
        room_dict: dict[tuple[int, int], Room] = {}
        ent_row, ent_col, ex_row, ex_col = self.select_entrance_exit()

        entrance_room: Room = Room(row=ent_row, col=ent_col, room_type=RoomType.ENTRANCE)
        exit_room: Room = Room(row=ex_row, col=ex_col, room_type=RoomType.EXIT)

        room_dict[entrance_room.get_loc()] = entrance_room

        current_row: int = ent_row
        current_col: int = ent_col

        calculating: bool = True
        while calculating:
            valid_dirs: list[Direction] = self.get_valid_directions(current_row=current_row, current_col=current_col)
            random_dir: Direction = random.choice(valid_dirs)
            move_dir: tuple[int, int] = self.movement_dict[random_dir]

            next_row: int = current_row + move_dir[0]
            next_col: int = current_col + move_dir[1]

            if (next_row, next_col) not in room_dict:
                if (next_row, next_col) == (ex_row, ex_col):
                    calculating = False
                    continue

                room_dict[(current_row, current_col)].add_door(door=random_dir)

                new_room: Room = Room(row=next_row, col=next_col, room_type=RoomType.NORMAL)
                new_room.add_door(door=self.door_connections_dict[random_dir])

                room_dict[(next_row, next_col)] = new_room

            else:
                room_dict[(current_row, current_col)].add_door(door=random_dir)
                next_room: Room = room_dict[(next_row, next_col)]

                next_room.add_door(door=self.door_connections_dict[random_dir])

            # move pointer
            current_row = next_row
            current_col = next_col

        room_dict[exit_room.get_loc()] = exit_room
        return room_dict


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
    def __init__(self, row: int, col: int, room_type: RoomType = RoomType.NORMAL) -> None:
        self.row: int = row
        self.col: int = col
        self.room_type: RoomType = room_type

        self.size_point: tuple[int, int] = (Main.GRID_CONSTANT * 8, Main.GRID_CONSTANT * 8)
        self.enabled: bool = True
        self.doors: set[Direction] = set()

    def add_door(self, door: Direction):
        self.doors.add(door)

    def get_loc(self) -> tuple[int, int]:
        return self.row, self.col
