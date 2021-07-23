import os
import calendar
from dotenv import load_dotenv

# REQUIRES RESTART OF BOT TO APPLY CHANGES

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
suggChannel = os.getenv('SUGG_CHANNEL') or '839962435044900874'
announcementChannel = os.getenv('ANNOUNCEMENT_CHANNEL') or '839961783498571867'
testChannel = os.getenv('TEST_CHANNEL') or '840042019971661825'
commandPrefix = '$'

# Meeting date & time
pollDay = os.getenv('POLL_DAY') or calendar.SUNDAY
pollHour = os.getenv('POLL_HOUR') or 20
pollMinute = os.getenv('POLL_MINUTE') or 0
meetingDay = os.getenv('MEETING_DAY') or calendar.MONDAY
meetingHour = os.getenv('MEETING_HOUR') or 20
meetingMinute = os.getenv('MEETING_MINUTE') or 0