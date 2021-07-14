import os
import calendar
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
suggChannel = '839962435044900874'
testChannel = '840042019971661825'
commandPrefix = '$'

# Meeting date & time
pollDay = os.getenv('POLL_DAY') or calendar.SUNDAY
pollHour = os.getenv('POLL_HOUR') or 20
pollMinute = os.getenv('POLL_MINUTE') or 0
meetingDay = os.getenv('MEETING_DAY') or calendar.MONDAY
meetingHour = os.getenv('MEETING_HOUR') or 20
meetingMinute = os.getenv('MEETING_MINUTE') or 0