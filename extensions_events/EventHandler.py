from discord.ext import commands


class EventHandler(commands.Cog, name="Event Handler"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.reply(f'Cant execute the command cause of the following "{error}"')


def setup(client):
    client.add_cog(EventHandler(client))