import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
token = TOKEN


def auth():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def main():
    vk_session = vk_api.VkApi(login=LOGIN, password=PASSWORD, auth_handler=auth)
    vk_session.auth(token_only=True)
    bot_session = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(bot_session, '{group_id}')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            bot = bot_session.get_api()
            photos = vk.photos.get(group_id='211020313', album_id='285252237')
            ln = len(photos['items'])
            rnd = random.randint(0, ln - 1)
            id = photos['items'][rnd]['id']
            owner_id = photos['items'][rnd]['owner_id']
            attachment = f'photo{owner_id}_{id}'
            bot.messages.send(user_id=event.obj.message['from_id'], random_id=random.randint(0, 2 ** 64), attachment=attachment)


if __name__ == '__main__':
    main()