from datetime import datetime
from discord import embeds
from discord.ext import commands
from discord.ext import tasks
import valve.source.a2s

# Killing floor 2 Server IP / PORT
KF_SERVER_ADDRESS = ("20.195.198.135", 27015)

# Channel where the "message to change" is
CHANNEL_ID = 892259015093014623

# Message to change
MESSAGE_ID = 901674705612832878

# region Class / Constructor
class StatisticKFServer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fetch_server_info.start()
# endregion

# region Loop every 60 seconds
    @tasks.loop(seconds=60)
    # region Get server / players info
    async def fetch_server_info(self):
        try:
            with valve.source.a2s.ServerQuerier(KF_SERVER_ADDRESS) as server:
                info = server.info()
                players = server.players()
        except valve.source.NoResponseError:
            return

        server = server.host
        nome = info.values['server_name']
        mapa = info.values['map']
        online = info.values["player_count"]
        capacidade = info.values["max_players"]

        jogadores = []

        for value in players.values['players']:
            jogadores.append((value.values['name'], value.values['score'], value.values['duration']))

        await self.enviar_embed_jogador(server, nome, mapa, online, capacidade, jogadores)
    # endregion

    # Wait until the bot is ready then start the loop
    @fetch_server_info.before_loop
    async def esperar_bot_online(self):
        await self.client.wait_until_ready()
# endregion

# region Player info Embed
    async def enviar_embed_jogador(self, server, nome , mapa, online, capacidade, jogadores):
        emb = {
            'title': f"{nome} - ({online}/{capacidade})",
            'description': f"**Mapa atual:** {mapa}",
            'color': 7419530,
            'fields': [],
            'footer': {
                'icon_url': "https://cdn.discordapp.com/embed/avatars/0.png",
                'text': f"IP: {server}"
            }
        }

        print(f"Achei {online} jogadores, sendo eles {jogadores}")

        for jogador in jogadores:
            if jogador[0] is not None and jogador[0] != '':
                player_info = {
                    'name': jogador[0],
                    'value': f"DOSH: {jogador[1]}$",
                    'inline': False
                }
                emb['fields'].append(player_info)

        canal = self.client.get_channel(CHANNEL_ID)
        mensagem = await canal.fetch_message(MESSAGE_ID)

        embed = embeds.Embed.from_dict(emb)
        embed.timestamp = datetime.utcnow()

        await mensagem.edit(embed=embed)
# endregion

def setup(client):
    client.add_cog(StatisticKFServer(client))