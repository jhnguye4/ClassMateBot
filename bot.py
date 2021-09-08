# bot.py
import os
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

# ASK EVAN FOR THE .ENV FILE SO YOU CAN GET THE PROPER TOKENS. DO NOT PUSH THE .ENV FILE OR THE
# TOKEN TO THE INTERNET UNDER ANY CIRCUMSTANCES
# Load the environment
load_dotenv()
# Get the token for our bot
TOKEN = os.getenv('TOKEN')
# Get the token for our discord server
GUILD = os.getenv('GUILD')

# intents = Intents.all()
# Set all bot commands to begin with $
bot = Bot(command_prefix="$")


# TODO add new commands as separate files, use ping.py as a reference to how to do it
# assignees: kunwarvidhan,salvisumedh2396,sunil1511,wevanbrown,War-Keeper
# labels: Overall Progress


@bot.command(name='test', help='purely a test function')
async def test(ctx):
    await ctx.channel.send("does this work?")

# Activate when the bot starts, prints the name of the server it joins and the names of all members of that server
# TODO fix this command to accurately report the list of users in the guild
# assignees: wevanbrown,War-Keeper
# labels: bugfix
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(f'{bot.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')

    members = '\n -'.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f"cogs.{filename[:-3]}")
    bot.load_extension('jishaku')

    await bot.change_presence(activity=discord.Game("f.help"))
    print("READY!")


# Should theoretically dm someone when a new person joins but not currently working
# TODO fix this command to send a message in the welcome channel and to send a message to newly joined members
# assignees: wevanbrown,War-Keeper
# labels: bugfix
@bot.event
async def on_member_join(member):
    for channels in member.guild.channels:
        await member.channel.send('JOINED')


# Prints any potential errors to a log file
# TODO check this this actually works correctly
# assignees: wevanbrown,War-Keeper
# labels: bugfix
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@bot.command(name="shutdown", help="Shuts down the bot, only usable by the owner")
async def shutdown(ctx):
    ctx.bot.close
    print("Bot closed successfully")


# Starts the bot with the current token
bot.run(TOKEN)