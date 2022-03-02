import json
import os
from discord.ext import commands


class ExtensionConfigChannels(commands.Cog, name="Config channels"):
    def __init__(self, client):
        self.client = client

    @commands.command(name='channels',
                      aliases=['c', 'canais'],
                      brief="``channels online #membrosonline``",
                      description="Configuração dos canais de estatísticas do servidor."
                                  "\nDevem ser configurados os canais \'online\', \'jogando\' e \'total\'.")
    async def channel_online(self, ctx, *args):
        if not args or len(args) < 2:
            await ctx.reply(f'{ctx.message.author.mention} please mention the channel being configured')

        channel = args[0]
        channel_mention = args[1]

        caminho = "./data/channels.json"
        json_data = open(caminho, 'w+')

        if os.stat(caminho).st_size == 0:
            json_buff = {}

        else:
            json_buff = json.load(json_data)

        json_buff[channel] = channel_mention
        json.dump(json_buff, json_data)
        json_data.close()


def setup(client):
    client.add_cog(ExtensionConfigChannels(client))
