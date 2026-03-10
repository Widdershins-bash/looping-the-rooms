from system.constants import Camera as cm


class Camera:
    def __init__(self, player_y: float, grid_constant: int) -> None:
        self.initial_y: float = player_y
        self.grid_constant: int = grid_constant

        self.y_offset: float = 0

    def get_offset(self, new_player_y: float, delta_time: float) -> float:
        easing_speed: float = delta_time * cm.EASING_MULTIPLIER

        self.y_offset = (new_player_y) * easing_speed
        return self.y_offset
