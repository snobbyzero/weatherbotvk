import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
import weather
from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    vk_session = vk_api.VkApi(
        token="ea79f27d6457615db0ec5f325aed9b12a89b7356c97f53831428944ebf37d45edc14acf3130b5c39fb224")
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    upload = VkUpload(vk_session)
    keyboard = VkKeyboard()
    keyboard.add_button("Сегодня")
    keyboard.add_button("Завтра")
    keyboard.add_line()
    keyboard.add_button("Сейчас")
    keyboard.add_button("На 5 дней")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if (
                str(event.text) == "Начать" or
                str(event.text).lower() == "инструкция"
            ):
                 vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="""
                        Краткая инструкция по работе с ботом:
                        1. Чтобы узнать сегодняшнюю погоду -- "сегодня"
                        2. Чтобы узнать завтрашнюю погоду -- "завтра"
                        3. Чтобы узнать погоду в данный момент -- "сейчас"
                        4. Чтобы узнать погоду на пять дней -- "на пять дней"
                        """,
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower() == "сегодня" or
                str(event.text).lower() == "погода сегодня"
            ):
                arr = weather.today_weather()
                attachments = []
                photo = upload.photo_messages(photos=arr[1])[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=arr[0],
                    attachment=",".join(attachments),
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower() == "завтра" or
                str(event.text).lower() == "погода завтра"
            ):
                arr = weather.tomorrow_weather()
                attachments = []
                photo = upload.photo_messages(photos=arr[1])[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=arr[0],
                    attachment=",".join(attachments),
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower() == "погода на пять дней" or
                str(event.text).lower() == "погода на 5 дней" or
                str(event.text).lower() == "на 5 дней" or
                str(event.text).lower() == "на пять дней"
            ):
                arr = weather.fiveday_weather()
                attachments = []
                photo = upload.photo_messages(photos=arr[1])[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=arr[0],
                    attachment=",".join(attachments),
                    keyboard = keyboard.get_keyboard()
                )
            elif (
                str(event.text).lower() == "сейчас" or
                str(event.text).lower() == "погода сейчас" or 
                str(event.text).lower() == "в данный момент" or
                str(event.text).lower() == "погода в данный момент"
            ):
                arr = weather.now_weather()
                attachments = []
                photo = upload.photo_messages(photos=arr[1])[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),                    
                    message=arr[0],
                    attachment=",".join(attachments),
                    keyboard = keyboard.get_keyboard()
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Я не знаю, что Вы от меня хотите",
                    keyboard = keyboard.get_keyboard()
                )
if __name__ == "__main__":
    app.run(debug=True)