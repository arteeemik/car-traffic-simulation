import time

import PySimpleGUI as sg

from classes.experiment import Experiment
from classes.experiment import Interval

import draw

# ---------------------------------------------------------------------- #
#                           Constants                                    #
# ---------------------------------------------------------------------- #

TEXT_NAME_LENGTH_LANE = "_LENGTH_LANE_"
TEXT_NAME_SPEED_START = "_SPEED_START_"
TEXT_NAME_SPEED_END = "_SPEED_END_"
TEXT_NAME_TIME_LOW_SPEED_START = "_TIME_LOW_SPEED_START_"
TEXT_NAME_TIME_LOW_SPEED_END = "_TIME_LOW_SPEED_END_"
TEXT_NAME_DURATION_LOW_SPEED_START = "_TIME_DURATION_SPEED_START_"
TEXT_NAME_DURATION_LOW_SPEED_END = "_TIME_DURATION_SPEED_END_"
TEXT_NAME_LOW_SPEED_START = "_LOW_SPEED_START_"
TEXT_NAME_LOW_SPEED_END = "_LOW_SPEED_END_"
TEXT_NAME_PERIODICITY_START = "_PERIODICITY_START_"
TEXT_NAME_PERIODICITY_END = "_PERIODICITY_END_"
IMAGE_NAME_LANE = "_PICTURE_"
TIME_SCALING = "_TIME_SCALING_"
TIME_TO_RESOLVE_ASSIDENT = "_TIME_TO_RESOLVE_ASSIDENT_"
TEXT_NAME_LANE_SLOW_SPEED = "_LANE_SLOW_SPEED_"

TEXT_NAME_GLOBAL_TIME_EXPERIMENT = "_TIME_"

BUTTON_NAME_START = "_START_"
BUTTON_NAME_END = "_END_"
BUTTON_NAME_EXIT = "_EXIT_"
BUTTON_NAME_UPDATE_TIME_SCALING = "_UPDATE_SCALING_"
BUTTON_NAME_UPDATE_TIME_ACCIDENT = "_TIME_ACCIDENT_"
BUTTON_NAME_UPDATE_LINE_LOW_SPEED = "_LINE_LOW_SPEED_"

BUTTON_NAME_ADD_LINE_LOW_SPEED = "_ADD_LINE_LOW_SPEED_"
BUTTON_NAME_DELETE_LINE_LOW_SPEED = "_DELETE_LINE_LOW_SPEED_"

CHECK_BOX_NAME_RANDOM_SLOW_DAWN = "_NEED_RANDOM_SLOW_DAWN_"

# ---------------------------------------------------------------------- #
#                           LAYOUT                                       #
# ---------------------------------------------------------------------- #


LAYOUT = [
    [sg.Text('Задайте необходимые параметры эксперимента')],

    [sg.HSeparator()],

    [sg.Text('Длина полосы (км):', size=(55, 1)), sg.InputText('1', size=(10, 1), key=TEXT_NAME_LENGTH_LANE)],

    [sg.Text('Скорость автомобилей от (км/ч):', size=(55, 1)), sg.InputText('60', size=(10, 1), key=TEXT_NAME_SPEED_START),
     sg.Text(text='до(км/ч):', size=(8, 1)), sg.InputText('150', size=(10, 1), key=TEXT_NAME_SPEED_END)],

    [sg.Text('Частота искусственного замедления автомобилей от (сек.):', size=(55, 1)), sg.InputText('2', size=(10, 1), key=TEXT_NAME_TIME_LOW_SPEED_START),
     sg.Text(text='до (сек.):', size=(8, 1)), sg.InputText('4', size=(10, 1), key=TEXT_NAME_TIME_LOW_SPEED_END)],

    [sg.Text('Время движения автомобилей с уменьшенной скоростью от (сек.):', size=(55, 1)), sg.InputText('3', size=(10, 1), key=TEXT_NAME_DURATION_LOW_SPEED_START),
     sg.Text(text='до (сек.):', size=(8, 1)), sg.InputText('10', size=(10, 1), key=TEXT_NAME_DURATION_LOW_SPEED_END)],

    [sg.Text('Уменьшенная скорость автомобилей от (км/ч):', size=(55, 1)),
     sg.InputText('30', size=(10, 1), key=TEXT_NAME_LOW_SPEED_START),
     sg.Text(text='до (км/ч):', size=(8, 1)), sg.InputText('60', size=(10, 1), key=TEXT_NAME_LOW_SPEED_END)],

    [sg.Text('Частота появиления автомобилей от (сек.):', size=(55, 1)),
     sg.InputText('3', size=(10, 1), key=TEXT_NAME_PERIODICITY_START),
     sg.Text(text='до (сек.):', size=(8, 1)), sg.InputText('7', size=(10, 1), key=TEXT_NAME_PERIODICITY_END)],

    [sg.Text('Необходимое время для разрешения аварии(сек.):', size=(55, 1)), sg.InputText('5', size=(10, 1), key=TIME_TO_RESOLVE_ASSIDENT),
     sg.Button('Обновить поле', key=BUTTON_NAME_UPDATE_TIME_ACCIDENT)],

    [sg.Text('Масштабирование времени:', size=(55, 1)), sg.InputText('3', size=(10, 1), key=TIME_SCALING),
     sg.Button('Обновить поле', key=BUTTON_NAME_UPDATE_TIME_SCALING)],

    [sg.Text("Место на полосе с искусственным замедлением скорости:", size=(55, 1), key=TEXT_NAME_LANE_SLOW_SPEED, visible=False),
     sg.InputText('0.5', visible=False, key="KEY_INPUT_LANE", size=(10, 1)),
     sg.Button('Обновить поле', key=BUTTON_NAME_UPDATE_LINE_LOW_SPEED, visible=False),
     sg.Button('Добавить место на полосе с искусственным замедлением скорости', key=BUTTON_NAME_ADD_LINE_LOW_SPEED),
     sg.Button('Удалить место на полосе с искусственным замедлением скорости', key=BUTTON_NAME_DELETE_LINE_LOW_SPEED, visible=False)],

    [sg.Checkbox('Вкл/выкл случайного замедления автомобилей:', size=(55, 1), default=True, key=CHECK_BOX_NAME_RANDOM_SLOW_DAWN)],

    [
        sg.Button('Старт', key=BUTTON_NAME_START),
        sg.Button('Стоп', key=BUTTON_NAME_END, visible=False, size=(4, 2), button_color='red', pad=(560, 15)),
        sg.Button('', key=TEXT_NAME_GLOBAL_TIME_EXPERIMENT, visible=False),
    ],
    [
        sg.Image(
            filename='pictures/start_polosa.png',
            size=(1300, 100),
            key=IMAGE_NAME_LANE,
            visible=False,
        )
    ],
    [sg.Exit('Выйти', key=BUTTON_NAME_EXIT)]
]


# ---------------------------------------------------------------------- #
#                           MAIN                                         #
# ---------------------------------------------------------------------- #

def check_input_params(values_from_window: dict) -> bool:
    try:
        for value in values_from_window.values():
            float(value)
    except Exception:
        sg.Popup("Параметры должны быть целочисленными или дробными!")
        return False

    for value in values_from_window.values():
        if float(value) < 0:
            sg.Popup("Параметры должны быть неотрицательными!")
            return False

    if (float(values_from_window[TEXT_NAME_SPEED_START]) >
            float(values_from_window[TEXT_NAME_SPEED_END])):
        sg.Popup("Диапазон начальных скоростей автомобилей неправильный!")
        return False

    if (float(values_from_window[TEXT_NAME_TIME_LOW_SPEED_START]) >
            float(values_from_window[TEXT_NAME_TIME_LOW_SPEED_END])):
        sg.Popup("Диапазон Частоты искусственного замедления автомобилей неправильный!")
        return False

    if (float(values_from_window[TEXT_NAME_DURATION_LOW_SPEED_START]) >
            float(values_from_window[TEXT_NAME_DURATION_LOW_SPEED_END])):
        sg.Popup("Диапазон времени движения автомобилей с уменьшенной скоростью неправильный!")
        return False

    if (float(values_from_window[TEXT_NAME_LOW_SPEED_START]) >
            float(values_from_window[TEXT_NAME_LOW_SPEED_END])):
        sg.Popup("Диапазон уменьшенных скоростей автомобилей неправильный!")
        return False

    if (float(values_from_window[TEXT_NAME_PERIODICITY_START]) >
            float(values_from_window[TEXT_NAME_PERIODICITY_END])):
        sg.Popup("Диапазон частоты появления автомобилей неправильный!")
        return False

    return True

visible_lane = False

class Input:
    def __init__(self, values):
        self.len_road = float(values[TEXT_NAME_LENGTH_LANE])
        self.interval_speed_car = Interval(
            float(values[TEXT_NAME_SPEED_START]),
            float(values[TEXT_NAME_SPEED_END]),
        )
        self.interval_low_speed_car = Interval(
            float(values[TEXT_NAME_LOW_SPEED_START]),
            float(values[TEXT_NAME_LOW_SPEED_END]),
        )
        self.interval_time_low_speed_car = Interval(
            float(values[TEXT_NAME_TIME_LOW_SPEED_START]),
            float(values[TEXT_NAME_TIME_LOW_SPEED_END]),
        )
        self.interval_duration_low_speed_car = Interval(
            float(values[TEXT_NAME_DURATION_LOW_SPEED_START]),
            float(values[TEXT_NAME_DURATION_LOW_SPEED_END]),
        )
        self.interval_frequency_appearance_cars = Interval(
            float(values[TEXT_NAME_PERIODICITY_START]),
            float(values[TEXT_NAME_PERIODICITY_END]),
        )
        self.time_to_resolve_accident = float(values[TIME_TO_RESOLVE_ASSIDENT])
        self.time_scaling = float(values[TIME_SCALING])
        if visible_lane:
            self.lane_to_slow = float(values["KEY_INPUT_LANE"])
        else:
            self.lane_to_slow = None

        self.need_random_slow = values[CHECK_BOX_NAME_RANDOM_SLOW_DAWN]


if __name__ == '__main__':
    draw.preprocessing()

    window = sg.Window('Симуляция движения автомобилей на автостраде', layout=LAYOUT).Finalize()
    window.Maximize()
    experiment = None

    past_time = 0
    last_time = None
    while True:
        event, values = window.Read(timeout_key="NO_ACTION", timeout=20)

        if event == sg.WIN_CLOSED or event == BUTTON_NAME_EXIT:
            break

        if event == BUTTON_NAME_END:
            experiment = None
            window[BUTTON_NAME_END].update(visible=False)
            window[TEXT_NAME_GLOBAL_TIME_EXPERIMENT].update(visible=False)

        if experiment:
            experiment.update_need_random_slow(values[CHECK_BOX_NAME_RANDOM_SLOW_DAWN])

        if event == BUTTON_NAME_UPDATE_TIME_SCALING:
            if experiment:
                try:
                    experiment.update_time_scaling(float(values[TIME_SCALING]))
                except Exception:
                    sg.Popup("Параметры должны быть целочисленными или дробными!")

        if event == BUTTON_NAME_UPDATE_TIME_ACCIDENT:
            if experiment:
                try:
                    experiment.update_time_to_resolve_accident(float(values[TIME_TO_RESOLVE_ASSIDENT]))
                except Exception:
                    sg.Popup("Параметры должны быть целочисленными или дробными!")

        if event == BUTTON_NAME_UPDATE_LINE_LOW_SPEED:
            if experiment:
                try:
                    lane_slow_speed = float(values["KEY_INPUT_LANE"])
                    experiment.update_lane_to_slow(float(lane_slow_speed))
                except Exception:
                    sg.Popup("Параметры должны быть целочисленными или дробными!")

        if event == BUTTON_NAME_ADD_LINE_LOW_SPEED:
            visible_lane = True
            window[BUTTON_NAME_ADD_LINE_LOW_SPEED].update(visible=False)
            window[TEXT_NAME_LANE_SLOW_SPEED].update(visible=True)
            window["KEY_INPUT_LANE"].update(visible=True),
            window[BUTTON_NAME_UPDATE_LINE_LOW_SPEED].update(visible=True)
            window[BUTTON_NAME_DELETE_LINE_LOW_SPEED].update(visible=True)
            if experiment:
                try:
                    lane_slow_speed = values["KEY_INPUT_LANE"]
                    experiment.update_lane_to_slow(float(lane_slow_speed))
                except Exception:
                    sg.Popup("Параметры должны быть целочисленными или дробными!")

        if event == BUTTON_NAME_DELETE_LINE_LOW_SPEED:
            visible_lane = False
            window[TEXT_NAME_LANE_SLOW_SPEED].update(visible=False)
            window["KEY_INPUT_LANE"].update(visible=False),
            window[BUTTON_NAME_UPDATE_LINE_LOW_SPEED].update(visible=False)
            window[BUTTON_NAME_DELETE_LINE_LOW_SPEED].update(visible=False)
            window[BUTTON_NAME_ADD_LINE_LOW_SPEED].update(visible=True)
            if experiment:
                experiment.update_lane_to_slow(None)

        if event == BUTTON_NAME_START:
            past_time = 0
            last_time = time.time()
            if check_input_params(values):
                input_params = Input(values)

                experiment = Experiment(
                    len_road=input_params.len_road,
                    interval_speed_car=input_params.interval_speed_car,
                    interval_low_speed_car=input_params.interval_low_speed_car,
                    interval_time_low_speed_car=input_params.interval_time_low_speed_car,
                    interval_frequency_appearance_cars=input_params.interval_frequency_appearance_cars,
                    interval_duration_low_speed_car=input_params.interval_duration_low_speed_car,
                    time_to_resolve_accident=input_params.time_to_resolve_accident,
                    time_scaling=input_params.time_scaling,
                    lane_to_slow=input_params.lane_to_slow,
                    need_random_slow=input_params.need_random_slow,
                )

                window[BUTTON_NAME_END].update(visible=True)
                window[TEXT_NAME_GLOBAL_TIME_EXPERIMENT].update(str(0), visible=True)

        if experiment:
            diff_time = (time.time() - last_time) * experiment.get_time_scaling()
            past_time += diff_time
            last_time = time.time()
            window[TEXT_NAME_GLOBAL_TIME_EXPERIMENT].update("Прошедшее время: " + "{0:.0f}".format(past_time))
            for i in range(50):
                experiment.tick()
                draw.draw_current_state(experiment, window)

    window.Close()
