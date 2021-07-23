import os
import calendar
from dotenv import load_dotenv

# REQUIRES RESTART OF BOT TO APPLY CHANGES

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
suggChannel = os.getenv('SUGG_CHANNEL') or 839962435044900874
announcementChannel = os.getenv('ANNOUNCEMENT_CHANNEL') or 839961783498571867
testChannel = os.getenv('TEST_CHANNEL') or 840042019971661825
commandPrefix = '$'

# Poll start date & time
pollStartDay = os.getenv('POLL_START_DAY') or calendar.SUNDAY
pollStartHour = os.getenv('POLL_START_HOUR') or 20
pollStartMinute = os.getenv('POLL_START_MINUTE') or 0

# Poll end date & time
pollEndDay = os.getenv('POLL_END_DAY') or calendar.MONDAY
pollEndHour = os.getenv('POLL_END_HOUR') or 19
pollEndMinute = os.getenv('POLL_END_MINUTE') or 30

# Meeting date & time
meetingDay = os.getenv('MEETING_DAY') or calendar.MONDAY
meetingHour = os.getenv('MEETING_HOUR') or 20
meetingMinute = os.getenv('MEETING_MINUTE') or 0