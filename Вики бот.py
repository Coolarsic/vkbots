import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import wikipedia


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, '{group_id}')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            vk.messages.send(user_id=event.obj.message['from_id'],
                            message=f"{wikipedia.summary(event.obj.message['text'])}",
                            random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()