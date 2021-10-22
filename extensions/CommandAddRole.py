import os, json
from discord.ext import commands
from discord.utils import get

_PATH_JSON_DB = 'data/roles.json'

class CommandAddRole(commands.Cog, name= "Add roles"):
    def __init__(self, client):
        self.client = client

    @commands.command(name='roleadd', aliases=['addrole', 'role', 'r'])
    async def add_role_command(self, ctx, *args):
        if not args:
            await ctx.reply(f'{ctx.message.author.mention} please add the roles you want to obtain as parameters.')
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

            else:
                return

        uid = str(member_object.id)

        if json_data.get(uid) is not None:
            json_data[uid]['role_id'] = list(set().union(json_data[uid]['role_id'], ids_list))
            json_data[uid]['role_name'] = list(set().union(json_data[uid]['role_name'], names_list))
        
        else:
            user_dict = {
                'user_name': member_object.name,
                'role_id': ids_list,
                'role_name': names_list
            }

            json_data.update({uid: user_dict})

        # write to file
        with open(_PATH_JSON_DB, 'w') as f:
            f.seek(0)
            json.dump(json_data, f, indent=4)

def setup(client):
    client.add_cog(CommandAddRole(client))