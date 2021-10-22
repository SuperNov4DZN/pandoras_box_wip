import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from CommandHelp import CommandHelp
load_dotenv(dotenv_path="secrets\.env")

read_env = os.getenv

extensions = os.listdir('extensions')

bot_token = read_env("BOT_TOKEN")
bot_prefix = read_env("BOT_PREFIX")

client = commands.Bot(command_prefix=bot_prefix, help_command=CommandHelp())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}.')

for ext in extensions:
    name, ext = os.path.splitext(ext)
    if ext == '.py':
        client.load_extension(f'extensions.{name}')
        print(f'{name} was loaded!')

client.run(bot_token)
