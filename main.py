import telebot
from telebot import types
import json
from datetime import datetime, date, time
import config, jsonfiles, Functions
bot = telebot.TeleBot(config.TOKEN)
# Глобальные переменные
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
a = telebot.types.ReplyKeyboardRemove()

@bot.message_handler(commands=['start'])

# ====================  С Т А Р Т   Б О Т А  ====================
def send_welcome(message):
    markup = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Начать работу')
    bot.send_message(message.chat.id, 'Добро пожаловать в систему.', reply_markup=markup)
    bot.register_next_step_handler(message, start_working)
def start_working(message):
    markup = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Начать работу')
    if message.text == 'Начать работу' or message.text == 'Главное меню':
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        user = jsonfiles.findindata('userid', message.chat.id, jsonfiles.openfile('Users.json'))
        if user == 0:
            markup.row('Зарегистрироваться')
            bot.send_message(message.chat.id, f'Приветствую!\nВы не авторизованы.\nПожалуйста зарегистрируйтесь.', reply_markup=markup)
            bot.register_next_step_handler(message, reg1)
        elif user['userid'] == message.chat.id:
            markup.row('Список заявок', 'Мои заявки', 'Добавить заявку')
            markup.row('Написать всем участникам')
            bot.send_message(message.chat.id, 'Выберите действие...', reply_markup=markup)
            bot.register_next_step_handler(message, main_menu)
    else:
         bot.send_message(message.chat.id, 'Команда не распознана!', reply_markup=markup)
         bot.register_next_step_handler(message, start_working)
        
# ===============================================================

@bot.message_handler(content_types=['text'])

# ==================== ГЛАВНОЕ МЕНЮ ====================
def main_menu(Message):
    if Message.text == 'Список заявок':
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Все', 'За период')
        markup.row('Отмена')
        bot.send_message(Message.chat.id, 'Какие заявки отобразить?', reply_markup=markup)
        bot.register_next_step_handler(Message, WhatTasks)
    elif Message.text == 'Написать всем участникам':
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Отмена')
        bot.send_message(Message.chat.id, 'Что вы хотите написать?', reply_markup=markup)
        bot.register_next_step_handler(Message, chat)
    elif Message.text == 'Мои заявки':
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Tasklist = jsonfiles.getmytaskslist('Tasks.json', Message.chat.id)
        for i in Tasklist:
            ib = types.InlineKeyboardButton('Подробнее', callback_data=i)
            q = types.InlineKeyboardMarkup().add(ib)
            bot.send_message(Message.chat.id, Tasklist[i], reply_markup=q)
        bot.register_next_step_handler(Message, main_menu)
    elif Message.text == 'Добавить заявку':
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        contr = jsonfiles.openfile('Contragents.json')
        mark = ''
        for item in contr['response']['item']:
            x = int(item['INN'])
            y = str(item['name'])
            mark = str(x) + ' - ' + y
            markup.row(mark)
        bot.send_message(Message.chat.id, 'Введите ИНН клиента', reply_markup=markup)
        bot.register_next_step_handler(Message, newtask1)
    else:
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Список заявок', 'Мои заявки', 'Добавить заявку')
        markup.row('Написать всем участникам')
        bot.send_message(Message.chat.id, 'команда не опознана.', reply_markup=markup)
        bot.register_next_step_handler(Message, main_menu)
# ===================================================================

# ==================== НОВАЯ ЗАЯВКА ====================
curtask = {'N': 0, 'regdate': '-', 'regtime': '-', 'manager': 0, 'contragent': 0, 'task': '-', 'confdate': '-', 'conftime': '-', 'master': 0, 'donedate': '-', 'donetime': '-', 'whocancel': 0, 'cancelreson': '-', 'canceldate': '-', 'canceltime': '-', 'status': 0,}
newcontr = 0
newcontrinn = 0
newcontrname = ''
newcontrperson = ''
newcontrphone = ''
def newtask1(Message):
    global curtask, newcontr, newcontrname, newcontrperson, newcontrinn, newcontrphone
    markup = types.ReplyKeyboardRemove()
    inn = str(Message.text)
    cinn = int(inn.split(' - ')[0])
    contr = jsonfiles.findindata('INN', cinn, jsonfiles.openfile('Contragents.json'))
    if contr['INN'] == int(cinn):
        curtask['contragent'] = cinn
        newcontr = 0
        bot.send_message(Message.chat.id, 'Кратко опишите проблему клиента, в одном сообщении.', reply_markup=a)
        bot.register_next_step_handler(Message, newtask4)
    else:
        curtask['contragent'] = cinn
        newcontrinn = cinn
        newcontr = 1
        bot.send_message(Message.chat.id, 'Введите наименование организации.', reply_markup=a)
        bot.register_next_step_handler(Message, newtask2)
def newtask2(Message):
    global curtask, newcontr, newcontrname, newcontrperson, newcontrinn, newcontrphone
    newcontrname = Message.text
    bot.send_message(Message.chat.id, 'Укажите контактное лицо клиента.', reply_markup=a)
    bot.register_next_step_handler(Message, newtask31)
def newtask31(Message):
    global curtask, newcontr, newcontrname, newcontrperson, newcontrinn, newcontrphone
    newcontrperson = Message.text
    bot.send_message(Message.chat.id, 'Укажите номер клиента.', reply_markup=a)
    bot.register_next_step_handler(Message, newtask3)
def newtask3(Message):
    global curtask, newcontr, newcontrname, newcontrperson, newcontrinn, newcontrphone
    newcontrphone = Message.text
    bot.send_message(Message.chat.id, 'Кратко опишите проблему клиента, в одном сообщении.', reply_markup=a)
    bot.register_next_step_handler(Message, newtask4)
def newtask4(Message):
    markup = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    global curtask, newcontr, newcontrname, newcontrperson, newcontrinn, newcontrphone
    curtask['task'] = Message.text
    curtask['manager'] = Message.chat.id
    fff = jsonfiles.openfile('Tasks.json')
    curtask['N'] = len(fff['response']['item'])+1
    now = datetime.now()
    curtask['regtime'] = datetime.strftime(now, '%H.%M')
    curtask['regdate'] = datetime.strftime(now, '%d.%m.%Y')
    nc = jsonfiles.openfile('Contragents.json')
    ncontr = {'INN': newcontrinn, 'name': newcontrname, 'person': newcontrperson, 'tel': newcontrphone}
    nc['response']['item'].append(ncontr)
    jsonfiles.writefile('Contragents.json', nc)
    markup.row('Да', 'Нет')
    bot.send_message(Message.chat.id, Functions.taskgen(curtask))
    bot.send_message(Message.chat.id, 'Подтвердите информацию', reply_markup=markup)
    bot.register_next_step_handler(Message, newtask5)
def newtask5(Message):
    global curtask, newcontr, newcontrname, newcontrperson, newcontrinn, newcontrphone
    markup = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if Message.text == 'Да':
        tasks = jsonfiles.openfile('Tasks.json')
        tasks['response']['item'].append(curtask)
        jsonfiles.writefile('Tasks.json', tasks)
        bot.send_message(Message.chat.id, 'Данные сохранены.', reply_markup=markup)
        for users in jsonfiles.openfile('Users.json')['response']['item']:
            ib = types.InlineKeyboardButton('Принять', callback_data=str(curtask['N'])+'-confirm')
            q = types.InlineKeyboardMarkup().add(ib)
            bot.send_message(users['userid'], f"‼️ Новая заявка ‼️ \n {Functions.taskgen(curtask)}",reply_markup=q)
        bot.register_next_step_handler(Message, start_working)
    elif Message.text == 'Нет':
        bot.send_message(Message.chat.id, 'Введите данные снова.')
        contr = jsonfiles.openfile('Contragents.json')
        for item in contr['response']['item']:
            mark = str(item['INN']) + ' - ' + str(item['name'])
            markup.row(mark)
        bot.send_message(Message.chat.id, 'Введите ИНН клиента', reply_markup=markup)
        bot.register_next_step_handler(Message, newtask1)
    else:
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Да', 'Нет')
        bot.send_message(Message.chat.id, 'Не верная команда')
        bot.send_message(Message.chat.id, Functions.taskgen(curtask))
        bot.send_message(Message.chat.id, 'Подтвердите информацию', reply_markup=markup)
        bot.register_next_step_handler(Message, newtask5)
        
# =================================================================

# ==================== СПИСОК ЗАЯВОК ====================
dtfrom = ''
dtto = ''
def WhatTasks(Message):
    global a, dtfrom, dtto
    markup = types.ReplyKeyboardRemove()
    if Message.text == 'Все':
        Tasklist = jsonfiles.gettaskslist('Tasks.json')
        for i in Tasklist:
            ib = types.InlineKeyboardButton('Подробнее', callback_data=i)
            q = types.InlineKeyboardMarkup().add(ib)
            markup = types.ReplyKeyboardRemove()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('Список заявок', 'Добавить заявку')
            markup.row('Написать всем участникам')
            bot.send_message(Message.chat.id, Tasklist[i], reply_markup=q)
        bot.send_message(Message.chat.id, 'Выберите действие', reply_markup=markup)
        bot.register_next_step_handler(Message, main_menu)
    elif Message.text == 'За период' or Message.text == 'Повтор':
        bot.send_message(Message.chat.id, 'Укажите начало периода\n в формате ДД.ММ.ГГГГ\n\nНапример:\n  01.01.2022', reply_markup=a)
        bot.register_next_step_handler(Message, datesfrom)
    elif Message.text == 'Отмена':
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Главное меню')
        bot.send_message(Message.chat.id, 'Возврат в главное меню.', reply_markup=markup)
        bot.register_next_step_handler(Message, start_working)
def datesfrom(Message):
    global a, dtfrom, dtto
    markup = types.ReplyKeyboardRemove()
    dtfrom = datetime.strptime(Message.text, '%d.%m.%Y')
    if dtfrom != False:
        bot.send_message(Message.chat.id, 'Укажите конец периода\n в формате ДД.ММ.ГГГГ\n\nНапример:\n  01.01.2022', reply_markup=a)
        bot.register_next_step_handler(Message, datesto)
    else:
        bot.send_message(Message.chat.id, 'Укажите начало периода\n в формате ДД.ММ.ГГГГ\n\nНапример:\n  01.01.2022', reply_markup=a)
        bot.register_next_step_handler(Message, datesfrom)
def datesto(Message):
    markup = types.ReplyKeyboardRemove()
    global a, dtfrom, dtto
    dtto = datetime.strptime(Message.text, '%d.%m.%Y')
    if dtto != False:
        Tasklist = jsonfiles.gettaskslist('Tasks.json', dtfrom, dtto)
        for i in Tasklist:
            ib = types.InlineKeyboardButton('Подробнее', callback_data=i)
            q = types.InlineKeyboardMarkup().add(ib)
            bot.send_message(Message.chat.id, Tasklist[i], reply_markup=q)
        bot.register_next_step_handler(Message, main_menu)
    elif dtto < dtfrom:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Повтор', 'Отмена')
        bot.send_message(Message.chat.id, '', reply_markup=a)
        bot.register_next_step_handler(Message, WhatTasks)
# =================================================================

# ==================== отправка сообщения всем ====================
def chat(Message):
    if Message.text != 'Отмена':
        user = jsonfiles.findindata('userid', Message.chat.id, jsonfiles.openfile('Users.json'))
        sfname = user['userfname']
        slname = user['userlname']
        for users in jsonfiles.openfile('Users.json')['response']['item']:
            bot.send_message(users['userid'], f"‼️ сообщение ‼️ \n от {slname} {sfname}\n\n{Message.text}")
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Главное меню')
        bot.send_message(Message.chat.id, 'Ваше сообщение отправлено', reply_markup=markup)
        bot.register_next_step_handler(Message, start_working)
    else:
        markup = types.ReplyKeyboardRemove()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Главное меню')
        bot.send_message(Message.chat.id, 'Возврат в главное меню.', reply_markup=markup)
        bot.register_next_step_handler(Message, start_working)
# =================================================================

# ==================== РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ ====================
ruid = 0
rufname = ''
rulname = ''
ruphone = ''
def reg1(Message):
    markup = types.ReplyKeyboardRemove()
    if Message.chat.type == 'private':
        if Message.text == 'Зарегистрироваться':
            bot.send_message(Message.chat.id, 'Напишите Ваше имя.', reply_markup=a)
            bot.register_next_step_handler(Message, reg2)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('Зарегистрироваться')
            bot.send_message(Message.chat.id, f'Не верный ввод', reply_markup=markup)
            bot.register_next_step_handler(Message, reg1)
def reg2(message):
    global ruid, rufname, rulname, ruphone, a
    bot.send_message(message.chat.id, 'Напишите Вашу фамилию.', reply_markup=a)
    if message.chat.type == 'private':
        rufname = message.text
        bot.register_next_step_handler(message, reg3)
def reg3(message):
    global ruid, rufname, rulname, ruphone, a
    bot.send_message(message.chat.id, 'Напишите Ваш номер телефона.\nв формате +99897 XXX XX XX', reply_markup=a)
    if message.chat.type == 'private':
        rulname = message.text
        bot.register_next_step_handler(message, reg4)
def reg4(message):
    global ruid, rufname, rulname, ruphone
    ruphone = message.text
    markup = types.ReplyKeyboardRemove()
    if message.chat.type == 'private':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Да', 'Нет')
        bot.send_message(message.chat.id, f'Пожалуйста подтвердите введенные данные.\n\n'
                        f'Имя: {rufname}\n'
                        f'Фамилия: {rulname}\n'
                        f'Номер телефона: {ruphone}\n'
                        f'Все верно?', reply_markup=markup)
        bot.register_next_step_handler(message, reg5)
def reg5(message):
    global ruid, rufname, rulname, ruphone
    markup = types.ReplyKeyboardRemove()
    ruid = message.chat.id
    if message.chat.type == 'private':
        if message.text == 'Да':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row('Главное меню')
            # Сохранение в файл нового пользователя
            usrj = jsonfiles.openfile('Users.json')
            json_data = {
                'userid': ruid,
                'userfname': rufname,
                'userlname': rulname,
                'tel': ruphone,
                }
            usrj['response']['item'].append(json_data)
            jsonfiles.writefile('Users.json', usrj)
            # ======================================
            bot.send_message(message.chat.id, 'Данные сохранены.', reply_markup=markup)
            bot.register_next_step_handler(message, start_working)
        elif message.text == 'Нет':
            bot.send_message(message.chat.id, 'Введите данные снова.')
            bot.send_message(message.chat.id, 'Напишите Ваше имя.', reply_markup=a)
            bot.register_next_step_handler(message, reg2)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.chat.id, 'Вы не подтвердили данные.')
            markup.row('Да', 'Нет')
            bot.send_message(message.chat.id, f'Пожалуйста подтвердите введенные данные.\n\n'
                            f'Имя: {rufname}\n'
                            f'Фамилия: {rulname}\n'
                            f'Номер телефона: {ruphone}\n'
                            f'Все верно?', reply_markup=markup)
            bot.register_next_step_handler(message, reg5)
# =========================================================================

@bot.callback_query_handler(func=lambda call: True)

def callback_inline(call):
    if call.message:
        comm = call.data
        confirmtask = comm.split('-')
        if len(confirmtask) > 0:
            conftask = jsonfiles.openfile('Tasks.json')
            for item in conftask['response']['item']:
                if item['N'] == int(confirmtask[0]):
                    item['master'] == call.message.chat.id
                    now = datetime.now()
                    item['conftime'] = datetime.strftime(now, '%H.%M')
                    item['confdate'] = datetime.strftime(now, '%d.%m.%Y')
            jsonfiles.writefile('Tasks.json', conftask)
        else:
            Task = jsonfiles.findindata('N', int(call.data), jsonfiles.openfile('Tasks.json'))
            mestext = Functions.taskgen(Task)
            bot.send_message(call.message.chat.id, mestext)
        

bot.polling(none_stop=True, interval=0)