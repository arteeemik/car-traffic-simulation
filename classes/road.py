from .lane import Lane


class Road:
    """docstring"""

    def __init__(self, len_road: float, cnt_lanes: int, need_time_to_resolve_accident: float):
        self.len_road = len_road
        self.lanes = [Lane(len_road, need_time_to_resolve_accident) for i in range(cnt_lanes)]

    # Обновление текущего состояния дороги
    def update(self, last_time: float, current_time: float, time_scaling: float, lane_to_slow: float, experiment, need_random_slow: bool):
        for lane in self.lanes:
            lane.update(last_time, current_time, experiment, 60.0 / 1300 * self.len_road, time_scaling, lane_to_slow, need_random_slow)

    def update_time_to_resolve_accident(self, new_time_to_resolve_accident):
        for lane in self.lanes:
            lane.update_time_to_resolve_accident(new_time_to_resolve_accident)

    def get_cars_to_make_picture(self):
        return self.lanes[0].get_cars_to_make_picture()

    def get_len_road(self):
        return self.len_road
