from discord.ext import commands
from discord import embeds

class CommandHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        message = ""
        for cog in mapping:
            if cog is None or len(mapping[cog]) == 0:
                continue
            message += f'{cog.qualified_name}\n'

            for command in mapping[cog]:
                message += f'`{command.name}`,'
            message += "\n\n"

        await self.get_destination().send(message)

    async def send_cog_help(self, cog):
        message = f'{cog.qualified_name}\n'

        pipipi = {
            'title': "SuperBot",
            'description': "Super",
            'fields': []
        }

        for command in cog.get_commands():
            laga = {}
            laga['name'] = command.name
            laga['value'] = command.brief
            laga['inline'] = False

            pipipi['fields'].append(laga)
            message += f'{command.name}: {command.brief}'

        embed = embeds.Embed.from_dict(pipipi)

        await self.get_destination().send(embed = embeds.Embed.from_dict(pipipi))

    async def send_group_help(self, group):
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')
        
    async def send_command_help(self, command):
        await self.get_destination().send(f'{command.name}: {command.description}')


# brief
# description