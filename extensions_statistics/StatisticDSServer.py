import discord
from discord.ext import commands
from discord.ext import tasks

canal_total_member = 892280493293338674
canal_member_on = 893691402595217408
canal_member_playing = 893702330510344223

# region Class / Constructor
class StatisticDSServer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pode_rodar = [False, False]
        self.switch_pode_rodar.start()
        self.qtd_membros_online = 0
        self.qtd_membros_jogando = 0
# endregion

# region Member join - leave
    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        canal = ctx.guild.get_channel(canal_total_member)
        qtdMembros = sum(not member.bot for member in ctx.guild.members)
        await canal.edit(name=f'👨‍👧‍👦 - Membros: {qtdMembros}')

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
        canal = ctx.guild.get_channel(canal_member_on)
        qtdMembros = sum(
            member.status != discord.Status.offline and not member.bot for member in ctx.guild.members)

        if self.pode_rodar[0] and qtdMembros != self.qtd_membros_online:
            self.qtd_membros_online = qtdMembros
            await canal.edit(name=f'✅ - Online: {qtdMembros}')
            self.pode_rodar[0] = False
# endregion

# region Atualizar status membro
    async def atualizar_membros_jogando(self, ctx):
        canal = ctx.guild.get_channel(canal_member_playing)
        qtdMembros = sum(
            member.activity is not None and member.activity.type == discord.ActivityType.playing and not member.bot for member in ctx.guild.members)

        if self.pode_rodar[1] and qtdMembros != self.qtd_membros_jogando:
            self.qtd_membros_online = qtdMembros
            await canal.edit(name=f'🎮 - Jogando: {qtdMembros}')
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

def setup(client):
    client.add_cog(StatisticDSServer(client))