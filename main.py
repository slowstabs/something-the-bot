import discord
from discord.ext import commands
import json
import random
import mysql.connector


intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

message_count = {}

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='dbtest'
)

# Load message counts from a JSON file if available
def load_message_count():
    try:
        with open('message_count.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save message counts to a JSON file
def save_message_count():
    with open('message_count.json', 'w') as file:
        json.dump(message_count, file)

@client.event
async def on_ready():
    print('Bot is ready')
    await client.tree.sync()
    global message_count
    message_count = load_message_count()  # Load previous message counts when the bot starts

@client.tree.command(name="hello", description="Says hello!")

async def hello(message):
    embedvar = discord.Embed(title="Response", description="Hello", color=0x00ff00)
    await message.channel.send(embed=embedvar)

@client.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore messages from bots

    author = str(message.author)
    if author in message_count:
        message_count[author] += 1
    else:
        message_count[author] = 1

    await client.process_commands(message)

@client.command()
async def messagecount(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if isinstance(member, discord.Member):
        user_count = message_count.get(str(member), 0)
        embedvar = discord.Embed(title="User", description=member, color=0x00ff00)
        embedvar.add_field(name="Number of Messages", value=user_count, inline=False)
        await ctx.send(embed=embedvar)
    else:
        await ctx.send("Please mention a valid user.")

@client.command()

async def tellme(ctx, *, question):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes, definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
        "Hell no, you ugly as shit"
    ]

    response = random.choice(responses)
    embedvar = discord.Embed(title="Question", description=question, color=0x351C75)
    embedvar.add_field(name="8 Ball", value=response, inline=False)
    await ctx.send(embed=embedvar)

@client.command()

async def roll(ctx):
    embedvar = discord.Embed(title="You rolled the dice!", description=random.randint(1, 6), color=0x351C75)
    await ctx.send(embed=embedvar)

@client.event
async def on_disconnect():
    save_message_count()

client.run("CLIENT TOKEN")
