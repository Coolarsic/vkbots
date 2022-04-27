import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
token = TOKEN
sl = {1: "Понедельник", 2: "Вторник", 3: "Среда", 4: "Четверг", 5: "Пятница", 6: "Суббота", 7: "Воскресенье"}


def main():
    bot_session = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(bot_session, '{group_id}')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            a = event.obj.message['text']
            vk = bot_session.get_api()
            try:
                date = datetime.datetime.strptime(a.replace('-', ''), '%Y%m%d')
                day = date.isoweekday()
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"{a} - это {sl[day]}",
                                 random_id=random.randint(0, 2 ** 64))
            except ValueError:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                message=f"Этот бот может сказать, какой день недели был в какую-либо дату. Просто введите её в формате YYYY-MM-DD.",
                                random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()