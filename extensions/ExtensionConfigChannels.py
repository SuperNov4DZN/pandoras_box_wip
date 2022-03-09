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
        channel_mention = 0

        if channel != "online" and channel != "jogando" and channel != "total":
            await ctx.reply(
                f'O tipo de canal informado não é válido! {channel} deve ser **online**, **jogando** ou **total**')
            return

        try:
            channel_mention = int(args[1])
        except ValueError:
            await ctx.reply("O id do canal informado não é válido")
            return

        caminho = "./data/channels.json"

        json_buff = None

        if os.stat(caminho).st_size == 0:
            json_buff = {}

        with open(caminho, 'r+') as json_data:
            if json_buff is None:
                json_buff = json.load(json_data)

            json_data.seek(0, 0)
            json_buff[channel] = channel_mention
            json.dump(json_buff, json_data)
            json_data.close()


def setup(client):
    client.add_cog(ExtensionConfigChannels(client))
