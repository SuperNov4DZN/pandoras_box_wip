from discord.ext import commands

used_commands = {

}

class CommandEventHandler(commands.Cog, name="Event Handler"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.reply(f'Cant execute the command cause of the following "{error}"')

    # @commands.Cog.listener()
    # async def on_command(self, ctx):
    #     if ctx.command is not None:
    #         if ctx.command.name in used_commands:
    #             used_commands[ctx.command.name] += 1
    #         else:
    #             used_commands[ctx.command.name] = 1
    #         await ctx.reply(f'Used commands {used_commands}')

    # @commands.Cog.listener()
    # async def on_command_completion(self, ctx):
    #     await ctx.reply(f'{ctx.command.name} was used correctly')

def setup(client):
    client.add_cog(CommandEventHandler(client))