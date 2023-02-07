import requests
import os
import math
import pygame
from io import BytesIO
from PIL import Image


def get_coords(toponym_name, api_key):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": api_key,
        "geocode": toponym_name,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print('Ошибка получения координат')
        exit(3)
    json_resp = response.json()
    toponym = json_resp['response']["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll = ','.join(toponym["Point"]["pos"].split())
    envelope = toponym['boundedBy']['Envelope']
    l, d = envelope['lowerCorner'].split(' ')
    r, u = envelope['upperCorner'].split(' ')
    geo = [float(i) for i in [r, l, u, d]] + [tuple([float(i) for i in ll.split(',')])]
    return (ll, geo)


def get_spn(geo_1, geo_2):
    if not geo_2:
        r, l, u, d, ll = geo_1
        dx = (abs(r) - abs(l))
        dy = (abs(u) - abs(d))
        return f'{dx},{dy}'
    ll1 = geo_1[-1]
    ll2 = geo_2[-1]
    dx = abs(ll1[0] - ll2[0]) * 2
    dy = abs(ll1[1] - ll2[1]) * 2
    return f'{dx},{dy}'


def get_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    sy = abs(y2 - y1) * 111
    l_x = 111 * math.cos(math.radians(abs(y1 + y1) / 2))
    sx = l_x * abs(x2 - x1)
    return math.sqrt(sx ** 2 + sy ** 2)


def get_image(coords, type='map', add_point=None, geo_2=None):
    ll, geo_1 = coords
    spn = get_spn(geo_1, geo_2)
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": type,
        'pt': f'{ll},comma' if not add_point else f'{ll},comma~{add_point}'
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print('Ошибка получения изображения')
        exit(4)
    return response.content


def get_business(ll, request, api_key, lang="ru_RU"):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": api_key,
        "text": request,
        "lang": lang,
        "ll": ll,
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print('Ошибка поиска организации')
        exit(5)
    json_response = response.json()
    organization = json_response["features"][0]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    point = organization["geometry"]["coordinates"]
    try:
        time = organization["properties"]["CompanyMetaData"]['Hours']['text']
    except Exception:
        time = 'не указано'
    [[l, d], [r, u]] = json_response['properties']['ResponseMetaData']['SearchResponse']['boundedBy']
    geo = [float(i) for i in [r, l, u, d]] + [tuple([float(i) for i in point])]
    return (org_name, org_address, point, time, geo)


def save_image(name, content):
    im = Image.open(BytesIO(content))
    im.save(name)


def delete_image(name):
    os.remove(name)


def show_image(name, head='', content=None):
    pygame.init()
    if content:
        save_image(name, content)
    image = pygame.image.load(name)
    screen = pygame.display.set_mode(image.get_size())
    pygame.display.set_caption(head)
    screen.blit(image, (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    if content:
        delete_image(name)


API_KEY_GEOCODER = "40d1649f-0493-4b70-98ba-98533de7710b"
API_KEY_ORGANIZATIONS = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
