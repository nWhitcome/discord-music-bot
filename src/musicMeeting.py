import sqlite3
import random
import calendar
import datetime
import config as config
import setupFunctions as setupFunctions

# Sends out a poll so people can vote on album of the week
# Takes two inputs: a dictionary used for music suggestions and a bot object to send messages from
async def sendPoll(dictionary, bot):
    if(int(datetime.datetime.now().day) + 1 != setupFunctions.getLastMeetingDay()):
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

# Sends out a reminder for the music meeting 30 minutes before
async def sendReminder(bot):
        channel = bot.get_channel(int(config.announcementChannel))
        pollString = config.musicId + ', the meeting for this week is starting in 30 minutes!'
        await channel.send(pollString)

# Chooses a winner from the album poll on the Covid Club server
async def chooseWinner(dictionary, bot):
    channel = bot.get_channel(int(config.announcementChannel))
    if(config.noWinnerMusic == 0):
        if(int(datetime.datetime.now().day) != setupFunctions.getLastMeetingDay()):
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
                    if(int(datetime.datetime.now().day) + 7 == setupFunctions.getLastMeetingDay()):
                        await channel.send("It's singles week! If you have a song you want everyone to hear during the meeting next week, use the suggest command with the name of the song and the artist before then!")
                    else:
                        await channel.send("Suggestions are now open for the following week, so make sure to get them in by " + calendar.day_name[config.pollDay] + " at " + setupFunctions.hourToPrintStandardTime(config.pollHour, config.pollMinute) + "!")
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