import time
import random

from typing import NamedTuple

from .road import Road


class Interval(NamedTuple):
    start: float
    end: float


class Experiment:
    """docstring"""

    def __init__(self, len_road: float, interval_speed_car: Interval,
                 interval_low_speed_car: Interval, interval_time_low_speed_car: Interval,
                 interval_frequency_appearance_cars: Interval, interval_duration_low_speed_car: Interval,
                 time_to_resolve_accident, time_scaling, need_random_slow, lane_to_slow=None):
        self.__time = time.time()
        self.__interval_speed_car = interval_speed_car
        self.__interval_low_speed_car = interval_low_speed_car
        self.__interval_time_low_speed_car = interval_time_low_speed_car
        self.__interval_duration_low_speed_car = interval_duration_low_speed_car
        self.__interval_frequency_appearance_cars = interval_frequency_appearance_cars
        self.__roads = [Road(len_road, 1, time_to_resolve_accident)]
        self.__time_scaling = time_scaling
        self.__lane_to_slow = lane_to_slow
        self.__need_random_slow = need_random_slow

    # Запуск эксперимента
    def tick(self):
        current_time = time.time()
        last_time = self.__time
        for road in self.__roads:
            road.update(last_time, current_time, self.__time_scaling, self.__lane_to_slow, self, self.__need_random_slow)

        self.__time = current_time

    def update_need_random_slow(self, need_random_slow: bool):
        self.__need_random_slow = need_random_slow

    def update_lane_to_slow(self, lane_to_slow):
        self.__lane_to_slow = lane_to_slow

    # Получение времени создания новой машины
    def get_time_to_creat_new_car(self, current_time):
        return current_time + random.uniform(
            self.__interval_frequency_appearance_cars.start,
            self.__interval_frequency_appearance_cars.end
        ) / self.__time_scaling

    # Получение времени, когда машина должна замедлиться искусственно
    def get_time_to_slow_down_car(self, current_time):
        return current_time + random.uniform(
            self.__interval_time_low_speed_car.start,
            self.__interval_time_low_speed_car.end
        ) / self.__time_scaling

    def get_duration_slow_down_car(self):
        return random.uniform(
            self.__interval_duration_low_speed_car.start,
            self.__interval_duration_low_speed_car.end
        ) / self.__time_scaling

    def get_speed_car(self):
        return random.uniform(
            self.__interval_speed_car.start,
            self.__interval_speed_car.end
        )

    def get_low_speed_for_car(self):
        return random.uniform(
            self.__interval_low_speed_car.start,
            self.__interval_low_speed_car.end
        )

    def update_time_scaling(self, new_time_scaling):
        self.__time_scaling = new_time_scaling

    def get_time_scaling(self):
        return self.__time_scaling

    def update_time_to_resolve_accident(self, new_time_to_resolve_accident):
        for road in self.__roads:
            road.update_time_to_resolve_accident(new_time_to_resolve_accident)

    def get_params_for_drawing(self):
        cars = self.__roads[0].get_cars_to_make_picture()
        len_road = self.__roads[0].get_len_road()

        return cars, len_road, self.__lane_to_slow
