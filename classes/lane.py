import random

from .car import Car


class Lane:
    """Класс Car - класс автомобиля

    Attributes
    ----------
    len_road : float
        Длина дороги
    cars : List[Car]
        Список автомобилей на этой полосе
    need_time_to_resolve_accident : float
        Время необходимое для разрешения аварии на полосе
    time_to_create_new_car : float
        Время для создания нового автомобиля
    time_to_slow_dawn : float
        Время, когда машина случайная должна искусственного замедлиться

    Methods
    -------
    update(last_time: float, current_time: float, experiment, body_length: float, time_scaling: float, lane_to_slow: float, need_random_slow: bool)
        Обновляет текущее состояние полосы в определенный промежуток времени

    __is_enough_time_to_clean_up_car(current_time, time_accident, time_scaling)
        Возвращает true/false в зависимости от того, достаточно ли прошло времени, чтобы удалить машины с полосы

    __try_create_car(current_time, experiment, body_length)
        Попытаться добавить новую машины на полосу

    __updated_cars_created_time(current_time, experiment)
        Обновить время создания новой машины на полосе

    __remove_cars(numbers_of_cars_to_delete)
        Удалить машины с полосы

    __update_accidents(current_time)
        Обновления состояния всех аварий, которые произошли на этой полосе

    __get_position_and_speed_next_car(current_position)
        Получение текущей позиции и скорости автомобиля, который идет после позиции current_position

    get_cars_to_make_picture()
        Получение автомобилей на этой полосе для модуля отрисовки

    update_time_to_resolve_accident(new_time_to_resolve_accident)
        Обновление времени, которое необходимо для разрешения аварий на этой полосе

    """

    def __init__(self, len_road: float, need_time_to_resolve_accident: float):
        self.len_road = len_road
        self.cars = []
        self.need_time_to_resolve_accident = need_time_to_resolve_accident
        self.time_to_create_new_car = None
        self.time_to_slow_dawn = None

    # Обновление текущего состояния полосы
    def update(self, last_time: float, current_time: float, experiment, body_length: float, time_scaling: float, lane_to_slow: float, need_random_slow: bool):
        if need_random_slow and self.time_to_slow_dawn is None:
            self.time_to_slow_dawn = experiment.get_time_to_slow_down_car(current_time)

        number_of_car_to_slow = None
        if self.time_to_slow_dawn is not None and self.time_to_slow_dawn <= current_time:
            self.time_to_slow_dawn = None
            number_of_car_to_slow = random.randint(0, len(self.cars))

        numbers_of_cars_to_delete = set()
        for num_car, car in enumerate(self.cars):
            if car.is_car_in_accident():
                if self.__is_enough_time_to_clean_up_car(current_time, car.get_time_accident(), time_scaling):
                    numbers_of_cars_to_delete.add(num_car)
            else:
                if car.is_car_slow_dawn():
                    time_to_end_low_speed = car.get_time_slow_speed()
                    if time_to_end_low_speed <= current_time:
                        car.make_init_speed()

                if lane_to_slow and car.get_current_position() > lane_to_slow and not car.is_slow_with_line():
                    low_speed = experiment.get_low_speed_for_car()
                    time_to_end_low_speed = current_time + experiment.get_duration_slow_down_car()
                    car.make_slow_with_line(low_speed, time_to_end_low_speed)

                elif number_of_car_to_slow is not None and num_car >= number_of_car_to_slow:
                    low_speed = experiment.get_low_speed_for_car()
                    time_to_end_low_speed = current_time + experiment.get_duration_slow_down_car()
                    car.slow_dawn(low_speed, time_to_end_low_speed)
                    number_of_car_to_slow = None

                current_position_next_car, next_speed_car = self.__get_position_and_speed_next_car(car.get_current_position())
                car.update(last_time, current_time, time_scaling, current_position_next_car, next_speed_car)
                if car.get_current_position() >= self.len_road:
                    numbers_of_cars_to_delete.add(num_car)

        self.__updated_cars_created_time(current_time, experiment)

        self.__try_create_car(current_time, experiment, body_length)

        self.__remove_cars(numbers_of_cars_to_delete)

        self.__update_accidents(current_time)

    # Проверка на то, что времени после аварии достаточно прошло, чтобы убрать машины с полосы
    def __is_enough_time_to_clean_up_car(self, current_time, time_accident, time_scaling):
        if current_time - time_accident >= self.need_time_to_resolve_accident / time_scaling:
            return True
        return False

    def __try_create_car(self, current_time, experiment, body_length):
        if self.time_to_create_new_car <= current_time:
            min_current_position_of_exists_cars = None

            for car in self.cars:
                current_postiotion = car.get_current_position()
                if (min_current_position_of_exists_cars is None
                        or min_current_position_of_exists_cars > current_postiotion):
                    min_current_position_of_exists_cars = current_postiotion
            if min_current_position_of_exists_cars is not None and min_current_position_of_exists_cars < 0:
                return

            self.time_to_create_new_car = None
            init_speed_of_car = experiment.get_speed_car()
            self.cars.append(Car(init_speed_of_car, body_length))

    def __updated_cars_created_time(self, current_time, experiment):
        if self.time_to_create_new_car is None:
            self.time_to_create_new_car = experiment.get_time_to_creat_new_car(current_time)

    def __remove_cars(self, numbers_of_cars_to_delete):
        updated_cars = []
        for num_car, car in enumerate(self.cars):
            if num_car not in numbers_of_cars_to_delete:
                updated_cars.append(car)
        self.cars = updated_cars

    def __update_accidents(self, current_time):
        # позиция текущая, номер машины, длина корпуса
        cars_positions: [(float, int, float)] = []
        for num_car, car in enumerate(self.cars):
            cars_positions.append((car.get_current_position(), num_car, car.get_body_length()))

        cars_in_accidents = []
        sorted_cars_positions = sorted(cars_positions)
        len_sorted_cars_positions = len(sorted_cars_positions)
        for num, (current_position, num_car, body_length) in enumerate(sorted_cars_positions):
            if num + 1 != len_sorted_cars_positions:
                next_current_position_car = sorted_cars_positions[num + 1][0]
                if next_current_position_car <= current_position + body_length:
                    cars_in_accidents.append(num_car)
                    cars_in_accidents.append(sorted_cars_positions[num + 1][1])

        for num_car in cars_in_accidents:
            if not self.cars[num_car].is_car_in_accident():
                self.cars[num_car].make_accident(current_time)

    def __get_position_and_speed_next_car(self, current_position):
        nearest_position = None
        speed = None
        for car in self.cars:
            position = car.get_current_position()
            car_speed = car.get_current_speed()
            if position > current_position:
                if nearest_position is None:
                    nearest_position = position
                    speed = car_speed
                else:
                    if position < nearest_position:
                        nearest_position = position
                        speed = car_speed
        return nearest_position, speed

    def get_cars_to_make_picture(self):
        return self.cars

    def update_time_to_resolve_accident(self, new_time_to_resolve_accident):
        self.need_time_to_resolve_accident = new_time_to_resolve_accident
