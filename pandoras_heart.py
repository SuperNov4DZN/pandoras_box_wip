import os
from discord.ext import commands
from dotenv import load_dotenv
from help.HelpAll import HelpAll
load_dotenv(dotenv_path="secrets\.env")

read_env = os.getenv

# region load each module folder
extensions = os.listdir('extensions')
events = os.listdir('extensions_events')
statistics = os.listdir('extensions_statistics')
# endregion

# Load bot token and prefix from .env
bot_token = read_env("BOT_TOKEN")
bot_prefix = read_env("BOT_PREFIX")

# Creat a new bot client
client = commands.Bot(command_prefix=bot_prefix, help_command=HelpAll())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}.')

# region Load extensions modules
for ext in extensions:
    name, extension = os.path.splitext(ext)
    if extension == '.py':
        client.load_extension(f'extensions.{name}')
        print(f'{name} was loaded!      [Extension]')
# endregion

# region Load events modules
for evt in events:
    name, extension = os.path.splitext(evt)
    if extension == '.py':
        client.load_extension(f'extensions_events.{name}')
        print(f'{name} was loaded!      [Events]')
# endregion

# region Load statistics modules
for sts in statistics:
    name, extension = os.path.splitext(sts)
    if extension == '.py':
        client.load_extension(f'extensions_statistics.{name}')
        print(f'{name} was loaded!      [Statistic]')
# endregion

# Start the bot with the given token
client.run(bot_token)