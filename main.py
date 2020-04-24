import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
from googletrans import Translator
import subprocess
from pyowm import OWM
import youtube_dl
import urllib
import urllib3
import json
from bs4 import BeautifulSoup as soup
import wikipedia
import random
from time import strftime
import requests
from currency_converter import CurrencyConverter


# преобразовывание текста в речь
def HelperSpeaks(speech):
    print(speech)
    for line in speech.splitlines():
        os.system("say " + speech)


# интерпретация голосового ответа пользователя
def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Скажите что-нибудь')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='RU-ru').lower()
        print('Вы сказали: ' + command + '\n')
    # если речь не распознана
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command


# функции
# открыть любую страницу
def assistant(command):
    if 'открой' in command:
        reg_ex = re.search('открой (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            HelperSpeaks('Веб-сайт, который вы запросили, был открыт для вас')
        else:
            pass
    elif 'пока' in command:
        HelperSpeaks('До свидания')
        sys.exit()
        #рассказывает о понятии из википедии в 3-х первых предложения
    elif 'расскажи мне о ' in command:
        reg_ex = re.search('расскажи мне о (.*)', command)
        try:
            if reg_ex:
                wikipedia.set_lang("ru")
                topic = reg_ex.group(1)
                HelperSpeaks(wikipedia.summary(topic, sentences=3))
        except Exception as e:
                print(e)
                HelperSpeaks(e)
    # приветствие
    elif 'привет' in command:
        day_time = int(strftime('%H'))
        if 4 <= day_time < 8:
            HelperSpeaks('Здравствуйте. Доброе утро')
        elif 9 <= day_time < 16:
            HelperSpeaks('Здравствуйте. Добрый день')
        elif 17 <= day_time <20:
            HelperSpeaks('Здравствуйте. Добрый вечер')
        else:
            HelperSpeaks('Здравствуйте. Доброй ночи')
    # расскажет о своих коммандах
    elif 'помоги мне' in command:
        HelperSpeaks("""
        Вы можете использовать эти команды, и я вам помогу:
        1.Открой {название сайта} - открою необходимый сайт
        2.Текущая погода в {город} - скажу вам текущее состояние и температуру воздуха
        3.Привет - поприветствую вас
        4.Время - скажу текущее системное время
        5.Пока - я выключусь
        6.Расскажи мне о {название предмета} - прочитаю из википедии первые 3 предложения.
        7.Переведи на английский {текст перевода} - переведу текст на английский
        """)
    #переведет текст на английский
    elif 'переведи на английский' in command:
        reg_ex = re.search('переведи на английский (.*)', command)
        try:
            if reg_ex:
                text = reg_ex.group(1)
                translator = Translator()
                translated = translator.translate(text, src = 'ru', dest ='en')
                HelperSpeaks(translated.text)
        except Exception as e:
            print(e)
            HelperSpeaks(e)

    # погода
    elif 'погода в городе' in command:
        reg_ex = re.search('погода в городе (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM('ba3126250c770d7e0a33dce442d14582', language="RU")
            observation = owm.weather_at_place(city)
            w = observation.get_weather()
            temp = w.get_temperature('celsius')['temp']
            HelperSpeaks('в городе ' + city + ' сейчас ' + str(w.get_detailed_status()))
            HelperSpeaks('температура ' + str(temp))
    # время
    elif 'время' in command:
        import datetime
        now = datetime.datetime.now()
        HelperSpeaks('Текущее время  %d часов %d минут' % (now.hour, now.minute))


while True:
    assistant(myCommand())

# Дополнить чтением новостей
# конвертер