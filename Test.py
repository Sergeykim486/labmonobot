from datetime import datetime, date, time
now = datetime.now()
x = datetime.strftime(now, '%H.%M')
print(x)