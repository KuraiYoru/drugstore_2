import requests
import json


def searching(place):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": place,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()


    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    with open('smth.json', 'w', encoding='utf-8') as f:
        json.dump(toponym['boundedBy']['Envelope'], f, indent=4, ensure_ascii=False)
    # Координаты центра топонима:
    dist = toponym['boundedBy']['Envelope']
    lower_x, lower_y = map(float, dist['lowerCorner'].split())
    upper_x, upper_y = map(float, dist['upperCorner'].split())
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    delta = list(map(str, [abs(lower_x - upper_x), abs(upper_y - lower_y)]))

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join(delta),
        "l": "map",

    }
    return map_params
