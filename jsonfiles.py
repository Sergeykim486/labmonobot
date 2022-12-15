import json
from datetime import datetime, date, time

def openfile(file_name):
    file = open('database/' + file_name, 'r')
    data = json.loads(file.read())
    file.close()
    return data

def writefile(file_name, data):
    file = open('database/' + file_name, 'w')
    file.write(json.dumps(data, indent=2))
    file.close()
    
def findindata(field, f, data):
    findedobj = 0
    for item in data['response']['item']:
        if item[field] == f:
            findedobj = 1
            finded = item
            return finded
    if findedobj == 0:
        return findedobj

def gettaskslist(file_name, x = 0, y = 0):
    tasks = openfile(file_name)
    tasklist = dict([])
    messagetext = ''
    if x == 0 and y == 0:
        for tasks in tasks['response']['item']:
            tnum = str(tasks['N'])
            tstatus = tasks['status']
            contragent = findindata('INN', tasks['contragent'], openfile('Contragents.json'))
            messagetext = '№ ' + tnum + ' от ' + str(tasks['regdate']) + ' ' + str(tasks['regtime']) + ':' + str(contragent['name'])
            if tstatus == 0:
                messagetext = '🔵' + messagetext
            elif tstatus == 1:
                messagetext = '🟡' + messagetext
            elif tstatus == 2:
                messagetext = '🟢' + messagetext
            elif tstatus == 3:
                messagetext = '🔴' + messagetext
            tasklist[tnum] = messagetext
    else:
        for tasks in tasks['response']['item']:
            dtt = datetime.strptime(tasks['regdate'], '%d.%m.%Y')
            if x <= dtt <= y:
                tnum = str(tasks['N'])
                tstatus = tasks['status']
                contragent = findindata('INN', tasks['contragent'], openfile('Contragents.json'))
                messagetext = '№ ' + tnum + ' от ' + str(tasks['regdate']) + ' ' + str(tasks['regtime']) + ':' + str(contragent['name'])
                if tstatus == 0:
                    messagetext = '🔵' + messagetext
                elif tstatus == 1:
                    messagetext = '🟡' + messagetext
                elif tstatus == 2:
                    messagetext = '🟢' + messagetext
                elif tstatus == 3:
                    messagetext = '🔴' + messagetext
                tasklist[tnum] = messagetext
    return tasklist

def getmytaskslist(file_name, user):
    tasks = openfile(file_name)
    tasklist = dict([])
    messagetext = ''
    for tasks in tasks['response']['item']:
        if tasks['master'] == user:
            tnum = str(tasks['N'])
            tstatus = tasks['status']
            contragent = findindata('INN', tasks['contragent'], openfile('Contragents.json'))
            messagetext = '№ ' + tnum + ' от ' + str(tasks['regdate']) + ' ' + str(tasks['regtime']) + ':' + str(contragent['name'])
            if tstatus == 0:
                messagetext = '🔵' + messagetext
            elif tstatus == 1:
                messagetext = '🟡' + messagetext
            elif tstatus == 2:
                messagetext = '🟢' + messagetext
            elif tstatus == 3:
                messagetext = '🔴' + messagetext
            tasklist[tnum] = messagetext
    return tasklist