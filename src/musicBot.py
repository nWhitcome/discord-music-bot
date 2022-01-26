from discord.ext.commands import Bot
from discord.utils import get
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import sqlite3
import calendar
import config as config
import musicMeeting as musicMeeting
import movieMeeting as movieMeeting
import setupFunctions as setupFunctions

bot = Bot(command_prefix=config.commandPrefix)

bot.runOnceFlag = 0
dictionary = {}
dictionaryMovie = {}
themeDictionary = {}
themeDictionaryMovie = {}

themeDictionary = {"Nate": ["One", "Two", "Three"], "Dave": ["One", "Two", "Three"], "Hello": ["One", "Two", "Three"]}

# Code content that is run once when the bot is started up. For example: cron job declarations and selecting data from a database
def runOnce():
    if(bot.runOnceFlag == 0):
        print("Ready")
        conn = sqlite3.connect('weeklyData.db')
        makeTable = 'CREATE TABLE IF NOT EXISTS weekly (id text PRIMARY KEY, content text NOT NULL); '
        makeTableMovies = 'CREATE TABLE IF NOT EXISTS weeklyMovie (id text PRIMARY KEY, content text NOT NULL); '
        makeNoWinnerTable = 'CREATE TABLE IF NOT EXISTS noWinner (id text PRIMARY KEY, musicMeeting integer NOT NULL, movieMeeting integer NOT NULL); '
        makeMusicThemesTable = 'CREATE TABLE IF NOT EXISTS musicThemes (id text PRIMARY KEY, themeOne text, themeTwo text, themeThree text, themeFour text, themeFive text); '

        c = conn.cursor()
        c.execute(makeTable)
        c.execute(makeTableMovies)
        c.execute(makeNoWinnerTable)
        c.execute(makeMusicThemesTable)
        
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
        scheduler.add_job(musicMeeting.sendPoll, 'cron', day_of_week=config.pollDay, hour=config.pollHour, minute=config.pollMinute, args=[dictionary, bot])
        scheduler.add_job(movieMeeting.sendPoll, 'cron', day_of_week=config.pollDayMovie, hour=config.pollHourMovie, minute=config.pollMinuteMovie, args=[dictionary, bot])
        scheduler.add_job(musicMeeting.sendReminder, 'cron', day_of_week=config.meetingDay, hour=config.reminderHour, minute=config.reminderMinute, args=[bot])
        scheduler.add_job(movieMeeting.sendReminder, 'cron', day_of_week=config.meetingDayMovie, hour=config.reminderHourMovie, minute=config.reminderMinuteMovie, args=[bot])
        scheduler.add_job(musicMeeting.chooseWinner, 'cron', day_of_week=config.meetingDay, hour=config.meetingHour, minute=config.meetingMinute, args=[dictionary, bot])
        scheduler.add_job(movieMeeting.chooseWinner, 'cron', day_of_week=config.meetingDayMovie, hour=config.meetingHourMovie, minute=config.meetingMinuteMovie, args=[bot])
        scheduler.start()
        print("Music poll set for " + calendar.day_name[config.pollDay] + " " + setupFunctions.hourToPrintStandardTime(config.pollHour, config.pollMinute))
        print("Music reminder set for " + calendar.day_name[config.meetingDay] + " " + setupFunctions.hourToPrintStandardTime(config.reminderHour, config.reminderMinute))
        print("Music meeting set for " + calendar.day_name[config.meetingDay] + " " + setupFunctions.hourToPrintStandardTime(config.meetingHour, config.meetingMinute))
        print("Movie poll set for " + calendar.day_name[config.pollDayMovie] + " " + setupFunctions.hourToPrintStandardTime(config.pollHourMovie, config.pollMinuteMovie))
        print("Movie reminder set for " + calendar.day_name[config.pollDayMovie] + " " + setupFunctions.hourToPrintStandardTime(config.reminderHourMovie, config.reminderMinuteMovie))
        print("Movie meeting set for " + calendar.day_name[config.meetingDayMovie] + " " + setupFunctions.hourToPrintStandardTime(config.meetingHourMovie, config.meetingMinuteMovie))
        bot.runOnceFlag = 1

# Allows users to submit a suggestion for album of the week, which is then stored in a database
@bot.command(name='theme')
async def suggest(ctx, *, arg):
    print("Received theme suggestion")
    if(str(ctx.channel.id) == config.suggChannel):
        authorName = str(ctx.author)
        if(not authorName in themeDictionary):
            themeDictionary[authorName] = []
        themeDictionary[authorName].insert(0, str(arg[:256]))
        if(len(themeDictionary[authorName]) > 3):
            themeDictionary[authorName].pop()
        print(themeDictionary)
        # conn = sqlite3.connect('weeklyData.db')
        # c = conn.cursor()
        # c.execute('INSERT OR REPLACE INTO weekly(id, content) VALUES(?,?);', (str(ctx.author), str(arg[:256])))
        # conn.commit()
        await ctx.message.add_reaction("👍")

    elif(str(ctx.channel.id) == config.suggChannelMovie):
        authorName = str(ctx.author)
        if(not authorName in themeDictionaryMovie):
            themeDictionaryMovie[authorName] = []
        themeDictionaryMovie[authorName].insert(0, str(arg[:256]))
        if(len(themeDictionaryMovie[authorName]) > 3):
            themeDictionaryMovie[authorName].pop()
        print(themeDictionaryMovie)
        # conn = sqlite3.connect('weeklyData.db')
        # c = conn.cursor()
        # c.execute('INSERT OR REPLACE INTO weeklyMovie(id, content) VALUES(?,?);', (str(ctx.author), str(arg[:256])))
        # conn.commit()
        await ctx.message.add_reaction("👍")

    else:
        print("Err: couldn't take suggestion")

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

# Lists all of the album choices that have been submitted
@bot.command(name='listMyThemes')
async def listSuggestions(ctx):
    authorName = str(ctx.author)
    print("Printing theme suggestions for " + authorName)
    listString = authorName + "\n"
    if(str(ctx.channel.id) == config.suggChannel):
        if(not authorName in themeDictionary):
            await ctx.send("No theme suggestions from you :(")
        else:
            for idx, k in enumerate(themeDictionary[str(ctx.author)]):
                listString += f'{idx + 1} - {k}\n'
            await ctx.send(listString)

    if(str(ctx.channel.id) == config.suggChannelMovie):
        if(not authorName in themeDictionaryMovie):
            await ctx.send("No theme suggestions from you :(")
        else:
            for idx, k in enumerate(themeDictionaryMovie[str(ctx.author)]):
                listString += f'{idx + 1} - {k}\n'
            await ctx.send(listString)

# Lists all of the album choices that have been submitted
@bot.command(name='listAllThemes')
async def listSuggestions(ctx):
    print("Printing all theme suggestions")
    listString = ""
    if(str(ctx.channel.id) == config.suggChannel):
        for key in themeDictionary:
            listString += key + "\n"
            for idx, k in enumerate(themeDictionary[key]):
                listString += f'{idx + 1} - {k}\n'
            listString += "\n"
        await ctx.send(listString)

    if(str(ctx.channel.id) == config.suggChannelMovie):
        for key in themeDictionaryMovie:
            listString += key + "\n"
            for idx, k in enumerate(themeDictionaryMovie[key]):
                listString += f'{idx + 1} - {k}\n'
            listString += "\n"
        await ctx.send(listString)

# Backup method that can only be called in the TestBot server that puts the album choice poll up in case it fails for some reason
@bot.command(name='poll')
async def poll(ctx):
    if(config.inTest == 1 and str(ctx.channel.id) == config.suggChannel):
        await musicMeeting.sendPoll(dictionary, bot)

# Backup method that can only be called in the TestBot server that puts the album choice poll up in case it fails for some reason
@bot.command(name='pollMovie')
async def pollmovie(ctx):
    if(config.inTest == 1 and str(ctx.channel.id) == config.suggChannelMovie):
        await movieMeeting.sendPoll(dictionary, bot)

# Backup method that can only be called in the TestBot server that chooses the winner
@bot.command(name='choosethewinner')
async def choosethewinner(ctx):
    if(config.inTest == 1 and str(ctx.channel.id) == config.suggChannel):
        await musicMeeting.chooseWinner(dictionary, bot)

# Backup method that can only be called in the TestBot server that chooses the winner
@bot.command(name='choosethewinnermovie')
async def choosethewinnermovie(ctx):
    if(config.inTest == 1 and str(ctx.channel.id) == config.suggChannelMovie):
        await movieMeeting.chooseWinner(bot)

# Deletes your suggestion for the week
@bot.command(name='delete')
async def delete(ctx):
    if(str(ctx.channel.id) == config.suggChannel):
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        c.execute("DELETE FROM weekly WHERE id = ?;", (str(ctx.author), ))
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