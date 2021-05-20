import calendar
import datetime

now = datetime.datetime.now().day

#last_monday = max(week[calendar.MONDAY]
    #for week in calendar.monthcalendar(now.year, now.month))
#print('{:4d}-{:02d}-{:02d}'.format(now.year, now.month, last_monday))
print(now)