import json
import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт
from map import searching
import requests
from PIL import Image
import pygame
from distance import lonlat_distance

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

params = {
    'apikey':'40d1649f-0493-4b70-98ba-98533de7710b',
    'geocode': toponym_to_find,
    'format': 'json'
}

response = f"http://geocode-maps.yandex.ru/1.x/"
response = requests.get(response, params=params)

address_ll = ','.join(response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split())


search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    #...
    pass
json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]
with open('smth.json', 'w', encoding='utf-8') as f:
    json.dump(organization, f, indent=4, ensure_ascii=False)
time = organization['properties']['CompanyMetaData']['Hours']['text']

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
a = list(map(float, address_ll.split(',')))
b = list(map(float, org_point.split(',')))
# delta = "0.005"
# params = searching(toponym_to_find)
# params['pt'] = f"{params['ll']},pmwtm"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    # "ll": address_ll,
    # "spn": ",".join([delta, delta]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{0},pm2dgl".format(org_point) + f"~{address_ll},pmwtm"
}



map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

dist = round(lonlat_distance(a, b))
pygame.init()




map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

screen = pygame.display.set_mode((600, 550))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
font = pygame.font.Font(None, 30)
smth = f"distance: {dist} metres"
text = font.render(smth, True, (128, 64, 48))
screen.blit(text, (0, 450))
smth = f"address: {org_address}"
text = font.render(smth, True, (128, 64, 48))
screen.blit(text, (0, 470))
smth = f"name: {org_name}"
text = font.render(smth, True, (128, 64, 48))
screen.blit(text, (0, 490))
smth = f"time: {time}"
text = font.render(smth, True, (128, 64, 48))
screen.blit(text, (0, 510))

# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()