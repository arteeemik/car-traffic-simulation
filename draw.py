import copy

from PIL import Image as image
from PIL import ImageDraw


IMAGE_NAME_LANE = "_PICTURE_"

IMAGE_BLANK_POLOSA = image.open('pictures/blang_polosa.jpeg').resize((1300, 100), image.ANTIALIAS)
IMAGE_CAR_RED = image.open('pictures/car_resize_2.png')
IMAGE_CAR_BLUE = image.open('pictures/car_resize_1.png')
IMAGE_CAR_GREEN = image.open('pictures/car_resize_3.png')


def preprocessing():
    image.open('pictures/car_1.png').resize((60, 60), image.ANTIALIAS).save('pictures/car_resize_1.png', format='png')
    image.open('pictures/car_2.png').resize((60, 60), image.ANTIALIAS).save('pictures/car_resize_2.png', format='png')
    image.open('pictures/car_3.jpg').resize((60, 60), image.ANTIALIAS).save('pictures/car_resize_3.png', format='png')


def draw_current_state(experiment, window):
    cars, len_road, lane_to_slow = experiment.get_params_for_drawing()
    polosa = copy.deepcopy(IMAGE_BLANK_POLOSA)
    draw_text = ImageDraw.Draw(polosa)
    for car in cars:
        car_image = IMAGE_CAR_GREEN
        if car.is_car_in_accident():
            car_image = IMAGE_CAR_RED
        elif car.is_car_slow_dawn():
            car_image = IMAGE_CAR_BLUE

        start_pic = int(1300 * car.get_current_position() / len_road)
        draw_text.text(
            (start_pic, 10),
            "{0:.1f}".format(car.get_current_speed()),
            fill=('#1C0606')
        )
        polosa.paste(car_image, (start_pic, 20))

    if lane_to_slow:
        draw_text.line([(1300 * lane_to_slow / len_road, 0), (1300 * lane_to_slow / len_road, 200)],
                       fill="red", width=0)
    polosa.save('pictures/my_new_test.png', format='png')

    window[IMAGE_NAME_LANE].update(filename='pictures/my_new_test.png', size=(1300, 100), visible=True)
    window.Refresh()
