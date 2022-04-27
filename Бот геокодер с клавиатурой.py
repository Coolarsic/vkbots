import json
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import os
import sys
import requests
coords = ''
layer = ''
location = ''
token = TOKEN

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def upload_photo(session, ph, id):

    with open('png.png', 'wb') as f:
        f.write(ph)
        f.close()
    upload = vk_api.VkUpload(session)
    upload_image = upload.photo_messages(photos='png.png')[0]
    print(upload_image)
    print(id)
    session.messages.send(user_id=id,
                              message=f"Это {location}. Что вы еще хотите увидеть?",
                              random_id=random.randint(0, 2 ** 64),
                          attachment='photo{}_{}'.format(str(upload_image['owner_id']), str(upload_image['id'])))


def send_location(bot_session, user_id):
    global location, layer, coords
    coords = list(map(str, coords))
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(coords)}&spn=0.005,0.005&l={layer}"
    image = requests.get(map_request).content
    upload_photo(bot_session, image, user_id)
    location = ''
    coords = ''
    layer = ''


def get_coords(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)

def geocode(address):

    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_request, params=geocoder_params)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {response.status_code} ({response.reason})""")

    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def main():
    global location, layer, coords
    bot_session = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(bot_session, '211020313')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if location == '' and layer == '':
                print(event.obj.message)
                addr = event.obj.message["text"]
                coords = get_coords(addr)
                location = event.obj.message['text']
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("Спутник", VkKeyboardColor.PRIMARY)
                keyboard.add_button("Гибрид", VkKeyboardColor.SECONDARY)
                keyboard.add_button("Схема", VkKeyboardColor.NEGATIVE)
                vk = bot_session.get_api()
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 random_id=random.randint(0, 2 ** 64),
                                 message="Выберите тип карты: ",
                                 keyboard=keyboard.get_keyboard())
                for event1 in longpoll.listen():
                    if event1.type == VkBotEventType.MESSAGE_NEW:
                        if event1.obj.message['text'] == "Спутник":
                            layer = 'sat'
                            send_location(vk, event.obj.message['from_id'])
                            break
                        elif event1.obj.message['text'] == "Схема":
                            layer = 'map'
                            send_location(vk, event.obj.message['from_id'])
                            break
                        elif event1.obj.message['text'] == "Гибрид":
                            layer = 'sat,skl'
                            send_location(vk, event.obj.message['from_id'])
                            break
                        else:
                             vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message="Просто нажмите кнопку =)")


if __name__ == '__main__':
    main()