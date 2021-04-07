

class Car:
    """docstring"""

    def __init__(self, init_speed: float, body_length: float):
        self.speed = 0
        self.init_speed = init_speed
        self.low_speed = None
        self.time_to_end_low_speed = None
        self.current_position = -body_length
        self.body_length = body_length
        self.time_accident = None
        self.already_slow_with_line = False

    # Получение времени, когда машина попала в аварию
    def is_car_in_accident(self):
        return bool(self.time_accident)

    def is_car_slow_dawn(self):
        return bool(self.time_to_end_low_speed)

    def get_time_slow_speed(self):
        return self.time_to_end_low_speed

    def make_init_speed(self):
        self.time_to_end_low_speed = None

    def get_current_speed(self):
        return self.speed

    def get_time_accident(self):
        return self.time_accident

    def make_accident(self, current_time):
        self.time_accident = current_time

    # Обновление текущего состояния автомобиля
    def update(self, last_time, current_time, time_scaling, position_next_car=None, next_speed_car=None):
        if self.time_accident:
            self.__update_current_state_if_accident()
        elif self.time_to_end_low_speed:
            self.__update_current_state_if_low_speed(last_time, current_time, time_scaling, position_next_car, next_speed_car)
        else:
            self.__update_current_state(last_time, current_time, time_scaling, position_next_car, next_speed_car)

    def __update_current_state_if_accident(self):
        return

    def __update_current_state_if_low_speed(self, last_time, current_time, time_scaling, position_next_car=None, next_speed_car=None):
        if (
                position_next_car and position_next_car - 3 * self.body_length - 0.1 * self.body_length >=
                self.current_position >=
                position_next_car - 3 * self.body_length + 0.1 * self.body_length):
            new_speed = self.speed - self.speed * 0.05 * (current_time - last_time) * time_scaling
            if new_speed < next_speed_car:
                self.speed = next_speed_car
            else:
                self.speed = new_speed
        elif position_next_car and position_next_car - 3 * self.body_length <= self.current_position:
            self.speed = self.speed - self.speed * 0.05 * (current_time - last_time) * time_scaling
        else:
            if self.speed < self.low_speed:
                new_speed = self.low_speed + 0.1 * self.low_speed * (current_time - last_time) * time_scaling
                if new_speed > self.low_speed:
                    self.speed = self.low_speed
                else:
                    self.speed = new_speed
        self.current_position = self.current_position + self.speed * (current_time - last_time) * time_scaling / (60 * 60)

    def __update_current_state(self, last_time, current_time, time_scaling, position_next_car=None, next_speed_car=None):
        if not position_next_car:
            if self.speed < self.init_speed:
                new_speed = self.speed + self.init_speed * 0.1 * (current_time - last_time) * time_scaling
                if new_speed <= self.init_speed:
                    self.speed = new_speed
                else:
                    self.speed = self.init_speed
        elif (
                position_next_car - 3 * self.body_length - 0.1 * self.body_length >=
                self.current_position >=
                position_next_car - 3 * self.body_length + 0.1 * self.body_length):
            new_speed = self.speed - self.speed * 0.05 * (current_time - last_time) * time_scaling
            if new_speed < next_speed_car:
                self.speed = next_speed_car
            else:
                self.speed = new_speed
        elif position_next_car - 3 * self.body_length <= self.current_position:
            self.speed = self.speed - self.speed * 0.05 * (current_time - last_time) * time_scaling
        else:
            if self.speed < self.init_speed:
                new_speed = self.speed + self.init_speed * 0.05 * (current_time - last_time) * time_scaling
                if new_speed <= self.init_speed:
                    self.speed = new_speed
                else:
                    self.speed = self.init_speed

        self.current_position = self.current_position + self.speed * (current_time - last_time) * time_scaling / (60 * 60)

    # Замедлить искусственно скорость автомобиля
    def slow_dawn(self, need_slow_speed, time_to_end_low_speed):
        self.speed = need_slow_speed
        self.low_speed = need_slow_speed
        self.time_to_end_low_speed = time_to_end_low_speed

    def get_current_position(self):
        return self.current_position

    def get_body_length(self):
        return self.body_length

    def is_slow_with_line(self):
        return self.already_slow_with_line

    def make_slow_with_line(self, need_slow_speed, time_to_end_low_speed):
        self.already_slow_with_line = True
        self.speed = need_slow_speed
        self.low_speed = need_slow_speed
        self.time_to_end_low_speed = time_to_end_low_speed
