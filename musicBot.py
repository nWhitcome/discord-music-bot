from discord.ext.commands import Bot
from discord.utils import get
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import sqlite3
import random
import calendar
import datetime
import config

bot = Bot(command_prefix=config.commandPrefix)

bot.runOnceFlag = 0
dictionary = {}
dictionaryMovie = {}



# Gets the last meeting day of the month
def getLastMeetingDay():
    now = datetime.datetime.now()
    last_day = max(week[config.meetingDay]
        for week in calendar.monthcalendar(now.year, now.month))
    return int(last_day)

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

# Code content that is run once when the bot is started up. For example: cron job declarations and selecting data from a database
def runOnce():
    if(bot.runOnceFlag == 0):
        print("Ready")
        conn = sqlite3.connect('weeklyData.db')
        makeTable = 'CREATE TABLE IF NOT EXISTS weekly (id text PRIMARY KEY, content text NOT NULL); '
        makeTableMovies = 'CREATE TABLE IF NOT EXISTS weeklyMovie (id text PRIMARY KEY, content text NOT NULL); '
        makeNoWinnerTable = 'CREATE TABLE IF NOT EXISTS noWinner (id text PRIMARY KEY, musicMeeting integer NOT NULL, movieMeeting integer NOT NULL); '

        c = conn.cursor()
        c.execute(makeTable)
        c.execute(makeTableMovies)
        c.execute(makeNoWinnerTable)
        
        c.execute('SELECT * FROM weekly;')
        rows = c.fetchall()
        for row in rows:
            dictionary[str(row[0])] = str(row[1])

        c.execute('SELECT * FROM noWinner;')
        rows = c.fetchall()
        if(rows):
            config.noWinnerMusic = rows[0][1]
            config.noWinnerMovie = rows[0][2]
            print("noWinnerMusic = " + str(config.noWinnerMusic) + ", noWinnerMovie = " + str(config.noWinnerMovie))
        else:
            conn = sqlite3.connect('weeklyData.db')
            c = conn.cursor()
            c.execute('INSERT OR REPLACE INTO noWinner(id, musicMeeting, movieMeeting) VALUES(?,?,?);', ("0", 0, 0))
            conn.commit()
        
        c.execute('SELECT * FROM weeklyMovie;')
        rows = c.fetchall()
        for row in rows:
            dictionaryMovie[str(row[0])] = str(row[1])

        scheduler = AsyncIOScheduler()
        scheduler.add_job(sendPoll, 'cron', day_of_week=config.pollDay, hour=config.pollHour, minute=config.pollMinute)
        scheduler.add_job(sendPollMovie, 'cron', day_of_week=config.pollDayMovie, hour=config.pollHourMovie, minute=config.pollMinuteMovie)
        scheduler.add_job(sendReminder, 'cron', day_of_week=config.meetingDay, hour=config.reminderHour, minute=config.reminderMinute)
        scheduler.add_job(sendReminderMovie, 'cron', day_of_week=config.meetingDayMovie, hour=config.reminderHourMovie, minute=config.reminderMinuteMovie)
        scheduler.add_job(chooseWinner, 'cron', day_of_week=config.meetingDay, hour=config.meetingHour, minute=config.meetingMinute)
        scheduler.add_job(chooseWinnerMovie, 'cron', day_of_week=config.meetingDayMovie, hour=config.meetingHourMovie, minute=config.meetingMinuteMovie)
        scheduler.start()
        print("Music poll set for " + calendar.day_name[config.pollDay] + " " + hourToPrintStandardTime(config.pollHour, config.pollMinute))
        print("Music reminder set for " + calendar.day_name[config.meetingDay] + " " + hourToPrintStandardTime(config.reminderHour, config.reminderMinute))
        print("Music meeting set for " + calendar.day_name[config.meetingDay] + " " + hourToPrintStandardTime(config.meetingHour, config.meetingMinute))
        print("Movie poll set for " + calendar.day_name[config.pollDayMovie] + " " + hourToPrintStandardTime(config.pollHourMovie, config.pollMinuteMovie))
        print("Movie reminder set for " + calendar.day_name[config.pollDayMovie] + " " + hourToPrintStandardTime(config.reminderHourMovie, config.reminderMinuteMovie))
        print("Movie meeting set for " + calendar.day_name[config.meetingDayMovie] + " " + hourToPrintStandardTime(config.meetingHourMovie, config.meetingMinuteMovie))
        bot.runOnceFlag = 1

# Sends out a poll so people can vote on album of the week
async def sendPoll():
    if(int(datetime.datetime.now().day) + 1 != getLastMeetingDay()):
        print("Posting poll...")
        channel = bot.get_channel(int(config.announcementChannel))
        if(dictionary.items()):
            pollString = '/poll "' + config.musicId + ', here is the poll for the album of the week:"'
            for i, j in dictionary.items():
                pollString += f' "{i} - {j}"'
            await channel.send(pollString)
            async for message in channel.history(limit = 10):
                if message.author == bot.user:
                    await message.delete()
                    break
            dictionary.clear()

            # Deletes all of the previous week's suggestions
            conn = sqlite3.connect('weeklyData.db')
            c = conn.cursor()
            c.execute('DELETE FROM weekly;')
            conn.commit()
        else:
            config.noWinnerMusic = 1
            conn = sqlite3.connect('weeklyData.db')
            c = conn.cursor()
            c.execute('UPDATE noWinner SET musicMeeting=1')
            conn.commit()
            print("No suggestions this week")

# Sends out a poll so people can vote on the movie of the week
async def sendPollMovie():
    print("Posting poll...")
    channel = bot.get_channel(int(config.announcementChannelMovie))
    if(dictionaryMovie.items()):
        pollString = '/poll "' + config.movieId + ', here is the poll for the movie of the week:"'
        for i, j in dictionaryMovie.items():
            pollString += f' "{i} - {j}"'
        await channel.send(pollString)
        #async for message in channel.history(limit = 10):
        #    if message.author == bot.user:
        #        await message.delete()
        #        break
        dictionaryMovie.clear()

        # Deletes all of the previous week's suggestions
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        c.execute('DELETE FROM weeklyMovie;')
        conn.commit()
    else:
        config.noWinnerMovie = 1
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        c.execute('UPDATE noWinner SET movieMeeting=1')
        conn.commit()
        print("No movie suggestions this week")

# Sends out a reminder for the music meeting 30 minutes before
async def sendReminder():
        channel = bot.get_channel(int(config.announcementChannel))
        pollString = config.musicId + ', the meeting for this week is starting in 30 minutes!'
        await channel.send(pollString)

# Sends out a reminder for the music meeting 30 minutes before
async def sendReminderMovie():
        channel = bot.get_channel(int(config.announcementChannelMovie))
        pollString = config.movieId + ', voting for this week starts in 30 minutes! Last chance to get your suggestions in!'
        await channel.send(pollString)

# Allows users to submit a suggestion for album of the week, which is then stored in a database
@bot.command(name='suggest')
async def suggest(ctx, *, arg):
    print("Received suggestion")
    if(str(ctx.channel.id) == config.suggChannel):
        dictionary[str(ctx.author)] = str(arg[:256])
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO weekly(id, content) VALUES(?,?);', (str(ctx.author), str(arg[:256])))
        conn.commit()
        await ctx.message.add_reaction("👍")

    elif(str(ctx.channel.id) == config.suggChannelMovie):
        dictionaryMovie[str(ctx.author)] = str(arg[:256])
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO weeklyMovie(id, content) VALUES(?,?);', (str(ctx.author), str(arg[:256])))
        conn.commit()
        await ctx.message.add_reaction("👍")

    else:
        print("Err: couldn't take suggestion")

# Lists all of the album choices that have been submitted
@bot.command(name='list')
async def listSuggestions(ctx):
    print("Listing suggestions")
    listString = ""
    if(str(ctx.channel.id) == config.suggChannel):
        if(not dictionary):
            await ctx.send("No suggestions... yet")
        else:
            for k, v in dictionary.items():
                listString += f'{k} - {v}\n'
            await ctx.send(listString)

    elif(str(ctx.channel.id) == config.suggChannelMovie):
        if(not dictionaryMovie):
            await ctx.send("No suggestions... yet")
        else:
            for k, v in dictionaryMovie.items():
                listString += f'{k} - {v}\n'
            await ctx.send(listString)

# Backup method that can only be called in the TestBot server that puts the album choice poll up in case it fails for some reason
@bot.command(name='poll')
async def poll(ctx):
    if(config.inTest == 1 and str(ctx.channel.id) == config.suggChannel):
        await sendPoll()

# Backup method that can only be called in the TestBot server that puts the album choice poll up in case it fails for some reason
@bot.command(name='pollMovie')
async def pollmovie(ctx):
    if(config.inTest == 1 and str(ctx.channel.id) == config.suggChannelMovie):
        await sendPollMovie()

# Backup method that can only be called in the TestBot server that chooses the winner
@bot.command(name='choosethewinner')
async def choosethewinner(ctx):
    if(config.inTest == 1 and str(ctx.channel.id) == config.suggChannel):
        await chooseWinner()

# Backup method that can only be called in the TestBot server that chooses the winner
@bot.command(name='choosethewinnermovie')
async def choosethewinnermovie(ctx):
    if(config.inTest == 1 and str(ctx.channel.id) == config.suggChannelMovie):
        await chooseWinnerMovie()

# Deletes your suggestion for the week
@bot.command(name='delete')
async def delete(ctx):
    if(str(ctx.channel.id) == config.suggChannel):
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        c.execute("DELETE FROM weekly WHERE id = ?;", (str(ctx.author)))
        conn.commit()
        dictionary.pop(str(ctx.author))
        await ctx.message.add_reaction("👍")

    elif(str(ctx.channel.id) == config.suggChannelMovie):
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        c.execute("DELETE FROM weeklyMovie WHERE id = ?;", (str(ctx.author), ))
        conn.commit()
        dictionaryMovie.pop(str(ctx.author))
        await ctx.message.add_reaction("👍")

# Chooses a winner from the album poll on the Covid Club server
async def chooseWinner():
    channel = bot.get_channel(int(config.announcementChannel))
    if(config.noWinnerMusic == 0):
        if(int(datetime.datetime.now().day) != getLastMeetingDay()):
            # Finds the last poll posted in the music announcements channel and gets the winner. Myself and the admins are the only ones that can post in that channel.
            async for message in channel.history(limit = 10):
                if message.author.id == 324631108731928587:
                    max = 0
                    index = []
                    i = 0
                    while i <  len(message.reactions):
                        if(int(message.reactions[i].count) > max):
                            max = message.reactions[i].count
                            index = [i]
                        elif message.reactions[i].count == max:
                            index.append(i)
                        i = i+1
                    await channel.send(config.musicId + 'And the winning album for the week is:')

                    # Breaks ties with the random function
                    await channel.send(message.embeds[0].description.split("\n")[random.choice(index)])
                    if(int(datetime.datetime.now().day) + 7 == getLastMeetingDay()):
                        await channel.send("It's singles week! If you have a song you want everyone to hear during the meeting next week, use the suggest command with the name of the song and the artist before then!")
                    else:
                        await channel.send("Suggestions are now open for the following week, so make sure to get them in by " + calendar.day_name[config.pollDay] + " at " + hourToPrintStandardTime(config.pollHour, config.pollMinute) + "!")
                    break
        else:
            print("Listing singles week songs...")
            if(not dictionary):
                await channel.send("No suggestions :(")
            else:
                listString = "Here are the songs for singles week: \n"
                for k, v in dictionary.items():
                    listString += f'{k} - {v}\n'
                await channel.send(listString)
                dictionary.clear()

                # Deletes all of the previous week's suggestions
                conn = sqlite3.connect('weeklyData.db')
                c = conn.cursor()
                c.execute('DELETE FROM weekly;')
                conn.commit()
    else:
        print("No winner chosen for the music club")
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        c.execute('UPDATE noWinner SET musicMeeting=0')
        conn.commit()
        config.noWinnerMusic = 0

# Chooses a winner from the album poll on the Covid Club server
async def chooseWinnerMovie():
    channel = bot.get_channel(int(config.announcementChannelMovie))
    if(config.noWinnerMovie == 0):
        # Finds the last poll posted in the movie announcements channel and gets the winner. Myself and the admins are the only ones that can post in that channel.
        async for message in channel.history(limit = 10):
            if message.author.id == 324631108731928587:
                max = 0
                index = []
                i = 0
                while i <  len(message.reactions):
                    if(int(message.reactions[i].count) > max):
                        max = message.reactions[i].count
                        index = [i]
                    elif message.reactions[i].count == max:
                        index.append(i)
                    i = i+1
                await channel.send(config.movieId + 'And the winning movie for the week is:')

                # Breaks ties with the random function
                await channel.send(message.embeds[0].description.split("\n")[random.choice(index)])
                await channel.send("Suggestions are now open for the following week, so make sure to get them in by " + calendar.day_name[config.pollDayMovie] + " at " + hourToPrintStandardTime(config.pollHourMovie, config.pollMinuteMovie) + "!")
                break
    else:
        print("No winner chosen for the movie club")
        print("No winner chosen for the music club")
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        c.execute('UPDATE noWinner SET movieMeeting=0')
        conn.commit()
        config.noWinnerMovie = 0

@bot.event
async def on_ready():
    runOnce()

#Checks if the user posted in the introductions channel and gives them member permission
@bot.event
async def on_message(message):
    if message.channel.id == 890462319384100914:
        role = get(message.guild.roles, id=889740023950376971)
        if not role in message.author.roles:
            print("Gave member role to {0}".format(message.author))
            await message.author.add_roles(role)
    await bot.process_commands(message)

bot.run(config.TOKEN)