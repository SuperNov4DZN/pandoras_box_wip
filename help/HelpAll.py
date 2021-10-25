from discord.ext import commands
from discord import embeds

class HelpAll(commands.HelpCommand):
    def __init__(self):
        super().__init__()

# region General BOT help
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
# endregion

# region Individual module help
    async def send_cog_help(self, cog):
        message = f'{cog.qualified_name}\n'

        help_embed = {
            'title': "BOT HELP",
            'description': "Comandos disponiveis",
            'fields': []
        }

        for command in cog.get_commands():
            command_info = {}
            command_info['name'] = command.name
            command_info['value'] = command.brief
            command_info['inline'] = False

            help_embed['fields'].append(command_info)
            message += f'{command.name}: {command.brief}'

        embed = embeds.Embed.from_dict(help_embed)

        await self.get_destination().send(embed = embeds.Embed.from_dict(help_embed))
# endregion

# region IDK
    async def send_group_help(self, group):
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')
# endregion
        
# region IDK
    async def send_command_help(self, command):
        await self.get_destination().send(f'{command.name}: {command.description}')
# endregion