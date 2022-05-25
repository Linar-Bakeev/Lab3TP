import os
import json
import requests


def parseWidth_Longitude():

    # Читаем полученный ранее JSON-файл
    with open(os.path.join(f'{os.path.dirname(__file__)}', 'json/result.json'), 'r') as file:
        data = json.loads(file.read())

    # Получаем данные
    pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')

    longitude = pos[0]
    width = pos[1]

    return dict(longitude=longitude, width=width)


def to_json(city):
    token = 'd517f19c-d50a-4836-bb0b-223ff9d29670'
    url_geo = f'https://geocode-maps.yandex.ru/1.x/'

    # Если параметр в функцию не был передан, то выставляем значение по-умолчанию
    if not city:
        city = 'Ульяновск'


    # Формируем URL с параметрами для запроса
    url = url_geo + f'?apikey={token}&geocode={city}&format=json'

    try:
        # Делаем запрос
        response = requests.get(url)

        # Если приходит код с ошибкой, то вызываем Exception
        if response.status_code != 200:
            raise Exception(response.status_code)

    except Exception as err:
        return err

    else:
        # Формируем путь к папке с JSON-файлом
        json_dir = os.path.join(f'{os.path.dirname(__file__)}', 'json')

        # Сохраняем JSON-файл
        with open(f'{json_dir}/result.json', 'w') as file:
            file.write(response.text)

    return response.status_code


def to_map(longitude, width):

    token = 'd517f19c-d50a-4836-bb0b-223ff9d29670'
    url_static = 'https://static-maps.yandex.ru/1.x/'

    # Если параметр в функцию не был передан, то выставляем значение по-умолчанию
    if not longitude or not width:
        longitude = '48.384824'
        width = '54.151718'

    # Параметры изображения, которые передаем в URL
    spn = [0.3, 0.3]
    size_w = 450
    size_h = 450
    scheme_l = 'map'
    url = url_static + f'?apikey={token}&ll={longitude},{width}&' \
                       f'spn={spn[0]},{spn[1]}&size={size_w},{size_h}&l={scheme_l}'

    try:
        # Делаем запрос
        response = requests.get(url)

        # Если приходит код с ошибкой, то вызываем Exception
        if response.status_code != 200:
            raise Exception(response.status_code)

    except Exception as err:
        return err

    else:
        # Формируем путь к папке с изображениями карт
        img_directory = os.path.join(f'{os.path.dirname(__file__)}', 'map')

        # Сохраняем изображение
        with open(f'{img_directory}/map.jpg', 'wb') as file:
            file.write(response.content)

    return response.status_code


def main():
    print('Введите адрес: ', end='')
    city = input()
    print()

    # Получаем json
    city_info = to_json(city)

    if city_info == 200:

        # Парсим ранее полученный json
        pos = parseWidth_Longitude()

        # Выведем в консоль долготу и широту
        print(f'Долгота: {pos["longitude"]}')
        print(f'Широта: {pos["width"]}')

        # Получаем карту
        city_map = to_map(pos['longitude'], pos['width'])

        if city_map != 200:
            print('Не удалось получить изображение!')

    else:
        print('Информация о городе не была получена!')


if __name__ == '__main__':
    main()

