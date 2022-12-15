import jsonfiles
from datetime import datetime, date, time

Translate = {
    'N': '№',
    'regdate': 'Дата регистрации',
    'regtime': 'Время',
    'manager': 'Зарегистрировал',
    'contragent': 'Клиент',
    'task': 'Заявка',
    'confdate': 'Дата принятия',
    'conftime': 'Время',
    'master': 'Мастер',
    'donedate': 'Дата завершения',
    'donetime': 'Время',
    'whocancel': 'Отменил',
    'cancelreson': 'Причина отмены',
    'canceldate': 'Дата отмены',
    'canceltime': 'Время',
    'status': 'Статус'
    }

def taskgen(task):
    global Translate
    messagetext = ''
    for i in task:
        if i == 'manager' or i == 'master' or i == 'whocancel':
            if task[i] != 0:
                user = jsonfiles.findindata('userid', task[i], jsonfiles.openfile('Users.json'))
                username = str(user['userlname']) + ' ' + str(user['userfname'])
                messagetext = str(messagetext) + Translate[i] + ': ' + username + '\n'
        elif i == 'contragent':
            messagetext = messagetext + str(jsonfiles.findindata('INN', task[i], jsonfiles.openfile('Contragents.json'))['name']) + '\n'
        elif task[i] != '-' and i != 'status':
            messagetext = messagetext + Translate[i] + ': ' + str(task[i]) + '\n'
        elif i == 'status':
            if task[i] == 0:
                messagetext = messagetext + str(i) + ': ' + 'Зарегистрирована'
            elif task[i] == 1:
                messagetext = messagetext + str(i) + ': ' + 'В работе'
            elif task[i] == 2:
                messagetext = messagetext + str(i) + ': ' + 'Выполнено'
            elif task[i] == 3:
                messagetext = messagetext + str(i) + ': ' + 'Отменена'
    return messagetext
