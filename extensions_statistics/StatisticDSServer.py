import json, os
import discord
from discord.ext import commands
from discord.ext import tasks


# region Class / Constructor
class StatisticDSServer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pode_rodar = [False, False]
        self.switch_pode_rodar.start()
        self.canais = load_channels()
        self.qtd_membros_online = 0
        self.qtd_membros_jogando = 0
# endregion

# region Member join - leave
    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        canal = ctx.guild.get_channel(self.canais['total'])
        qtd_membros = sum(not member.bot for member in ctx.guild.members)
        await canal.edit(name=f'👨‍👧‍👦 - Membros: {qtd_membros}')

    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        await self.on_member_join(self, ctx)
# endregion

# region listener mudança membro
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.status != after.status:
            await self.atualizar_membros_on(after)

        elif before.activity != after.activity:
            await self.atualizar_membros_jogando(after)
# endregion

# region Atualizar membro Online
    async def atualizar_membros_on(self, ctx):
        canal = ctx.guild.get_channel(self.canais['online'])
        qtd_membros = sum(
            member.status != discord.Status.offline and not member.bot for member in ctx.guild.members)

        if self.pode_rodar[0] and qtd_membros != self.qtd_membros_online:
            self.qtd_membros_online = qtd_membros
            await canal.edit(name=f'✅ - Online: {qtd_membros}')
            self.pode_rodar[0] = False
# endregion

# region Atualizar status membro
    async def atualizar_membros_jogando(self, ctx):
        canal = ctx.guild.get_channel(self.canais['jogando'])
        qtd_membros = sum(
            member.activity is not None and member.activity.type == discord.ActivityType.playing and not member.bot for member in ctx.guild.members)

        if self.pode_rodar[1] and qtd_membros != self.qtd_membros_jogando:
            self.qtd_membros_online = qtd_membros
            await canal.edit(name=f'🎮 - Jogando: {qtd_membros}')
            self.pode_rodar[1] = False
# endregion

# region Loop 15 mins
    @tasks.loop(minutes=15)
    async def switch_pode_rodar(self):
        self.pode_rodar = [True for _ in self.pode_rodar]

    @switch_pode_rodar.before_loop
    async def esperar_bot_online(self):
        await self.client.wait_until_ready()
# endregion


def load_channels():
    caminho = "./data/channels.json"
    arquivo_existe = os.path.isfile(caminho)
    if arquivo_existe:
        with open(caminho, 'r') as json_data:
            channels = json.load(json_data)
            return channels


def setup(client):
    client.add_cog(StatisticDSServer(client))
