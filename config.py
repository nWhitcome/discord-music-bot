import os
import calendar
from dotenv import load_dotenv

# REQUIRES RESTART OF BOT TO APPLY CHANGES

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
suggChannel = os.getenv('SUGG_CHANNEL', '839962435044900874')
announcementChannel = os.getenv('ANNOUNCEMENT_CHANNEL', '839961783498571867')
suggChannelMovie = os.getenv('SUGG_CHANNEL_MOVIE', '867434344715649034')
announcementChannelMovie = os.getenv('ANNOUNCEMENT_CHANNEL_MOVIE', '867434989519634432')
testChannel = os.getenv('TEST_CHANNEL','840042019971661825')
testChannelMovie = os.getenv('TEST_CHANNEL_MOVIE','874768828867960902')
commandPrefix = '$'

# Meeting date & time for the music club
musicId = "<@&839958672868245504>"
pollDay = int(os.getenv('POLL_DAY', calendar.SUNDAY))
pollHour = int(os.getenv('POLL_HOUR', 20))
pollMinute = int(os.getenv('POLL_MINUTE', 0))
meetingDay = int(os.getenv('MEETING_DAY', calendar.MONDAY))
meetingHour = int(os.getenv('MEETING_HOUR', 20))
meetingMinute = int(os.getenv('MEETING_MINUTE', 0))
reminderHour = int(os.getenv('MEETING_HOUR', 19))
reminderMinute = int(os.getenv('MEETING_MINUTE', 30))

# Meeting date & time for the movie club
movieId = "<@&872896127882633268>"
pollDayMovie = int(os.getenv('POLL_DAY_MOVIE', calendar.TUESDAY))
pollHourMovie = int(os.getenv('POLL_HOUR_MOVIE', 12))
pollMinuteMovie = int(os.getenv('POLL_MINUTE_MOVIE', 0))
meetingDayMovie = int(os.getenv('MEETING_DAY_MOVIE', calendar.TUESDAY))
meetingHourMovie = int(os.getenv('MEETING_HOUR_MOVIE', 22))
meetingMinuteMovie = int(os.getenv('MEETING_MINUTE_MOVIE', 0))
reminderHourMovie = int(os.getenv('MEETING_HOUR', 11))
reminderMinuteMovie = int(os.getenv('MEETING_MINUTE', 30))
