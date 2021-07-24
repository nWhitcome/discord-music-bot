import os
import calendar
from dotenv import load_dotenv

# REQUIRES RESTART OF BOT TO APPLY CHANGES

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
suggChannel = os.getenv('SUGG_CHANNEL', '839962435044900874')
announcementChannel = os.getenv('ANNOUNCEMENT_CHANNEL', '839961783498571867')
testChannel = os.getenv('TEST_CHANNEL','840042019971661825')
commandPrefix = '$'

# Meeting date & time
pollDay = int(os.getenv('POLL_DAY', calendar.SUNDAY))
pollHour = int(os.getenv('POLL_HOUR', 20))
pollMinute = int(os.getenv('POLL_MINUTE', 0))
meetingDay = int(os.getenv('MEETING_DAY', calendar.MONDAY))
meetingHour = int(os.getenv('MEETING_HOUR', 20))
meetingMinute = int(os.getenv('MEETING_MINUTE', 0))