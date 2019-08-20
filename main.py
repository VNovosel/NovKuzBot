import telebot
from telebot import types  # хранится клавиатура(кнопки)
import const
from geopy.distance import geodesic

bot = telebot.TeleBot(const.TOKEN)

#новая попытка изменения файла
#третье изменение
################# МЕНЮ ВНИЗУ #############################
# создаем клавиатуру  (размер, в одной строке одна кнопка)
#вместо murkup_menu может быть что угодно свое, тогда чуть ниже markup_menu.add тоже изменяется
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

# создаем наши кнопки (у кнопок есть параметры: запросит локацию)
btn_address = types.KeyboardButton('Адрес тренировок', request_location=True)
btn_service = types.KeyboardButton('Услуги')
btn_peyment = types.KeyboardButton('Стоимость услуг')
btn_link = types.KeyboardButton('Мой сайт')
btn_help = types.KeyboardButton('Консультации')

# добавляем наши кнопки в "Объект клавиатура"
markup_menu.add(btn_address, btn_service, btn_peyment, btn_link, btn_help)
#############################################################

################# МЕНЮ В ТЕКСТЕ #############################
# создаем инлайн кнопки
markup_inline_menu = types.InlineKeyboardMarkup()
btn_in_bju = types.InlineKeyboardButton('Рассчет БЖУ', callback_data='bju')
btn_in_text2 = types.InlineKeyboardButton('Текст 2', callback_data='text2')

# добавляем созданные кнопки в меню
markup_inline_menu.add(btn_in_bju, btn_in_text2)
#############################################################

# обработчик         (свойство   [команды])
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    #print(message) - выводим входные данные в консоль
    bot.reply_to(message, '{0}, '.format(message.from_user.first_name) +
                          'здравствуйте! Я БОТ-помощник Арменуи.' + '\n'
                          'Здесь Вы можете получить всю интересующую Вас информацию. '
                          'Выберите один из пунктов меню ниже.',
                           reply_markup=markup_menu)
    # показать клавиатуру


# функция: send_welcome, параметр: message, метод: reply_to

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    text = message.text #*******положили сюда наш текст - написанный пользователем, при вызове функции*****
    if text == 'Услуги': # вместо message.text теперь можно написать просто текст
        bot.reply_to(message, 'Вам доступны:' + '\n'
                              '- групповые фитнес тренировки; ' + '\n'
                              '- помощь в подборе правильного питания; ' + '\n'
                              '- видеокурс тренировок с подробными комментариями.')
    elif message.text == 'Стоимость услуг':
        bot.reply_to(message, 'Вы можете приобрести:' + '\n'
                              '- разовое занятие - 325 рублей' + '\n'
                              '- абонемент на групповые занятия - 2200 рублей/8 занятий.' + '\n'
                              '- рекомендации по питанию - 999 рублей. ' + '\n'
                              '- видеокурс ONLINE "Базовый уровень" - 1000 рублей. ')
    elif message.text == 'Мой сайт':
        bot.reply_to(message, 'Ссылка на сайт с более подробной информацией: https://amirzoyan.ru/')
    elif message.text == 'Консультации':
        bot.reply_to(message, 'Выберете нужный раздел:',
                               reply_markup=markup_inline_menu)
    else:
        bot.reply_to(message, 'Выберите один из пунктов меню, а не "' + text + '"') # вначале функции мы ввели переменную text и теперь можем ее использовать

# отвечаем на фото
@bot.message_handler(content_types=['photo'])
def text_handler(message):
    # задали переменную, которую используем ниже как аргумент в bot.send.message
    chat_id = message.chat.id # задали переменную, которую используем ниже как аргумент в bot.send.message
    bot.send_message(chat_id, 'Красиво.')


#################### БЛИЖАЙШАЯ ТОЧКА #########################
# определяем координаты
# из параметра у кнопки
@bot.message_handler(func=lambda m: True, content_types=['location'])
def fitness_location(message):
    lon = message.location.longitude
    lat = message.location.latitude

    distance = []
    for m in const.GYM:
        result = geodesic(m['latm'], m['lonm'], (lat, lon)).km
        distance.append(result)
    index = distance.index(min(distance))

    bot.send_message(message.chat.id, 'Ближайший к Вам зал')
    bot.send_venue(message.chat.id,
                   const.GYM[index]['latm'],
                   const.GYM[index]['lonm'],
                   const.GYM[index]['title'],
                   const.GYM[index]['address'])


################### КБЖУ #####################
@bot.callback_query_handler(func=lambda call:True)
def call_back_help(call):
    if call.data == 'bju':
        bot.send_message(call.message.chat.id, text='функция не реализована')




############# бесконечный цикл ожидания запросов от пользователей
#bot.polling(none_stop=True, interval=0)
