import calendar
import datetime
import config as config

# Gets the last meeting day of the month
def getLastMeetingDay():
    now = datetime.datetime.now()
    last_day = max(week[config.meetingDay]
        for week in calendar.monthcalendar(now.year, now.month))
    return int(last_day)

# Converts an hour and minute to a readable time for logging purposes
def hourToPrintStandardTime(hour, minute):
    printableHour = hour
    printableAmPm = 'AM'
    if (hour <= 0 or hour >= 24):
        printableHour = 12
    elif (hour >= 13):
        printableHour = hour - 12
    if (hour >= 11 and hour < 24):
        printableAmPm = 'PM'
    return str(printableHour) + ':' + str(minute).zfill(2) + ' ' + str(printableAmPm) + ' CST'