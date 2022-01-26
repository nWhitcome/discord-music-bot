import sqlite3
import random
import calendar
import config as config
import setupFunctions as setupFunctions

# Sends out a poll so people can vote on the movie of the week
async def sendPoll(dictionary, bot):
    print("Posting poll...")
    channel = bot.get_channel(int(config.announcementChannelMovie))
    if(dictionary.items()):
        pollString = '/poll "' + config.movieId + ', here is the poll for the movie of the week:"'
        for i, j in dictionary.items():
            pollString += f' "{i} - {j}"'
        await channel.send(pollString)
        #async for message in channel.history(limit = 10):
        #    if message.author == bot.user:
        #        await message.delete()
        #        break
        dictionary.clear()

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
async def sendReminder(bot):
        channel = bot.get_channel(int(config.announcementChannelMovie))
        pollString = config.movieId + ', voting for this week starts in 30 minutes! Last chance to get your suggestions in!'
        await channel.send(pollString)

# Chooses a winner from the album poll on the Covid Club server
async def chooseWinner(bot):
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
                await channel.send("Suggestions are now open for the following week, so make sure to get them in by " + calendar.day_name[config.pollDayMovie] + " at " + setupFunctions.hourToPrintStandardTime(config.pollHourMovie, config.pollMinuteMovie) + "!")
                break
    else:
        print("No winner chosen for the movie club")
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        c.execute('UPDATE noWinner SET movieMeeting=0')
        conn.commit()
        config.noWinnerMovie = 0