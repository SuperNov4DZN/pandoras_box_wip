from discord.ext import commands
from discord import embeds


class HelpAll(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    # region General BOT help
    async def send_bot_help(self, mapping):
        help_embed = {
            'title': "MODULES",
            'description': "Módulos disponíveis",
            'fields': [],
            'footer': {'text': "Super me dá uma sugada singela"}
        }

        for cog in mapping:
            if cog is None or len(mapping[cog]) == 0:
                continue

            cog_info = {'name': cog.qualified_name}

            cog_commands = ""
            for command in mapping[cog]:
                if command != mapping[cog][-1]:
                    cog_commands += f'`{command.name}`, '
                else:
                    cog_commands += f'`{command.name}`'

            cog_info['value'] = cog_commands
            cog_info['inline'] = False
            help_embed['fields'].append(cog_info)

        await self.get_destination().send(embed=embeds.Embed.from_dict(help_embed))

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

        await self.get_destination().send(embed=embeds.Embed.from_dict(help_embed))

    # endregion

    # region IDK
    async def send_group_help(self, group):
        # TODO: Make an embed
        await self.get_destination().send(
            f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')

    # endregion

    # region IDK
    async def send_command_help(self, command):
        # TODO: Make an embed
        await self.get_destination().send(f'{command.name}: {command.description}')
# endregion
