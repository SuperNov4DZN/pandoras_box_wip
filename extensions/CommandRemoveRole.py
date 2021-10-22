import os, json
from discord.ext import commands
from discord.utils import get

_PATH_JSON_DB = 'data/roles.json'

class CommandRemoveRole(commands.Cog, name="Remove roles"):
    def __init__(self, client):
        self.client = client

    @commands.command(name='roleremove', aliases=['removerole', 'rrole', 'rr'], description='ESSE É UM COMANDO TESTE', brief='ESSE É O BRIEF DO COMANDO')
    async def remove_role_command(self, ctx, *args):
        if not args:
            await ctx.reply(f'{ctx.message.author.mention} please add the roles you want to remove as parameters.')
            return

        ids_list = []
        names_list = []

        if os.stat(_PATH_JSON_DB).st_size == 0:
            json_data = {}

        else:
            with open(_PATH_JSON_DB, 'r') as f:
                try:
                    json_data = json.load(f)

                except json.decoder.JSONDecodeError:
                    raise ValueError(f'CommandAddRole.command_insert(): JSONDecodeError in {_PATH_JSON_DB}')

        for arg_index in range(len(args)):
            # if the arg is a user mention
            if type(args[arg_index]) is str and args[arg_index].startswith("<@!") == True:
                member_id = int(args[arg_index].strip('<@!>'))
                # user_object = await ctx.message.guild.query_members(user_ids=[member_id])
                member_object = await self.client.fetch_user(member_id)

            # elif the arg is a role
            elif type(args[arg_index] is str and args[arg_index].startswith("<@&") == True):
                role_id = int(args[arg_index].strip('<@&>'))
                role_object = get(ctx.guild.roles, id=role_id)

                ids_list.append(str(role_object.id))
                names_list.append(role_object.name)

        uid = str(member_object.id)

        if json_data.get(uid) is not None:
            json_data[uid]['role_id'] = [x for x in json_data[uid]['role_id'] if x not in ids_list]
            json_data[uid]['role_name'] = [x for x in json_data[uid]['role_name'] if x not in names_list]
        
        else:
            return
            
        # write to file
        with open(_PATH_JSON_DB, 'w') as f:
            f.seek(0)
            json.dump(json_data, f, indent=4)

def setup(client):
    client.add_cog(CommandRemoveRole(client))