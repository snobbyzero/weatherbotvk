import requests
from bs4 import BeautifulSoup
import datetime
import PIL.Image as Image

def now_weather():
    page = requests.get("http://api.openweathermap.org/data/2.5/weather?q=moscow&appid=baae14e4c755825f78434e0aea84846b&units=metric&lang=ru")
    info = page.json()
    return [(
        "~~Погода в Москве: " + info["weather"][0]["description"] + "\n" +
        "~~Температура: " + str(round(info["main"]["temp_min"])) + "-" + str(round(info["main"]["temp_max"])) + "°C\n" +
        "~~Давление: " + str(round(info["main"]["pressure"]*0.75)) +  " мм рт. ст." + "\n"
        "~~Влажность: " + str(info["main"]["humidity"]) + "%\n" + 
        "~~Ветер: " + get_wind(info["wind"]["speed"]) + ", " + str(info["wind"]["speed"]) + "м/с" #+ get_winddirection(info["wind"]["deg"])
    ), "icons/" + info["weather"][0]["icon"] + ".png"]

def today_weather():
    page = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=moscow&appid=baae14e4c755825f78434e0aea84846b&units=metric&lang=ru")
    info = page.json()
    arr = []
    result = []
    for el in info["list"]:
        date = str(el["dt_txt"]).split(" ")
        if date[0] == str(datetime.date.today()):
            if date[1] == "09:00:00":
                arr.append(el)
                result.append("УТРО\n")
            elif date[1] == "15:00:00":
                arr.append(el)
                result.append("ДЕНЬ\n")
            elif date[1] == "18:00:00":
                arr.append(el)
                result.append("ВЕЧЕР\n")
        elif date[0] == str(datetime.date.today() + datetime.timedelta(days=1)) and date[1] == "00:00:00":
            arr.append(el)
            result.append("НОЧЬ\n")
    image = Image.new("RGB", (50*len(result), 50))
    for i in range(len(arr)):
        img = Image.open("icons/" + arr[i]["weather"][0]["icon"] + ".png")
        image.paste(img, (i*50, 0))
    image.save("icons/temp.png")
    for i in range(len(arr)):
        result[i] += (
        "~~Погода в Москве: " + arr[i]["weather"][0]["description"] + "\n" +
        "~~Температура: " + str(round(arr[i]["main"]["temp_min"])) + "-" + str(round(arr[i]["main"]["temp_max"])) + "°C\n" +
        "~~Давление: " + str(round(arr[i]["main"]["pressure"]*0.75)) +  " мм рт. ст." + "\n"
        "~~Влажность: " + str(arr[i]["main"]["humidity"]) + "%\n" + 
        "~~Ветер: " + get_wind(arr[i]["wind"]["speed"]) + ", " + str(arr[i]["wind"]["speed"]) + "м/с , " + get_winddirection(arr[i]["wind"]["deg"])
        )
    result.append(
        "\nСредняя погода в течение дня:\n\n" + "".join(["------" + str(round((arr[i]["main"]["temp_min"]+arr[i]["main"]["temp_max"])/2)) + "°C" for i in range(len(arr))])
    )
    return ["\n".join(result), "icons/temp.png"]

def tomorrow_weather():
    page = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=moscow&appid=baae14e4c755825f78434e0aea84846b&units=metric&lang=ru")
    info = page.json()
    arr = []
    result = []
    for el in info["list"]:
        date = str(el["dt_txt"]).split(" ")
        if date[0] == str(datetime.date.today() + datetime.timedelta(days=1)):
            if date[1] == "09:00:00":
                arr.append(el)
                result.append("УТРО\n")
            elif date[1] == "15:00:00":
                arr.append(el)
                result.append("ДЕНЬ\n")
            elif date[1] == "18:00:00":
                arr.append(el)
                result.append("ВЕЧЕР\n")
        elif date[0] == str(datetime.date.today() + datetime.timedelta(days=2)) and date[1] == "00:00:00":
            arr.append(el)
            result.append("НОЧЬ\n")
    image = Image.new("RGB", (50*len(result), 50))
    for i in range(len(arr)):
        img = Image.open("icons/" + arr[i]["weather"][0]["icon"] + ".png")
        image.paste(img, (i*50, 0))
    image.save("icons/temp.png")
    for i in range(len(arr)):
        result[i] += (
        "~~Погода в Москве: " + arr[i]["weather"][0]["description"] + "\n" +
        "~~Температура: " + str(round(arr[i]["main"]["temp_min"])) + "-" + str(round(arr[i]["main"]["temp_max"])) + "°C\n" +
        "~~Давление: " + str(round(arr[i]["main"]["pressure"]*0.75)) +  " мм рт. ст." + "\n"
        "~~Влажность: " + str(arr[i]["main"]["humidity"]) + "%\n" + 
        "~~Ветер: " + get_wind(arr[i]["wind"]["speed"]) + ", " + str(arr[i]["wind"]["speed"]) + "м/с , " + get_winddirection(arr[i]["wind"]["deg"])
        )
    result.append(
        "\nСредняя погода в течение дня:\n\n" + "".join(["------" + str(round((arr[i]["main"]["temp_min"]+arr[i]["main"]["temp_max"])/2)) + "°C" for i in range(len(arr))])
    )
    return ["\n".join(result), "icons/temp.png"]

def fiveday_weather():
    page = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=moscow&appid=baae14e4c755825f78434e0aea84846b&units=metric&lang=ru")
    info = page.json() 
    day_arr = ["------" + str(round((el["main"]["temp_min"]+el["main"]["temp_max"])/2)) + "°C" for el in info["list"] if str(el["dt_txt"]).split(' ')[1] == "15:00:00"]
    night_arr = ["------" + str(round((el["main"]["temp_min"]+el["main"]["temp_max"])/2)) + "°C" for el in info["list"] if str(el["dt_txt"]).split(' ')[1] == "00:00:00"]
    image = Image.new("RGB", (50*len(day_arr), 50))
    с = 0
    for i in range(len(info["list"])):
        if str(info["list"][i]["dt_txt"]).split(" ")[1] == "15:00:00":
            img = Image.open("icons/" + info["list"][i]["weather"][0]["icon"] + ".png")
            print(info["list"][i]["weather"][0]["icon"])
            image.paste(img, (с*50, 0))
            с += 1
    image.save("icons/temp.png")
    return [(
        "Погода с " + datetime.date.strftime(datetime.date.today(), "%d.%m") +
        " по " + datetime.date.strftime(datetime.date.today() + datetime.timedelta(days=4), "%d.%m" + ":\n") +
        "".join(day_arr) + "----ДЕНЬ\n" +
        "".join(night_arr) + "----НОЧЬ"
        ), "icons/temp.png"]


def get_wind(speed):
    if speed <= 0.2:
        return "штиль"
    elif speed >= 0.3 and speed <= 1.5:
        return "тихий"
    elif speed >= 1.6 and speed <= 3.3:
        return "легкий"
    elif speed >= 3.4 and speed <= 5.4:
        return "слабый"
    elif speed >= 5.5 and speed <= 7.9:
        return "умеренный"
    elif speed >= 8 and speed <= 10.7:
        return "свежий"
    elif speed >= 10.8 and speed <= 13.8:
        return "сильный"
    elif speed >= 13.9 and speed <= 17.1:
        return "крепкий"
    elif speed >= 17.2 and speed <= 20.7:
        return "очень крепкий"
    elif speed >= 20.8 and speed <= 24.4:
        return "шторм"
    elif speed >= 24.5 and speed <= 28.4:
        return "буря"
    elif speed >= 28.5 and speed <= 32.6:
        return "жесткий шторм"
    else:
        return "ураган"

def get_winddirection(deg):
    page = requests.get("https://ru.wikipedia.org/wiki/%D0%A0%D1%83%D0%BC%D0%B1")
    soup = BeautifulSoup(page.text, "html.parser")
    result = soup.find("table", {"class":"wikitable"}).findAll("td")
    degree_arr = []
    name_arr = []
    for i in range(0, len(result), 7):
        degree_arr.append(float(result[i+5].text.replace(",", ".")[:-1]))
        name_arr.append(result[i+4].text)
    for degree in reversed(degree_arr):
        if deg >= degree:
            return name_arr[degree_arr.index(degree)]

