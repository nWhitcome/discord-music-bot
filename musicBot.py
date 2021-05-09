import os
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
import sqlite3

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
suggChannel = '839962435044900874'
testChannel = '840042019971661825'

bot = Bot(command_prefix='$')
dictionary = {}

async def sendPoll():
    channel = bot.get_channel(839961783498571867)
    pollString = '/poll "<@&839958672868245504>, here is the poll for the album of the week:"'
    for i, j in dictionary.items():
        pollString += f' "{i} - {j}"'
    await channel.send(pollString)
    async for message in channel.history(limit = 10):
        if message.author == bot.user:
            await message.delete()
            break
    dictionary.clear()

@bot.command(name='suggest')
async def suggest(ctx, *, arg):
    if(str(ctx.channel.id) == suggChannel or str(ctx.channel.id) == testChannel):
        dictionary[ctx.author] = arg
        conn = sqlite3.connect('weeklyData.db')
        c = conn.cursor()
        print(str(ctx.author), str(arg))
        c.execute('INSERT INTO weekly(id, content) VALUES(?,?);', (str(ctx.author), str(arg)))
        conn.commit()
        await ctx.message.add_reaction("👍")

@bot.command(name='list')
async def listSuggestions(ctx):
    if(str(ctx.channel.id) == suggChannel or str(ctx.channel.id) == testChannel):
        for k, v in dictionary.items():
            await ctx.send(f'{k} - {v}')

#@bot.command(name='poll')
#async def poll(ctx):
#    await sendPoll()

@bot.event
async def on_ready():
    print("Ready")
    conn = sqlite3.connect('weeklyData.db')
    makeTable = 'CREATE TABLE IF NOT EXISTS weekly (id text PRIMARY KEY, content text NOT NULL); '

    c = conn.cursor()
    c.execute(makeTable)
    c.execute('SELECT * FROM weekly;')

    rows = c.fetchall()
    for row in rows:
        dictionary[row[0]] = row[1]

    scheduler = AsyncIOScheduler()
    scheduler.add_job(sendPoll, 'cron', day_of_week='sun', hour=12)
    scheduler.start()

bot.run(TOKEN)