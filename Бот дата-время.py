import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
st = {"число", "дата", "время", "день"}


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, '{group_id}')
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if len(st & set(event.obj.message['text'].lower().split())) > 0:
                offset = datetime.timezone(datetime.timedelta(hours=1))
                moscow_time = datetime.datetime.now(offset)
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Дата: {moscow_time.date()}, время: {moscow_time.strftime('%H:%m:%S')} (по МСК)",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"Если хотите получить время и дату по МСК, то в вашем сообщении должны быть слова:"
                                     f" время, число, дата или день",
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()